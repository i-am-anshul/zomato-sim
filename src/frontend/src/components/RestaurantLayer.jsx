import React from 'react';
import { Marker, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import { useSim } from '../context/SimContext';

// Create a simple red square icon for restaurants using divIcon
const restaurantIcon = L.divIcon({
  className: '', // no default leaflet styles
  html: `<div style="
    width: 14px;
    height: 14px;
    background-color: #DC2626;
    border: 2px solid #991B1B;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4);
  "></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7],
});

export default function RestaurantLayer() {
  const { state } = useSim();

  return state.restaurants.map((r) => (
    <Marker
      key={`rest-${r.id}`}
      position={[r.lat, r.lng]}
      icon={restaurantIcon}
    >
      <Tooltip direction="top" offset={[0, -10]} opacity={0.9}>
        <div className="text-xs">
          <div className="font-semibold">{r.name}</div>
          <div className="text-gray-500">Restaurant #{r.id}</div>
        </div>
      </Tooltip>
    </Marker>
  ));
}
