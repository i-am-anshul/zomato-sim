# Architecture: Food Delivery Rider Repositioning Simulation

## Overview

Single-process monolith. FastAPI runs the simulation tick loop + WebSocket broadcast + REST control endpoints in one async process. React SPA served separately by Vite dev server. Redis for spatial queries only.

```
┌─────────────────┐       WebSocket        ┌──────────────────┐
│   React + Vite  │◄──────────────────────►│   FastAPI Server  │
│   (Leaflet Map) │       REST (control)   │                  │
│   Port 5173     │──────────────────────►│   Port 8000      │
└─────────────────┘                        │                  │
                                           │  ┌────────────┐  │
                                           │  │ Tick Loop   │  │
                                           │  │ (asyncio)   │  │
                                           │  └─────┬──────┘  │
                                           │        │         │
                                           │  ┌─────▼──────┐  │
                                           │  │   Redis     │  │
                                           │  │ GEOSEARCH   │  │
                                           │  └────────────┘  │
                                           └──────────────────┘
```

## Module Structure

| Module | Responsibility |
|--------|---------------|
| `simulation/engine.py` | Tick loop, clock, speed control, orchestrates per-tick pipeline |
| `simulation/entities.py` | Rider, Restaurant, Order dataclasses |
| `simulation/spawner.py` | Order spawning with zone-based density profiles |
| `simulation/nudger.py` | Gravity model + repulsion for idle rider repositioning |
| `simulation/matcher.py` | Order-to-nearest-rider assignment via Redis GEOSEARCH |
| `api/websocket.py` | WS connection manager, broadcast with try/except per client |
| `api/routes.py` | REST: POST /start, /pause, /reset, /speed/{multiplier} |
| `config.py` | Sim params (rider count, restaurant count, zone configs, tick rate) |

## Data Flow Per Tick

```
spawn_orders() → match_orders_to_riders() → nudge_idle_riders() → update_positions() → broadcast_state()
```

## Dual Simulation

Run nudged + naive strategies in parallel — two rider arrays, same order sequence. Enables apples-to-apples comparison in the same run.

## API Surface

| Method | Endpoint | Purpose |
|--------|----------|---------|
| WS | `/ws` | Real-time state broadcast (riders, orders, KPIs) |
| POST | `/api/start` | Start simulation |
| POST | `/api/pause` | Pause simulation |
| POST | `/api/reset` | Reset to initial state |
| POST | `/api/speed/{multiplier}` | Set speed (1, 5, 10) |
| GET | `/api/config` | Get current simulation config |

## Key Decisions

- **No database** — all state in Python dicts + Redis geo index
- **No auth** — simulation demo only
- **orjson** for serialization — 10x faster than stdlib, critical at 10x speed
- **Redis for GEOSEARCH only** — not persistence. Fallback: in-memory brute force
- **Heatmap at 1-2 Hz** — not per-tick, to save frontend render budget
