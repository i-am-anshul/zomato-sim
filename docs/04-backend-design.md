# Backend Design: Rider Repositioning Simulation

## Module Structure

```
src/backend/
├── main.py                 # FastAPI app, startup, CORS
├── config.py               # Simulation parameters
├── api/
│   ├── routes.py           # REST endpoints (start/pause/reset/speed)
│   └── websocket.py        # WS connection manager + broadcast
└── simulation/
    ├── engine.py            # Tick loop, clock, orchestration
    ├── entities.py          # Rider, Restaurant, Order dataclasses
    ├── spawner.py           # Order spawning with zone density
    ├── nudger.py            # Gravity model + repulsion
    └── matcher.py           # Order-to-rider assignment via Redis
```

## Entities

| Entity | Key Fields |
|--------|-----------|
| Rider | id, lat, lng, status (idle/delivering/repositioning), target_lat, target_lng, speed |
| Restaurant | id, lat, lng, name, zone_id |
| Order | id, restaurant_id, customer_lat, customer_lng, status (pending/assigned/picked_up/delivered), assigned_rider_id, created_tick, assigned_tick, delivered_tick |
| Zone | id, center_lat, center_lng, radius, base_order_rate, time_profile |

## Tick Pipeline

```python
async def tick():
    spawn_orders()          # Probabilistic per zone
    match_orders()          # Assign pending orders to nearest idle rider (Redis GEOSEARCH)
    nudge_idle_riders()     # Gravity + repulsion for unassigned riders
    update_positions()      # Move all riders toward their targets
    compute_kpis()          # Aggregate metrics for both strategies
    broadcast_state()       # Send JSON snapshot via WS
```

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| WS | `/ws` | State broadcast every tick |
| POST | `/api/start` | Start sim |
| POST | `/api/pause` | Pause sim |
| POST | `/api/reset` | Reset to initial state |
| POST | `/api/speed/{mult}` | Set speed multiplier (1/5/10) |

## Gravity + Repulsion Model

```
For each idle rider:
  attraction = Σ (order_weight / distance²) × direction_to_order
  repulsion  = Σ (1 / distance²) × direction_away_from_other_riders  (within 500m)
  nudge_vector = attraction - repulsion_factor × repulsion
  rider.target = rider.position + normalize(nudge_vector) × step_size
```

## Redis Usage

- GEOADD: Update rider positions each tick
- GEOADD: Store restaurant positions (once)
- GEOSEARCH: Find nearest idle rider to each pending order (radius query)
- GEOSEARCH: Find nearby demand for each idle rider (for gravity calc)
