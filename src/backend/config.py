"""Simulation configuration — all tunable constants in one place."""

from dataclasses import dataclass, field
from typing import List

# ---------------------------------------------------------------------------
# Grid / geography
# ---------------------------------------------------------------------------
CENTER_LAT = 12.9716
CENTER_LNG = 77.5946
CITY_RADIUS = 0.05  # ~5 km in degrees

# ---------------------------------------------------------------------------
# Simulation sizing
# ---------------------------------------------------------------------------
NUM_RIDERS = 50
NUM_RESTAURANTS = 30

# ---------------------------------------------------------------------------
# Tick timing
# ---------------------------------------------------------------------------
BASE_TICK_INTERVAL = 0.1  # seconds (100 ms → 10 ticks/sec at 1×)

# ---------------------------------------------------------------------------
# Movement
# ---------------------------------------------------------------------------
RIDER_SPEED = 0.0003       # degrees per tick (~30 m)
ARRIVAL_THRESHOLD = 0.0004  # degrees – "close enough" to target

# ---------------------------------------------------------------------------
# Nudge model
# ---------------------------------------------------------------------------
NUDGE_RADIUS = 0.03        # degrees (~3 km) for gravity search
REPULSION_RADIUS = 0.005   # degrees (~500 m)
REPULSION_FACTOR = 0.3
GRAVITY_MIN_DIST = 0.0005  # floor to avoid division-by-zero

# ---------------------------------------------------------------------------
# Zones — Bangalore neighborhoods
# ---------------------------------------------------------------------------

@dataclass
class ZoneConfig:
    id: int
    name: str
    center_lat: float
    center_lng: float
    radius: float           # degrees (~1 km ≈ 0.009)
    base_order_rate: float   # probability per tick of spawning an order


ZONES: List[ZoneConfig] = [
    ZoneConfig(id=1, name="Koramangala",     center_lat=12.9352, center_lng=77.6245, radius=0.012, base_order_rate=0.10),
    ZoneConfig(id=2, name="Indiranagar",     center_lat=12.9784, center_lng=77.6408, radius=0.012, base_order_rate=0.10),
    ZoneConfig(id=3, name="MG Road",         center_lat=12.9756, center_lng=77.6068, radius=0.010, base_order_rate=0.06),
    ZoneConfig(id=4, name="Jayanagar",       center_lat=12.9299, center_lng=77.5838, radius=0.011, base_order_rate=0.06),
    ZoneConfig(id=5, name="Whitefield",      center_lat=12.9698, center_lng=77.7500, radius=0.014, base_order_rate=0.03),
    ZoneConfig(id=6, name="Electronic City", center_lat=12.8440, center_lng=77.6630, radius=0.014, base_order_rate=0.03),
]

# ---------------------------------------------------------------------------
# Restaurant names (30 realistic Bangalore eateries)
# ---------------------------------------------------------------------------
RESTAURANT_NAMES: List[str] = [
    # Koramangala (zone 1)
    "Meghana Foods - Koramangala",
    "Truffles - Koramangala",
    "Nandhini Deluxe - Koramangala",
    "Empire Restaurant - Koramangala",
    "Corner House - Koramangala",
    # Indiranagar (zone 2)
    "Toit Brewpub - Indiranagar",
    "Chinita - Indiranagar",
    "Glen's Bakehouse - Indiranagar",
    "Smoke House Deli - Indiranagar",
    "Brahmin's Coffee Bar - Indiranagar",
    # MG Road (zone 3)
    "Koshy's - MG Road",
    "India Coffee House - MG Road",
    "Shivaji Military Hotel - MG Road",
    "The Only Place - MG Road",
    "Ebony - MG Road",
    # Jayanagar (zone 4)
    "Vidyarthi Bhavan - Jayanagar",
    "MTR - Jayanagar",
    "Hotel Janardhan - Jayanagar",
    "Veena Stores - Jayanagar",
    "Kadamba Veg - Jayanagar",
    # Whitefield (zone 5)
    "Windmills Craftworks - Whitefield",
    "Biryani Pot - Whitefield",
    "Magnolia Bakery - Whitefield",
    "Punjab Grill - Whitefield",
    "Hammered - Whitefield",
    # Electronic City (zone 6)
    "Adiga's - Electronic City",
    "Kabab Magic - Electronic City",
    "Domino's - Electronic City",
    "Chai Point - Electronic City",
    "Paradise Biryani - Electronic City",
]

# ---------------------------------------------------------------------------
# Redis
# ---------------------------------------------------------------------------
REDIS_URL = "redis://localhost:6379/0"

# ---------------------------------------------------------------------------
# Sim time
# ---------------------------------------------------------------------------
SIM_START_HOUR = 11  # 11:00 AM
SIM_START_MINUTE = 0
SECONDS_PER_TICK = 6  # each tick = 6 real-world seconds → 1 min every 10 ticks
