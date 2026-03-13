import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import RiderLayer from './RiderLayer';
import RestaurantLayer from './RestaurantLayer';
import HeatmapLayer from './HeatmapLayer';
import ControlBar from './ControlBar';

const BANGALORE_CENTER = [12.9716, 77.5946];
const DEFAULT_ZOOM = 13;

export default function SimMap() {
  return (
    <div className="relative flex-1">
      <MapContainer
        center={BANGALORE_CENTER}
        zoom={DEFAULT_ZOOM}
        zoomControl={true}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <RiderLayer />
        <RestaurantLayer />
        <HeatmapLayer />
      </MapContainer>
      <ControlBar />
    </div>
  );
}
