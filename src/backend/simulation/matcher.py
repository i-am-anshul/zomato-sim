"""Order-to-rider matching using nearest idle rider.

Uses Redis GEOSEARCH when available, falls back to brute-force.
"""

from __future__ import annotations

import math
from typing import List, Optional, TYPE_CHECKING

from simulation.entities import Order, OrderStatus, Rider, RiderStatus
from config import ARRIVAL_THRESHOLD

if TYPE_CHECKING:
    from simulation.engine import SimulationEngine


def _distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Euclidean distance in degrees (sufficient for same-city comparison)."""
    return math.sqrt((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2)


def _find_nearest_idle_rider_brute(
    riders: List[Rider], lat: float, lng: float, max_radius: float = 0.05
) -> Optional[Rider]:
    """Brute-force nearest idle rider within max_radius."""
    best: Optional[Rider] = None
    best_dist = max_radius
    for rider in riders:
        if rider.status != RiderStatus.IDLE:
            continue
        d = _distance(rider.lat, rider.lng, lat, lng)
        if d < best_dist:
            best_dist = d
            best = rider
    return best


async def _find_nearest_idle_rider_redis(
    engine: "SimulationEngine",
    redis_key: str,
    riders: List[Rider],
    lat: float,
    lng: float,
    max_radius_km: float = 5.0,
) -> Optional[Rider]:
    """Use Redis GEOSEARCH to find nearest idle rider."""
    if engine.redis is None:
        return _find_nearest_idle_rider_brute(riders, lat, lng)

    try:
        results = await engine.redis.geosearch(
            redis_key,
            longitude=lng,
            latitude=lat,
            radius=max_radius_km,
            unit="km",
            sort="ASC",
            count=20,  # get a few candidates
        )
        rider_map = {str(r.id): r for r in riders}
        for member in results:
            member_str = member if isinstance(member, str) else member.decode()
            rider = rider_map.get(member_str)
            if rider and rider.status == RiderStatus.IDLE:
                return rider
        return None
    except Exception:
        return _find_nearest_idle_rider_brute(riders, lat, lng)


def _move_rider_toward(rider: Rider, target_lat: float, target_lng: float) -> bool:
    """Move rider one step toward target. Returns True if arrived."""
    d = _distance(rider.lat, rider.lng, target_lat, target_lng)
    if d <= ARRIVAL_THRESHOLD:
        rider.lat = target_lat
        rider.lng = target_lng
        return True

    # Normalize direction and move by rider speed
    dlat = (target_lat - rider.lat) / d
    dlng = (target_lng - rider.lng) / d
    rider.lat += dlat * rider.speed
    rider.lng += dlng * rider.speed
    return False


async def match_and_progress_orders(
    engine: "SimulationEngine",
    riders: List[Rider],
    orders: List[Order],
    redis_key: str,
) -> None:
    """Match pending orders to nearest idle riders and progress active deliveries.

    Handles the full lifecycle: pending → assigned → picked_up → delivered.
    """
    # --- Phase 1: Progress existing deliveries ---
    for order in orders:
        if order.status == OrderStatus.DELIVERED:
            continue

        if order.assigned_rider_id is None:
            continue

        rider = _get_rider(riders, order.assigned_rider_id)
        if rider is None:
            continue

        if order.status == OrderStatus.ASSIGNED:
            # Rider is heading to restaurant
            arrived = _move_rider_toward(rider, order.restaurant_lat, order.restaurant_lng)
            if arrived:
                order.status = OrderStatus.PICKED_UP
                order.picked_up_tick = engine.tick
                rider.target_lat = order.customer_lat
                rider.target_lng = order.customer_lng

        elif order.status == OrderStatus.PICKED_UP:
            # Rider is heading to customer
            arrived = _move_rider_toward(rider, order.customer_lat, order.customer_lng)
            if arrived:
                order.status = OrderStatus.DELIVERED
                order.delivered_tick = engine.tick
                rider.status = RiderStatus.IDLE
                rider.target_lat = None
                rider.target_lng = None
                rider.current_order_id = None

    # --- Phase 2: Match pending orders to idle riders ---
    pending = [o for o in orders if o.status == OrderStatus.PENDING]
    for order in pending:
        rider = await _find_nearest_idle_rider_redis(
            engine, redis_key, riders, order.restaurant_lat, order.restaurant_lng
        )
        if rider is None:
            continue

        # Assign
        order.status = OrderStatus.ASSIGNED
        order.assigned_rider_id = rider.id
        order.assigned_tick = engine.tick
        rider.status = RiderStatus.DELIVERING
        rider.current_order_id = order.id
        rider.target_lat = order.restaurant_lat
        rider.target_lng = order.restaurant_lng


def _get_rider(riders: List[Rider], rider_id: int) -> Optional[Rider]:
    for r in riders:
        if r.id == rider_id:
            return r
    return None
