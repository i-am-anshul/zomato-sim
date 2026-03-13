/**
 * Mock data generator for standalone demo mode.
 * Generates realistic positions around Bangalore center (12.9716, 77.5946).
 */

const BANGALORE_CENTER = { lat: 12.9716, lng: 77.5946 };
const SPREAD = 0.04; // ~4km spread

function randomAround(center, spread) {
  return {
    lat: center.lat + (Math.random() - 0.5) * spread * 2,
    lng: center.lng + (Math.random() - 0.5) * spread * 2,
  };
}

const RESTAURANT_NAMES = [
  'Meghana Foods', 'MTR', 'Vidyarthi Bhavan', 'Toit Brewpub', 'Empire Restaurant',
  'Truffles', 'Nagarjuna', 'Brahmin\'s Coffee Bar', 'CTR', 'Mavalli Tiffin Rooms',
  'Rameshwaram Cafe', 'Third Wave Coffee', 'Koshy\'s', 'Airlines Hotel', 'Shivaji Military Hotel',
  'Veena Stores', 'Corner House', 'Biryani Zone', 'Bowl Company', 'Domino\'s Pizza',
  'Paradise Biryani', 'Behrouz Biryani', 'Burger King', 'KFC', 'McDonald\'s',
  'Subway', 'Pizza Hut', 'Starbucks', 'Chai Point', 'Leon Grill',
];

const STATUS_OPTIONS = ['idle', 'delivering', 'repositioning'];

/** Generate initial set of 30 restaurants (fixed positions). */
export function generateRestaurants(count = 30) {
  return Array.from({ length: count }, (_, i) => {
    const pos = randomAround(BANGALORE_CENTER, SPREAD * 0.8);
    return {
      id: i + 1,
      lat: pos.lat,
      lng: pos.lng,
      name: RESTAURANT_NAMES[i % RESTAURANT_NAMES.length],
    };
  });
}

/** Generate initial set of 50 riders. */
export function generateRiders(count = 50) {
  return Array.from({ length: count }, (_, i) => {
    const pos = randomAround(BANGALORE_CENTER, SPREAD);
    return {
      id: i + 1,
      lat: pos.lat,
      lng: pos.lng,
      status: STATUS_OPTIONS[Math.floor(Math.random() * 3)],
    };
  });
}

/** Generate initial naive riders (same positions, slightly offset). */
export function generateNaiveRiders(riders) {
  return riders.map((r) => ({
    ...r,
    lat: r.lat + (Math.random() - 0.5) * 0.005,
    lng: r.lng + (Math.random() - 0.5) * 0.005,
  }));
}

/** Generate heatmap data points. */
export function generateHeatmap() {
  const points = [];
  // Create a few hotspots
  const hotspots = [
    { lat: 12.975, lng: 77.590, intensity: 0.9 },
    { lat: 12.960, lng: 77.600, intensity: 0.7 },
    { lat: 12.980, lng: 77.580, intensity: 0.8 },
    { lat: 12.965, lng: 77.610, intensity: 0.6 },
    { lat: 12.985, lng: 77.595, intensity: 0.5 },
  ];
  for (const hs of hotspots) {
    for (let i = 0; i < 8; i++) {
      points.push([
        hs.lat + (Math.random() - 0.5) * 0.01,
        hs.lng + (Math.random() - 0.5) * 0.01,
        hs.intensity * (0.5 + Math.random() * 0.5),
      ]);
    }
  }
  return points;
}

/** Generate mock KPI data. */
export function generateKpis() {
  return {
    nudged: {
      avg_pickup: +(3 + Math.random() * 3).toFixed(1),
      idle_pct: Math.round(8 + Math.random() * 10),
      deliveries: Math.round(20 + Math.random() * 30),
      coverage: Math.round(75 + Math.random() * 20),
    },
    naive: {
      avg_pickup: +(6 + Math.random() * 4).toFixed(1),
      idle_pct: Math.round(25 + Math.random() * 15),
      deliveries: Math.round(10 + Math.random() * 20),
      coverage: Math.round(50 + Math.random() * 25),
    },
  };
}

/** Drift a rider to simulate movement — visible on map. */
export function driftRider(rider) {
  const drift = 0.002; // ~200m per tick — visible on map
  return {
    ...rider,
    lat: rider.lat + (Math.random() - 0.5) * drift,
    lng: rider.lng + (Math.random() - 0.5) * drift,
    status: Math.random() > 0.95
      ? STATUS_OPTIONS[Math.floor(Math.random() * 3)]
      : rider.status,
  };
}

/** Generate a full mock tick from previous state. */
export function generateMockTick(prevState) {
  const tick = (prevState.tick || 0) + 1;
  const totalMinutes = tick;
  const hours = 8 + Math.floor(totalMinutes / 60);
  const mins = totalMinutes % 60;
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const displayHour = hours > 12 ? hours - 12 : hours;
  const simTime = `${displayHour}:${String(mins).padStart(2, '0')} ${ampm}`;

  const riders = (prevState.riders || []).map(driftRider);
  const naiveRiders = (prevState.naiveRiders || []).map(driftRider);

  // Slowly shift KPIs
  const prevKpis = prevState.kpis || generateKpis();
  const kpis = {
    nudged: {
      avg_pickup: +Math.max(2, prevKpis.nudged.avg_pickup + (Math.random() - 0.55) * 0.2).toFixed(1),
      idle_pct: Math.max(3, Math.min(30, prevKpis.nudged.idle_pct + Math.round((Math.random() - 0.55) * 2))),
      deliveries: prevKpis.nudged.deliveries + (Math.random() > 0.3 ? 1 : 0),
      coverage: Math.min(99, Math.max(60, prevKpis.nudged.coverage + Math.round((Math.random() - 0.45) * 1))),
    },
    naive: {
      avg_pickup: +Math.max(4, prevKpis.naive.avg_pickup + (Math.random() - 0.45) * 0.2).toFixed(1),
      idle_pct: Math.max(15, Math.min(50, prevKpis.naive.idle_pct + Math.round((Math.random() - 0.45) * 2))),
      deliveries: prevKpis.naive.deliveries + (Math.random() > 0.5 ? 1 : 0),
      coverage: Math.min(90, Math.max(40, prevKpis.naive.coverage + Math.round((Math.random() - 0.55) * 1))),
    },
  };

  return {
    tick,
    simTime,
    riders,
    naiveRiders,
    restaurants: prevState.restaurants,
    heatmap: generateHeatmap(),
    kpis,
  };
}
