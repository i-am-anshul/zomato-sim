# Scope: Food Delivery Rider Repositioning Simulation

## Problem Statement

Food delivery platforms (Zomato-style) face a rider positioning inefficiency: idle riders sit in low-demand zones while orders pile up in hotspots nearby. This simulation models 3 actors (Restaurant, Customer, Rider) on a real map and demonstrates a **gravity-based nudging algorithm** that repositions idle riders toward high-demand zones. The goal: visually and quantitatively prove that nudging reduces pickup time and idle waste vs. a naive (no-nudge) strategy.

## Functional Requirements

| Feature | Priority | Complexity | Notes |
|---------|----------|------------|-------|
| Leaflet map with real tiles (e.g., Bangalore) | Must | Low | `react-leaflet` v4 + OSM tiles. Zero backend cost. |
| Rider markers (50) moving in real-time | Must | Medium | Use `CircleMarker` or Canvas renderer — not DOM icons (perf). |
| Restaurant markers (30) fixed on map | Must | Low | Square/fork icon, static positions. |
| Order spawn with zone-based density | Must | Medium | Configurable rates per zone. Probabilistic per tick. |
| Heatmap overlay showing order density | Must | Low | `leaflet-heat` plugin. Update at 1-2 Hz, not per-tick. |
| Gravity-model nudging engine | Must | Medium | Weighted center of nearby demand. **Must include repulsion/dispersion** to prevent single-point convergence. |
| Nudged vs Naive toggle/comparison | Must | Medium | Toggle strategy mid-run or show ghost markers for naive. |
| Simulation controls (Start/Pause/Reset) | Must | Low | Standard playback model. |
| Speed control (1x / 5x / 10x) | Must | Low | Adjusts tick interval. Lock changes between ticks. |
| Live KPI panel (3-5 numbers) | Should | Low | Avg pickup time, idle rider %, deliveries/min, coverage score. Essential for quantifying nudge benefit. |
| Density shift over time (lunch/evening profiles) | Should | Low | Time-based demand profiles. Can ship with static zones first. |
| Configurable rider/restaurant count via sliders | Nice | Low | Quick param tweaking. |
| Nudge direction arrows on riders | Nice | Low | Amber animated arrows showing repositioning intent. |

## Non-Functional Requirements

| Requirement | Target | Justification |
|-------------|--------|---------------|
| Tick computation | <50ms at 1x, <10ms at 10x | CTO analysis: gravity + spatial queries for 50 riders ≈ 5-8ms. Fits. |
| WS broadcast latency | <5ms for ~7KB payload | Single-digit clients, local network. |
| Frontend render | 60fps (16ms budget) | Canvas/CircleMarker for 50 riders. Heatmap at 1-2 Hz. |
| End-to-end tick-to-render | <100ms perceived | Server tick → WS → React state → Leaflet update. |
| Max WS connections | Cap at 10 | This is a demo, not production. Prevents accidental flood. |

## Back-of-Envelope Estimates

| Metric | Estimate | Calculation |
|--------|----------|-------------|
| State size per tick | ~7KB JSON | 50 riders × 100B + 30 restaurants × 60B + orders |
| Redis GEOSEARCH calls/tick | 50 | One per rider. ~0.1ms each = 5ms total. |
| Concurrent orders (peak) | 20-40 | Based on spawn rate vs fulfillment rate. |
| Total memory footprint | <10MB | All in-memory, no persistence needed. |
| WS messages/sec at 10x | ~10 | One broadcast per tick. |

## MVP Scope

**In Scope:**
- Single-page Leaflet map centered on a city (Bangalore or similar)
- 50 animated riders, 30 fixed restaurants, order hotspots as heatmap
- Server-side tick-based simulation with gravity nudging
- Nudged vs Naive strategy comparison (toggle + KPI delta)
- Playback controls: Start/Pause/Reset, speed selector
- Live KPI panel: avg pickup time, idle %, deliveries completed
- WebSocket real-time state push from FastAPI to React
- Redis GEOSEARCH for spatial proximity queries

**Out of Scope (for now):**
- Real road-snapping / routing (riders move point-to-point, not along roads)
- Authentication, multi-user, persistence
- Customer-facing UI (customers are abstracted as order spawns)
- ML-based prediction (gravity model only)
- Mobile responsiveness
- Production deployment / scaling

## Primary User Journey

| Step | Action | System Response |
|------|--------|----------------|
| 1 | Open app | Map loads with 30 restaurants, 50 riders at initial positions. Heatmap off. Status: Stopped. |
| 2 | Click **Start** | Tick loop begins. Orders spawn per zone density. Heatmap appears. Riders move. |
| 3 | Observe map | Riders animate toward orders/hotspots. Nudge arrows visible. KPIs update live. |
| 4 | Adjust speed to 5x | Tick rate increases. Animations accelerate. |
| 5 | Toggle **Comparison** | Ghost markers show naive rider positions. KPI panel shows delta (nudged vs naive). |
| 6 | Click **Pause** | All animation freezes. Click riders/restaurants for detail popups. |
| 7 | Read KPI panel | Avg pickup time 40% lower with nudging. Idle rider % down. |
| 8 | Click **Reset** | Returns to initial state for another run. |

