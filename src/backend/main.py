"""FastAPI application — entry point for the rider repositioning simulation."""

from __future__ import annotations

import sys
import os

# Add the backend directory to the Python path so modules resolve correctly
# when running with `uvicorn main:app` from src/backend/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router as api_router, set_engine
from api.websocket import ConnectionManager
from simulation.engine import SimulationEngine

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
engine = SimulationEngine()
ws_manager = ConnectionManager()


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: initialize engine + wire broadcast. Shutdown: pause + close Redis."""
    await engine.initialize()
    engine._broadcast_fn = ws_manager.broadcast
    set_engine(engine)
    print(f"[sim] Engine initialized. Redis: {'connected' if engine.redis else 'unavailable (brute-force fallback)'}")
    print(f"[sim] {len(engine.restaurants)} restaurants, {len(engine.nudged_riders)} riders ready.")
    yield
    # Shutdown
    await engine.pause()
    if engine.redis:
        await engine.redis.close()
    print("[sim] Shutdown complete.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Rider Repositioning Simulation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for development demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST routes
app.include_router(api_router)


# ---------------------------------------------------------------------------
# WebSocket endpoint
# ---------------------------------------------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    # Send initial state immediately on connect
    try:
        import orjson
        await ws.send_text(orjson.dumps(engine.snapshot()).decode("utf-8"))
    except Exception:
        pass

    try:
        while True:
            # Keep connection alive — we don't expect client messages,
            # but we need to read to detect disconnects.
            await ws.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)
    except Exception:
        ws_manager.disconnect(ws)
