"""Gravity-based nudging with repulsion for idle riders.

Nudged riders are attracted toward pending orders (demand) and repelled
from nearby riders (to prevent clumping).
"""

from __future__ import annotations

import math
from typing import List, TYPE_CHECKING

from simulation.entities import Order, OrderStatus, Rider, RiderStatus
from config import (
    NUDGE_RADIUS,
    REPULSION_RADIUS,
    REPULSION_FACTOR,
    GRAVITY_MIN_DIST,
    RIDER_SPEED,
    CENTER_LAT,
    CENTER_LNG,
    CITY_RADIUS,
)

if TYPE_CHECKING:
    from simulation.engine import SimulationEngine


def _distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    return math.sqrt((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2)


def _clamp_to_city(lat: float, lng: float) -> tuple[float, float]:
    """Keep position within city circle."""
    d = _distance(lat, lng, CENTER_LAT, CENTER_LNG)
    if d > CITY_RADIUS:
        # Pull back toward center
        ratio = CITY_RADIUS / d
        lat = CENTER_LAT + (lat - CENTER_LAT) * ratio
        lng = CENTER_LNG + (lng - CENTER_LNG) * ratio
    return lat, lng


def nudge_idle_riders(
    engine: "SimulationEngine",
    riders: List[Rider],
    orders: List[Order],
) -> None:
    """Apply gravity + repulsion to idle nudged riders.

    Idle riders are pulled toward pending/assigned orders (demand signal)
    and pushed away from other nearby riders (prevents clumping).
    """
    # Collect demand points — pending and assigned orders' restaurant locations
    demand_points: List[tuple[float, float]] = []
    for order in orders:
        if order.status in (OrderStatus.PENDING, OrderStatus.ASSIGNED):
            demand_points.append((order.restaurant_lat, order.restaurant_lng))

    # Also add customer locations for picked-up orders (represents active demand area)
    for order in orders:
        if order.status == OrderStatus.PICKED_UP:
            demand_points.append((order.customer_lat, order.customer_lng))

    idle_riders = [r for r in riders if r.status == RiderStatus.IDLE]

    if not demand_points:
        # No demand at all — riders hold position
        return

    for rider in idle_riders:
        # --- Attraction toward demand ---
        attract_lat = 0.0
        attract_lng = 0.0
        attract_count = 0

        for dlat, dlng in demand_points:
            d = _distance(rider.lat, rider.lng, dlat, dlng)
            if d > NUDGE_RADIUS:
                continue
            d = max(d, GRAVITY_MIN_DIST)  # avoid division by zero
            weight = 1.0 / (d * d)
            # Direction toward demand
            dir_lat = (dlat - rider.lat) / d
            dir_lng = (dlng - rider.lng) / d
            attract_lat += weight * dir_lat
            attract_lng += weight * dir_lng
            attract_count += 1

        if attract_count == 0:
            # No nearby demand — hold position
            continue

        # --- Repulsion from other riders ---
        repulse_lat = 0.0
        repulse_lng = 0.0

        for other in riders:
            if other.id == rider.id:
                continue
            d = _distance(rider.lat, rider.lng, other.lat, other.lng)
            if d > REPULSION_RADIUS or d < 1e-8:
                continue
            d = max(d, GRAVITY_MIN_DIST)
            weight = 1.0 / (d * d)
            # Direction AWAY from other rider
            dir_lat = (rider.lat - other.lat) / d
            dir_lng = (rider.lng - other.lng) / d
            repulse_lat += weight * dir_lat
            repulse_lng += weight * dir_lng

        # --- Combine ---
        nudge_lat = attract_lat - REPULSION_FACTOR * repulse_lat
        nudge_lng = attract_lng - REPULSION_FACTOR * repulse_lng

        # Normalize and scale by rider speed
        mag = math.sqrt(nudge_lat ** 2 + nudge_lng ** 2)
        if mag < 1e-8:
            continue

        step_lat = (nudge_lat / mag) * RIDER_SPEED
        step_lng = (nudge_lng / mag) * RIDER_SPEED

        target_lat = rider.lat + step_lat
        target_lng = rider.lng + step_lng

        # Keep within city bounds
        target_lat, target_lng = _clamp_to_city(target_lat, target_lng)

        rider.target_lat = target_lat
        rider.target_lng = target_lng
        rider.status = RiderStatus.REPOSITIONING


def move_repositioning_riders(riders: List[Rider]) -> None:
    """Move repositioning riders one step toward their nudge target."""
    for rider in riders:
        if rider.status != RiderStatus.REPOSITIONING:
            continue
        if rider.target_lat is None or rider.target_lng is None:
            rider.status = RiderStatus.IDLE
            continue

        d = _distance(rider.lat, rider.lng, rider.target_lat, rider.target_lng)
        if d < GRAVITY_MIN_DIST:
            rider.lat = rider.target_lat
            rider.lng = rider.target_lng
            rider.status = RiderStatus.IDLE
            rider.target_lat = None
            rider.target_lng = None
            continue

        dir_lat = (rider.target_lat - rider.lat) / d
        dir_lng = (rider.target_lng - rider.lng) / d
        rider.lat += dir_lat * rider.speed
        rider.lng += dir_lng * rider.speed

        # After moving, mark back as idle (nudge recalculated each tick)
        rider.status = RiderStatus.IDLE
        rider.target_lat = None
        rider.target_lng = None
