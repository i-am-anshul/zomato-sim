# Rider Repositioning Simulation

A food delivery simulation (Zomato-style) that demonstrates how a gravity-based nudging algorithm repositions idle riders toward high-demand zones to reduce pickup time.

3 actors: **Restaurants** (generate orders), **Customers** (place orders), **Riders** (pick up and deliver). The simulation runs two strategies side-by-side — **nudged** (gravity + repulsion repositioning) vs **naive** (riders stay put when idle) — so you can compare outcomes quantitatively.

## Prerequisites

- **Node.js** >= 18
- **Python** >= 3.10
- **Redis** >= 6.2 (optional — falls back to in-memory brute force if unavailable)

## Setup

### Backend

```bash
cd src/backend
pip install -r requirements.txt
```

### Frontend

```bash
cd src/frontend
npm install
```

## Running

### 1. Start Redis (optional)

```bash
redis-server
```

If Redis isn't running, the backend will log a fallback message and use in-memory spatial queries instead.

### 2. Start the backend

```bash
cd src/backend
python3 -m uvicorn main:app --reload --port 8000
```

### 3. Start the frontend

```bash
cd src/frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

### 4. Use the simulation

1. Click **Start** to begin the simulation
2. Adjust speed with **1x / 5x / 10x** buttons
3. Toggle **Heatmap** to see order density overlay
4. Toggle **Comparison** to see naive rider positions (ghost markers)
5. Watch the **KPI panel** on the right for live metrics

The frontend works standalone with mock data if the backend isn't running.

## Project Structure

```
docs/                          Design documents
src/
├── backend/
│   ├── main.py                FastAPI app entry point
│   ├── config.py              Simulation parameters + zone definitions
│   ├── api/
│   │   ├── routes.py          REST endpoints (start/pause/reset/speed)
│   │   └── websocket.py       WS connection manager + broadcast
│   └── simulation/
│       ├── engine.py          Tick loop + dual simulation orchestration
│       ├── entities.py        Rider, Restaurant, Order, Zone dataclasses
│       ├── spawner.py         Zone-based order spawning
│       ├── matcher.py         Order-to-rider assignment (Redis GEOSEARCH)
│       └── nudger.py          Gravity attraction + repulsion model
└── frontend/
    ├── src/
    │   ├── App.jsx            Layout shell
    │   ├── mockData.js        Mock data for standalone mode
    │   ├── context/
    │   │   └── SimContext.jsx  State management + WS connection
    │   └── components/
    │       ├── SimMap.jsx      Leaflet map container
    │       ├── RiderLayer.jsx  Animated rider markers
    │       ├── RestaurantLayer.jsx
    │       ├── HeatmapLayer.jsx
    │       ├── ControlBar.jsx  Playback + speed + toggles
    │       ├── KpiPanel.jsx    Live metrics sidebar
    │       └── TopBar.jsx      Clock + title
    └── package.json
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| Map | Leaflet + react-leaflet v4 |
| Heatmap | leaflet-heat |
| Backend | Python FastAPI |
| Real-time | WebSocket (FastAPI native) |
| Spatial queries | Redis GEOSEARCH (optional) |
| Serialization | orjson |
