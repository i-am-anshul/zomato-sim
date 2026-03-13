import React, { createContext, useContext, useReducer, useEffect, useRef, useCallback } from 'react';
import {
  generateRiders,
  generateNaiveRiders,
  generateRestaurants,
  generateHeatmap,
  generateKpis,
  generateMockTick,
} from '../mockData';

// ── Initial State ──────────────────────────────────────────────
const initialRiders = generateRiders(50);
const initialRestaurants = generateRestaurants(30);

const initialState = {
  tick: 0,
  simTime: '8:00 AM',
  riders: initialRiders,
  naiveRiders: generateNaiveRiders(initialRiders),
  restaurants: initialRestaurants,
  orders: [],
  heatmap: generateHeatmap(),
  kpis: generateKpis(),
  simStatus: 'stopped', // stopped | running | paused
  speed: 1,
  showHeatmap: true,
  showComparison: false,
  wsConnected: false,
};

// ── Reducer ────────────────────────────────────────────────────
function simReducer(state, action) {
  switch (action.type) {
    case 'WS_MESSAGE': {
      const d = action.payload;
      return {
        ...state,
        tick: d.tick ?? state.tick,
        simTime: d.sim_time ?? d.simTime ?? state.simTime,
        riders: d.riders ?? state.riders,
        naiveRiders: d.naive_riders ?? d.naiveRiders ?? state.naiveRiders,
        restaurants: d.restaurants ?? state.restaurants,
        orders: d.orders ?? state.orders,
        heatmap: d.heatmap ?? state.heatmap,
        kpis: d.kpis ?? state.kpis,
      };
    }
    case 'MOCK_TICK': {
      const next = generateMockTick(state);
      return { ...state, ...next };
    }
    case 'SET_STATUS':
      return { ...state, simStatus: action.payload };
    case 'SET_SPEED':
      return { ...state, speed: action.payload };
    case 'TOGGLE_HEATMAP':
      return { ...state, showHeatmap: !state.showHeatmap };
    case 'TOGGLE_COMPARISON':
      return { ...state, showComparison: !state.showComparison };
    case 'SET_WS_CONNECTED':
      return { ...state, wsConnected: action.payload };
    case 'RESET': {
      const freshRiders = generateRiders(50);
      return {
        ...initialState,
        riders: freshRiders,
        naiveRiders: generateNaiveRiders(freshRiders),
        restaurants: generateRestaurants(30),
        heatmap: generateHeatmap(),
        kpis: generateKpis(),
      };
    }
    default:
      return state;
  }
}

// ── Context ────────────────────────────────────────────────────
const SimContext = createContext(null);

export function SimProvider({ children }) {
  const [state, dispatch] = useReducer(simReducer, initialState);
  const wsRef = useRef(null);
  const mockTimerRef = useRef(null);

  // ── WebSocket connection (with backoff) ─────────────────────
  useEffect(() => {
    let ws;
    let reconnectTimer;
    let retryDelay = 2000;
    let disposed = false;

    function connect() {
      if (disposed) return;
      try {
        ws = new WebSocket('ws://localhost:8000/ws');
        wsRef.current = ws;

        ws.onopen = () => {
          retryDelay = 2000; // reset backoff on success
          dispatch({ type: 'SET_WS_CONNECTED', payload: true });
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            dispatch({ type: 'WS_MESSAGE', payload: data });
          } catch {
            // ignore malformed messages
          }
        };

        ws.onclose = () => {
          dispatch({ type: 'SET_WS_CONNECTED', payload: false });
          if (!disposed) {
            reconnectTimer = setTimeout(connect, retryDelay);
            retryDelay = Math.min(retryDelay * 1.5, 30000); // backoff up to 30s
          }
        };

        ws.onerror = () => {
          ws.close();
        };
      } catch {
        dispatch({ type: 'SET_WS_CONNECTED', payload: false });
      }
    }

    connect();

    return () => {
      disposed = true;
      clearTimeout(reconnectTimer);
      if (ws) ws.close();
    };
  }, []);

  // ── Mock tick timer (runs when WS not connected and sim is running) ──
  useEffect(() => {
    if (mockTimerRef.current) {
      clearInterval(mockTimerRef.current);
      mockTimerRef.current = null;
    }

    if (state.simStatus === 'running' && !state.wsConnected) {
      const interval = 1000 / state.speed;
      mockTimerRef.current = setInterval(() => {
        dispatch({ type: 'MOCK_TICK' });
      }, interval);
    }

    return () => {
      if (mockTimerRef.current) {
        clearInterval(mockTimerRef.current);
      }
    };
  }, [state.simStatus, state.speed, state.wsConnected]);

  // ── Actions ──────────────────────────────────────────────────
  const API_BASE = 'http://localhost:8000/api';

  const sendRest = useCallback(async (path, method = 'POST') => {
    try {
      await fetch(`${API_BASE}${path}`, { method });
    } catch {
      // Backend not available — local-only mode
    }
  }, []);

  const start = useCallback(() => {
    dispatch({ type: 'SET_STATUS', payload: 'running' });
    sendRest('/start');
  }, [sendRest]);

  const pause = useCallback(() => {
    dispatch({ type: 'SET_STATUS', payload: 'paused' });
    sendRest('/pause');
  }, [sendRest]);

  const reset = useCallback(() => {
    dispatch({ type: 'RESET' });
    sendRest('/reset');
  }, [sendRest]);

  const setSpeed = useCallback((s) => {
    dispatch({ type: 'SET_SPEED', payload: s });
    sendRest(`/speed/${s}`);
  }, [sendRest]);

  const toggleHeatmap = useCallback(() => {
    dispatch({ type: 'TOGGLE_HEATMAP' });
  }, []);

  const toggleComparison = useCallback(() => {
    dispatch({ type: 'TOGGLE_COMPARISON' });
  }, []);

  const value = {
    state,
    actions: { start, pause, reset, setSpeed, toggleHeatmap, toggleComparison },
  };

  return <SimContext.Provider value={value}>{children}</SimContext.Provider>;
}

export function useSim() {
  const ctx = useContext(SimContext);
  if (!ctx) throw new Error('useSim must be used within SimProvider');
  return ctx;
}
