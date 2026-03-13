"""Dataclasses for simulation entities: Rider, Restaurant, Order, Zone."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RiderStatus(str, Enum):
    IDLE = "idle"
    DELIVERING = "delivering"
    REPOSITIONING = "repositioning"


class OrderStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

@dataclass
class Rider:
    id: int
    lat: float
    lng: float
    status: RiderStatus = RiderStatus.IDLE
    target_lat: Optional[float] = None
    target_lng: Optional[float] = None
    speed: float = 0.0003  # degrees per tick
    current_order_id: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lat": round(self.lat, 6),
            "lng": round(self.lng, 6),
            "status": self.status.value,
        }


@dataclass
class Restaurant:
    id: int
    lat: float
    lng: float
    name: str
    zone_id: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lat": round(self.lat, 6),
            "lng": round(self.lng, 6),
            "name": self.name,
            "zone_id": self.zone_id,
        }


@dataclass
class Order:
    id: int
    restaurant_id: int
    restaurant_lat: float
    restaurant_lng: float
    customer_lat: float
    customer_lng: float
    status: OrderStatus = OrderStatus.PENDING
    assigned_rider_id: Optional[int] = None
    created_tick: int = 0
    assigned_tick: Optional[int] = None
    picked_up_tick: Optional[int] = None
    delivered_tick: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "lat": round(self.customer_lat, 6),
            "lng": round(self.customer_lng, 6),
            "status": self.status.value,
        }


@dataclass
class Zone:
    id: int
    name: str
    center_lat: float
    center_lng: float
    radius: float
    base_order_rate: float

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "center_lat": round(self.center_lat, 6),
            "center_lng": round(self.center_lng, 6),
            "radius": self.radius,
            "base_order_rate": self.base_order_rate,
        }
