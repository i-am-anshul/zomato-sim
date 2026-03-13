import { useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet.heat';
import { useSim } from '../context/SimContext';

export default function HeatmapLayer() {
  const map = useMap();
  const { state } = useSim();
  const heatLayerRef = useRef(null);
  const lastUpdateRef = useRef(0);

  useEffect(() => {
    if (!state.showHeatmap) {
      // Remove heatmap layer if toggled off
      if (heatLayerRef.current) {
        map.removeLayer(heatLayerRef.current);
        heatLayerRef.current = null;
      }
      return;
    }

    // Throttle updates to ~2 Hz
    const now = Date.now();
    if (now - lastUpdateRef.current < 500 && heatLayerRef.current) {
      return;
    }
    lastUpdateRef.current = now;

    const points = (state.heatmap || []).map(([lat, lng, intensity]) => [
      lat,
      lng,
      intensity,
    ]);

    if (heatLayerRef.current) {
      heatLayerRef.current.setLatLngs(points);
    } else {
      heatLayerRef.current = L.heatLayer(points, {
        radius: 30,
        blur: 20,
        maxZoom: 17,
        max: 1.0,
        gradient: {
          0.2: '#22c55e',  // green
          0.4: '#84cc16',  // lime
          0.6: '#eab308',  // yellow
          0.8: '#f97316',  // orange
          1.0: '#ef4444',  // red
        },
      }).addTo(map);
    }

    return () => {
      // Cleanup on unmount
    };
  }, [state.heatmap, state.showHeatmap, map]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (heatLayerRef.current) {
        map.removeLayer(heatLayerRef.current);
        heatLayerRef.current = null;
      }
    };
  }, [map]);

  return null;
}
