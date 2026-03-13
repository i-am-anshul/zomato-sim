"""REST endpoints for simulation control."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException

from config import (
    BASE_TICK_INTERVAL,
    CENTER_LAT,
    CENTER_LNG,
    CITY_RADIUS,
    NUM_RIDERS,
    NUM_RESTAURANTS,
    NUDGE_RADIUS,
    REPULSION_FACTOR,
    REPULSION_RADIUS,
    RIDER_SPEED,
    ZONES,
)

if TYPE_CHECKING:
    from simulation.engine import SimulationEngine

router = APIRouter(prefix="/api")

# Will be set in main.py
_engine: "SimulationEngine | None" = None


def set_engine(engine: "SimulationEngine") -> None:
    global _engine
    _engine = engine


def _get_engine() -> "SimulationEngine":
    if _engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return _engine


@router.post("/start")
async def start_simulation():
    engine = _get_engine()
    await engine.start()
    return {"status": "running", "tick": engine.tick}


@router.post("/pause")
async def pause_simulation():
    engine = _get_engine()
    await engine.pause()
    return {"status": "paused", "tick": engine.tick}


@router.post("/reset")
async def reset_simulation():
    engine = _get_engine()
    await engine.reset()
    return {"status": "reset", "tick": 0}


@router.post("/speed/{multiplier}")
async def set_speed(multiplier: int):
    if multiplier not in (1, 2, 5, 10):
        raise HTTPException(status_code=400, detail="Speed must be 1, 2, 5, or 10")
    engine = _get_engine()
    engine.set_speed(multiplier)
    return {"speed": engine.speed_multiplier}


@router.get("/config")
async def get_config():
    engine = _get_engine()
    return {
        "num_riders": NUM_RIDERS,
        "num_restaurants": NUM_RESTAURANTS,
        "center_lat": CENTER_LAT,
        "center_lng": CENTER_LNG,
        "city_radius": CITY_RADIUS,
        "rider_speed": RIDER_SPEED,
        "nudge_radius": NUDGE_RADIUS,
        "repulsion_radius": REPULSION_RADIUS,
        "repulsion_factor": REPULSION_FACTOR,
        "tick_interval": BASE_TICK_INTERVAL,
        "speed": engine.speed_multiplier,
        "running": engine.running,
        "tick": engine.tick,
        "redis_available": engine.redis is not None,
        "zones": [
            {"id": z.id, "name": z.name, "center_lat": z.center_lat, "center_lng": z.center_lng, "radius": z.radius, "base_order_rate": z.base_order_rate}
            for z in ZONES
        ],
    }


@router.get("/snapshot")
async def get_snapshot():
    """Return current simulation state as a single JSON object (same format as WS messages)."""
    engine = _get_engine()
    return engine.snapshot()
