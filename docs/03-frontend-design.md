# Frontend Design: Rider Repositioning Simulation

## Design System

| Element | Value |
|---------|-------|
| Styling | Tailwind CSS only |
| Font | System default (sans-serif) |
| Colors | Blue `#2563EB` (riders), Red `#DC2626` (restaurants), Amber `#F59E0B` (nudge), Grey `#6B7280` (UI) |
| Map tiles | OpenStreetMap via react-leaflet v4 |
| Polish | Presentable — clean, readable, not over-designed |

## Component Hierarchy

```
App
├── TopBar (sim clock + title)
├── SimMap (MapContainer)
│   ├── TileLayer
│   ├── RiderLayer (CircleMarkers — nudged + ghost/naive)
│   ├── RestaurantLayer (fixed markers)
│   └── HeatmapLayer (leaflet-heat, 1-2 Hz update)
├── ControlBar (overlay, bottom-center)
│   ├── PlaybackControls (Start/Pause/Reset)
│   ├── SpeedSelector (1x/5x/10x)
│   └── Toggles (heatmap, comparison)
└── KpiPanel (right sidebar)
    ├── MetricCard × 4 (avg pickup, idle %, deliveries, coverage)
    └── ComparisonDelta (nudged vs naive)
```

## State Management

Single `useReducer` + Context. WebSocket `onmessage` dispatches to reducer.

| State | Type | Source |
|-------|------|--------|
| riders[] | array | WS broadcast |
| naiveRiders[] | array | WS broadcast |
| restaurants[] | array | WS broadcast (initial) |
| orders[] | array | WS broadcast |
| kpis | object | WS broadcast |
| simStatus | enum (stopped/running/paused) | local + REST |
| speed | number | local + REST |
| showHeatmap | boolean | local |
| showComparison | boolean | local |

## WebSocket Contract (expected from backend)

```json
{
  "tick": 142,
  "sim_time": "12:34 PM",
  "riders": [{"id": 1, "lat": 12.97, "lng": 77.59, "status": "idle|delivering|repositioning"}],
  "naive_riders": [{"id": 1, "lat": 12.97, "lng": 77.59, "status": "idle|delivering"}],
  "restaurants": [{"id": 1, "lat": 12.96, "lng": 77.58, "name": "..."}],
  "orders": [{"id": 1, "lat": 12.97, "lng": 77.60, "status": "pending|assigned|delivered"}],
  "heatmap": [[12.97, 77.59, 0.8], [12.96, 77.58, 0.5]],
  "kpis": {
    "nudged": {"avg_pickup": 4.2, "idle_pct": 12, "deliveries": 34, "coverage": 88},
    "naive": {"avg_pickup": 7.1, "idle_pct": 31, "deliveries": 22, "coverage": 64}
  }
}
```
