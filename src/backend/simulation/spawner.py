"""Order spawning with zone-based density and time-of-day profiles."""

from __future__ import annotations

import math
import random
from typing import List, TYPE_CHECKING

from simulation.entities import Order, OrderStatus

if TYPE_CHECKING:
    from simulation.engine import SimulationEngine


def _time_multiplier(sim_hour: float) -> float:
    """Return demand multiplier based on simulated hour of day.

    Lunch (12–14): 3×
    Evening (19–21): 2.5×
    Light morning (10–12): 1.5×
    Off-peak: 1×
    """
    if 12.0 <= sim_hour < 14.0:
        return 3.0
    if 19.0 <= sim_hour < 21.0:
        return 2.5
    if 10.0 <= sim_hour < 12.0:
        return 1.5
    return 1.0


def _random_point_in_circle(center_lat: float, center_lng: float, radius: float) -> tuple[float, float]:
    """Return a random (lat, lng) uniformly distributed inside a circle."""
    angle = random.uniform(0, 2 * math.pi)
    # sqrt for uniform area distribution
    r = radius * math.sqrt(random.random())
    return center_lat + r * math.sin(angle), center_lng + r * math.cos(angle)


def spawn_orders(engine: "SimulationEngine") -> List[Order]:
    """Spawn new orders probabilistically for each zone. Returns list of newly created orders."""
    sim_hour = engine.sim_hour()
    time_mult = _time_multiplier(sim_hour)
    new_orders: List[Order] = []

    for zone in engine.zones:
        effective_rate = zone.base_order_rate * time_mult
        if random.random() < effective_rate:
            # Pick a random restaurant in this zone
            zone_restaurants = [r for r in engine.restaurants if r.zone_id == zone.id]
            if not zone_restaurants:
                continue
            restaurant = random.choice(zone_restaurants)

            # Customer location: random point within zone
            cust_lat, cust_lng = _random_point_in_circle(
                zone.center_lat, zone.center_lng, zone.radius
            )

            engine.next_order_id += 1
            order = Order(
                id=engine.next_order_id,
                restaurant_id=restaurant.id,
                restaurant_lat=restaurant.lat,
                restaurant_lng=restaurant.lng,
                customer_lat=cust_lat,
                customer_lng=cust_lng,
                status=OrderStatus.PENDING,
                created_tick=engine.tick,
            )
            new_orders.append(order)

    return new_orders
