"""Simulation engine — tick loop, clock, dual-strategy orchestration."""

from __future__ import annotations

import asyncio
import math
import random
from typing import Any, Dict, List, Optional

import redis.asyncio as aioredis

from config import (
    BASE_TICK_INTERVAL,
    CENTER_LAT,
    CENTER_LNG,
    CITY_RADIUS,
    NUM_RIDERS,
    NUM_RESTAURANTS,
    REDIS_URL,
    RESTAURANT_NAMES,
    RIDER_SPEED,
    SECONDS_PER_TICK,
    SIM_START_HOUR,
    SIM_START_MINUTE,
    ZONES,
)
from simulation.entities import (
    Order,
    OrderStatus,
    Restaurant,
    Rider,
    RiderStatus,
    Zone,
)
from simulation.matcher import match_and_progress_orders
from simulation.nudger import move_repositioning_riders, nudge_idle_riders
from simulation.spawner import spawn_orders


class SimulationEngine:
    """Manages the full simulation state and tick loop."""

    def __init__(self) -> None:
        # Tick state
        self.tick: int = 0
        self.speed_multiplier: int = 1
        self.running: bool = False
        self._task: Optional[asyncio.Task] = None

        # Entity state
        self.zones: List[Zone] = []
        self.restaurants: List[Restaurant] = []
        self.nudged_riders: List[Rider] = []
        self.naive_riders: List[Rider] = []
        self.nudged_orders: List[Order] = []
        self.naive_orders: List[Order] = []
        self.next_order_id: int = 0

        # KPI accumulators
        self.nudged_deliveries: int = 0
        self.naive_deliveries: int = 0
        self.nudged_pickup_ticks: List[int] = []
        self.naive_pickup_ticks: List[int] = []

        # Redis
        self.redis: Optional[aioredis.Redis] = None

        # WebSocket broadcast callback (set by main.py)
        self._broadcast_fn = None

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    async def initialize(self) -> None:
        """Set up Redis connection (optional) and generate initial state."""
        # Try Redis
        try:
            self.redis = aioredis.from_url(REDIS_URL, decode_responses=True)
            await self.redis.ping()
        except Exception:
            self.redis = None

        self._build_initial_state()

    def _build_initial_state(self) -> None:
        """Create zones, restaurants, and riders."""
        # Zones
        self.zones = [
            Zone(
                id=z.id,
                name=z.name,
                center_lat=z.center_lat,
                center_lng=z.center_lng,
                radius=z.radius,
                base_order_rate=z.base_order_rate,
            )
            for z in ZONES
        ]

        # Restaurants — distribute across zones
        self.restaurants = []
        restaurants_per_zone = NUM_RESTAURANTS // len(ZONES)
        extra = NUM_RESTAURANTS % len(ZONES)
        rid = 0
        name_idx = 0
        for zi, zone in enumerate(self.zones):
            count = restaurants_per_zone + (1 if zi < extra else 0)
            for _ in range(count):
                rid += 1
                angle = random.uniform(0, 2 * math.pi)
                r = zone.radius * 0.7 * math.sqrt(random.random())
                lat = zone.center_lat + r * math.sin(angle)
                lng = zone.center_lng + r * math.cos(angle)
                name = RESTAURANT_NAMES[name_idx % len(RESTAURANT_NAMES)]
                name_idx += 1
                self.restaurants.append(
                    Restaurant(id=rid, lat=lat, lng=lng, name=name, zone_id=zone.id)
                )

        # Riders — scattered across city area
        self.nudged_riders = []
        self.naive_riders = []
        for i in range(1, NUM_RIDERS + 1):
            angle = random.uniform(0, 2 * math.pi)
            r = CITY_RADIUS * math.sqrt(random.random())
            lat = CENTER_LAT + r * math.sin(angle)
            lng = CENTER_LNG + r * math.cos(angle)
            self.nudged_riders.append(
                Rider(id=i, lat=lat, lng=lng, speed=RIDER_SPEED)
            )
            # Naive riders start at same positions
            self.naive_riders.append(
                Rider(id=i, lat=lat, lng=lng, speed=RIDER_SPEED)
            )

        # Reset orders and KPIs
        self.nudged_orders = []
        self.naive_orders = []
        self.next_order_id = 0
        self.nudged_deliveries = 0
        self.naive_deliveries = 0
        self.nudged_pickup_ticks = []
        self.naive_pickup_ticks = []
        self.tick = 0

    # ------------------------------------------------------------------
    # Sim clock
    # ------------------------------------------------------------------

    def sim_hour(self) -> float:
        """Current simulated hour of day (decimal)."""
        total_seconds = (SIM_START_HOUR * 3600 + SIM_START_MINUTE * 60) + self.tick * SECONDS_PER_TICK
        total_seconds %= 86400  # wrap at midnight
        return total_seconds / 3600.0

    def sim_time_str(self) -> str:
        """Human-readable sim time, e.g. '12:34 PM'."""
        h = self.sim_hour()
        hours = int(h)
        minutes = int((h - hours) * 60)
        period = "AM" if hours < 12 else "PM"
        display_hour = hours % 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minutes:02d} {period}"

    # ------------------------------------------------------------------
    # Redis sync
    # ------------------------------------------------------------------

    async def _sync_riders_to_redis(self) -> None:
        """Update rider positions in Redis geo sets."""
        if self.redis is None:
            return
        try:
            pipe = self.redis.pipeline()
            pipe.delete("riders:nudged", "riders:naive")

            nudged_members = []
            for r in self.nudged_riders:
                nudged_members.extend([r.lng, r.lat, str(r.id)])
            if nudged_members:
                pipe.geoadd("riders:nudged", nudged_members)

            naive_members = []
            for r in self.naive_riders:
                naive_members.extend([r.lng, r.lat, str(r.id)])
            if naive_members:
                pipe.geoadd("riders:naive", naive_members)

            await pipe.execute()
        except Exception:
            pass  # Redis unavailable — matcher will fall back to brute force

    # ------------------------------------------------------------------
    # KPI computation
    # ------------------------------------------------------------------

    def _compute_kpis(self) -> Dict[str, Any]:
        """Compute KPIs for both strategies."""

        def _kpis_for(riders: List[Rider], orders: List[Order], pickup_history: List[int], delivery_count: int) -> Dict[str, Any]:
            idle_count = sum(1 for r in riders if r.status == RiderStatus.IDLE)
            idle_pct = round(idle_count / len(riders) * 100) if riders else 0

            # Average pickup time (ticks between created and picked_up)
            avg_pickup = 0.0
            if pickup_history:
                avg_pickup = round(sum(pickup_history) / len(pickup_history), 1)

            # Coverage: percentage of city zones that have at least one rider nearby
            zone_coverage = 0
            for zone in self.zones:
                for r in riders:
                    d = math.sqrt((r.lat - zone.center_lat) ** 2 + (r.lng - zone.center_lng) ** 2)
                    if d < zone.radius * 2:
                        zone_coverage += 1
                        break
            coverage_pct = round(zone_coverage / len(self.zones) * 100) if self.zones else 0

            return {
                "avg_pickup": avg_pickup,
                "idle_pct": idle_pct,
                "deliveries": delivery_count,
                "coverage": coverage_pct,
            }

        return {
            "nudged": _kpis_for(self.nudged_riders, self.nudged_orders, self.nudged_pickup_ticks, self.nudged_deliveries),
            "naive": _kpis_for(self.naive_riders, self.naive_orders, self.naive_pickup_ticks, self.naive_deliveries),
        }

    # ------------------------------------------------------------------
    # Heatmap data
    # ------------------------------------------------------------------

    def _heatmap_data(self) -> List[List[float]]:
        """Generate heatmap points from active orders (nudged set)."""
        points = []
        for order in self.nudged_orders:
            if order.status in (OrderStatus.PENDING, OrderStatus.ASSIGNED):
                points.append([
                    round(order.restaurant_lat, 6),
                    round(order.restaurant_lng, 6),
                    0.8,
                ])
        # Also add zone centers with intensity proportional to base rate
        for zone in self.zones:
            points.append([
                round(zone.center_lat, 6),
                round(zone.center_lng, 6),
                round(zone.base_order_rate * 3, 2),
            ])
        return points

    # ------------------------------------------------------------------
    # Full state snapshot
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "tick": self.tick,
            "sim_time": self.sim_time_str(),
            "speed": self.speed_multiplier,
            "running": self.running,
            "riders": [r.to_dict() for r in self.nudged_riders],
            "naive_riders": [r.to_dict() for r in self.naive_riders],
            "restaurants": [r.to_dict() for r in self.restaurants],
            "orders": [o.to_dict() for o in self.nudged_orders if o.status != OrderStatus.DELIVERED],
            "heatmap": self._heatmap_data(),
            "kpis": self._compute_kpis(),
            "zones": [z.to_dict() for z in self.zones],
        }

    # ------------------------------------------------------------------
    # Tick pipeline
    # ------------------------------------------------------------------

    async def _do_tick(self) -> None:
        """Execute one simulation tick."""
        self.tick += 1

        # 1. Spawn orders (same orders for both strategies)
        new_orders = spawn_orders(self)
        # Deep copy for naive side — same orders, independent lifecycle
        for order in new_orders:
            self.nudged_orders.append(order)
            naive_copy = Order(
                id=order.id,
                restaurant_id=order.restaurant_id,
                restaurant_lat=order.restaurant_lat,
                restaurant_lng=order.restaurant_lng,
                customer_lat=order.customer_lat,
                customer_lng=order.customer_lng,
                status=OrderStatus.PENDING,
                created_tick=order.created_tick,
            )
            self.naive_orders.append(naive_copy)

        # 2. Sync rider positions to Redis
        await self._sync_riders_to_redis()

        # 3. Match orders to riders — both strategies
        await match_and_progress_orders(self, self.nudged_riders, self.nudged_orders, "riders:nudged")
        await match_and_progress_orders(self, self.naive_riders, self.naive_orders, "riders:naive")

        # Track new deliveries and pickup times
        for o in self.nudged_orders:
            if o.status == OrderStatus.DELIVERED and o.delivered_tick == self.tick:
                self.nudged_deliveries += 1
                if o.picked_up_tick and o.assigned_tick:
                    self.nudged_pickup_ticks.append(o.picked_up_tick - o.created_tick)
        for o in self.naive_orders:
            if o.status == OrderStatus.DELIVERED and o.delivered_tick == self.tick:
                self.naive_deliveries += 1
                if o.picked_up_tick and o.assigned_tick:
                    self.naive_pickup_ticks.append(o.picked_up_tick - o.created_tick)

        # 4. Nudge idle NUDGED riders (naive riders do nothing when idle)
        nudge_idle_riders(self, self.nudged_riders, self.nudged_orders)

        # 5. Move repositioning riders (nudged only — naive stay put)
        move_repositioning_riders(self.nudged_riders)

        # 6. Clean up old delivered orders (keep last 200 for KPI history)
        self.nudged_orders = [o for o in self.nudged_orders if o.status != OrderStatus.DELIVERED or self.tick - (o.delivered_tick or 0) < 50]
        self.naive_orders = [o for o in self.naive_orders if o.status != OrderStatus.DELIVERED or self.tick - (o.delivered_tick or 0) < 50]

        # 7. Broadcast state
        if self._broadcast_fn:
            await self._broadcast_fn(self.snapshot())

    # ------------------------------------------------------------------
    # Control API
    # ------------------------------------------------------------------

    async def start(self) -> None:
        if self.running:
            return
        self.running = True
        self._task = asyncio.create_task(self._tick_loop())

    async def pause(self) -> None:
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def reset(self) -> None:
        await self.pause()
        self._build_initial_state()
        # Flush Redis geo keys
        if self.redis:
            try:
                await self.redis.delete("riders:nudged", "riders:naive")
            except Exception:
                pass
        # Broadcast reset state
        if self._broadcast_fn:
            await self._broadcast_fn(self.snapshot())

    def set_speed(self, multiplier: int) -> None:
        self.speed_multiplier = max(1, min(multiplier, 10))

    async def _tick_loop(self) -> None:
        """Main async loop — runs ticks at configured speed."""
        while self.running:
            await self._do_tick()
            interval = BASE_TICK_INTERVAL / self.speed_multiplier
            await asyncio.sleep(interval)
