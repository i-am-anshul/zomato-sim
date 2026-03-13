import React from 'react';
import { CircleMarker, Tooltip, useMap } from 'react-leaflet';
import { useEffect, useRef } from 'react';
import L from 'leaflet';
import { useSim } from '../context/SimContext';

const RIDER_COLOR = '#2563EB';

function statusToColor(status) {
  switch (status) {
    case 'idle':
      return '#94A3B8';
    case 'delivering':
      return RIDER_COLOR;
    case 'repositioning':
      return '#F59E0B';
    default:
      return RIDER_COLOR;
  }
}

/** Renders nudged riders as filled circle markers that update positions. */
function NudgedRiders({ riders }) {
  const map = useMap();
  const markersRef = useRef({});

  useEffect(() => {
    const existing = markersRef.current;
    const seen = new Set();

    for (const r of riders) {
      seen.add(r.id);
      if (existing[r.id]) {
        existing[r.id].setLatLng([r.lat, r.lng]);
        existing[r.id].setStyle({
          fillColor: statusToColor(r.status),
        });
      } else {
        const marker = L.circleMarker([r.lat, r.lng], {
          radius: 6,
          fillColor: statusToColor(r.status),
          fillOpacity: 0.9,
          color: RIDER_COLOR,
          weight: 2,
          opacity: 1,
        });
        marker.bindTooltip(`Rider #${r.id}<br/>${r.status}`, {
          direction: 'top',
          offset: [0, -8],
          opacity: 0.9,
          className: 'text-xs',
        });
        marker.addTo(map);
        existing[r.id] = marker;
      }
    }

    // Remove riders no longer in the list
    for (const id of Object.keys(existing)) {
      if (!seen.has(Number(id))) {
        map.removeLayer(existing[id]);
        delete existing[id];
      }
    }
  }, [riders, map]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      for (const marker of Object.values(markersRef.current)) {
        map.removeLayer(marker);
      }
      markersRef.current = {};
    };
  }, [map]);

  return null;
}

/** Renders naive/ghost rider markers — hollow circles, 40% opacity. */
function NaiveRiders({ riders }) {
  const map = useMap();
  const markersRef = useRef({});

  useEffect(() => {
    const existing = markersRef.current;
    const seen = new Set();

    for (const r of riders) {
      seen.add(r.id);
      if (existing[r.id]) {
        existing[r.id].setLatLng([r.lat, r.lng]);
      } else {
        const marker = L.circleMarker([r.lat, r.lng], {
          radius: 6,
          fillColor: 'transparent',
          fillOpacity: 0,
          color: RIDER_COLOR,
          weight: 1.5,
          opacity: 0.4,
          dashArray: '4 3',
        });
        marker.bindTooltip(`Naive #${r.id}<br/>${r.status}`, {
          direction: 'top',
          offset: [0, -8],
          opacity: 0.9,
          className: 'text-xs',
        });
        marker.addTo(map);
        existing[r.id] = marker;
      }
    }

    for (const id of Object.keys(existing)) {
      if (!seen.has(Number(id))) {
        map.removeLayer(existing[id]);
        delete existing[id];
      }
    }
  }, [riders, map]);

  useEffect(() => {
    return () => {
      for (const marker of Object.values(markersRef.current)) {
        map.removeLayer(marker);
      }
      markersRef.current = {};
    };
  }, [map]);

  return null;
}

export default function RiderLayer() {
  const { state } = useSim();

  return (
    <>
      <NudgedRiders riders={state.riders} />
      {state.showComparison && <NaiveRiders riders={state.naiveRiders} />}
    </>
  );
}