## Key Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Gravity convergence** — all riders clump to one point | Demo looks absurd | High | Add repulsion term or zone caps (max N riders per cell). Inspired by ambulance dispatch MEXCLP: position at boundaries, not centers. |
| **Riders on water/buildings** | Visual credibility collapses | Medium | Constrain initial positions and movement to a predefined road-like grid within city bounds. Don't need full routing — just avoid obvious water/park areas. |
| **10x speed tick budget exceeded** | Simulation drifts, UI shows stale state | Medium | Use `orjson` for fast serialization. Send diffs not full state. Heatmap at 1-2 Hz. Profile early. |
| **FastAPI WS has no broadcast primitive** | Disconnected client crashes broadcast loop | High | Maintain `Set[WebSocket]`, wrap each `send` in try/except. Periodic ping/pong for stale detection. |
| **Browser tab backgrounded** | Queued WS messages replay on foreground | Low | Send latest-state snapshots, not event log. Client discards stale frames. |
| **Zero orders period** | Division by zero in gravity calc | Medium | Guard against empty demand. Default to "hold position" when no orders. |

## Alternative Approaches Considered

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Pre-baked JSON timeline** (no backend) | Fastest to build. Identical visual demo. | No interactivity (can't change params). Not a real simulation. | Good fallback if time runs out. Not MVP. |
| **Cellular automata grid** | Simpler math. Fast. Emergent behavior. | Less realistic. Loses per-rider granularity. | Interesting but doesn't showcase Redis/WS. |
| **Auction-based pull** (restaurants bid for riders) | More realistic (Uber Surge model). Emergent. | More complex to implement. Harder to visualize. | Could be v2 enhancement. |
| **deck.gl instead of Leaflet** | GPU-accelerated. Handles thousands of paths smoothly. | Steeper learning curve. Team knows Leaflet. | Consider if Leaflet marker perf is an issue. |
| **In-memory spatial calc instead of Redis** | No Redis dependency. 50 riders = trivial brute force. | Misses the learning/demo value of Redis geo. | Keep Redis — it's the right pattern to demonstrate. |

## Tech Stack

| Component | Technology | Why | Alternative |
|-----------|-----------|-----|-------------|
| Frontend | React + Vite | Fast HMR, zero-config, team familiarity | Next.js (overkill for single-page sim) |
| Map | Leaflet + react-leaflet v4 | Mature, well-documented, free tiles | deck.gl (if perf issues arise) |
| Heatmap | leaflet-heat | Drop-in Leaflet plugin | Custom canvas (unnecessary) |
| Backend | Python FastAPI | Team is Python-first. Native async + WS support. | Django (too heavy for this) |
| Real-time | FastAPI native WebSocket | No extra dependency. Sufficient for <10 clients. | Socket.IO (overkill) |
| Spatial queries | Redis GEOSEARCH (v6.2+) | Demonstrates geo-spatial pattern. Fast radius queries. | In-memory brute force (viable fallback) |
| JSON serialization | orjson | 10x faster than stdlib json. Critical at 10x speed. | stdlib json (too slow at high tick rate) |
| Simulation state | In-memory Python dicts | 50 riders, 30 restaurants. No DB needed. | SQLite (unnecessary) |

## UI Layout (Single Screen)

```
┌──────────────────────────────────────────────────────────┐
│ [Sim Time: 12:34 PM]    RIDER REPOSITION SIM    [Help]   │
├────────────────────────────────────────────┬─────────────┤
│                                            │ KPI PANEL   │
│            LEAFLET MAP                     │ Avg Pickup  │
│         (full remaining area)              │ Idle Riders │
│                                            │ Deliveries  │
│   ┌─────────────┐                         │ Coverage %  │
│   │   LEGEND    │                         │─────────────│
│   └─────────────┘                         │ COMPARISON  │
│                                            │ Nudge delta │
│ ┌──────────────────────────────┐          │             │
│ │ ▶ Start │ ⏸ Pause │ ↺ Reset │          │             │
│ │ Speed: [1x] [5x] [10x]      │          │             │
│ │ ☑ Heatmap  ☑ Comparison      │          │             │
│ └──────────────────────────────┘          │             │
└────────────────────────────────────────────┴─────────────┘
```

## Visual Language

| Element | Style | Color |
|---------|-------|-------|
| Riders (nudged) | Filled circle, 12px | Blue `#2563EB` |
| Riders (naive/ghost) | Hollow circle, 40% opacity | Blue `#2563EB` |
| Riders idle | Pulsing ring | Blue + grey center |
| Riders repositioning | Circle + directional arrow | Blue + amber `#F59E0B` arrow |
| Restaurants | Square marker | Red `#DC2626` |
| Heatmap | Gradient overlay | Green → Yellow → Red |
| Nudge arrows | Animated dashed line | Amber `#F59E0B` |
