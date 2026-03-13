import React from 'react';
import { SimProvider } from './context/SimContext';
import TopBar from './components/TopBar';
import SimMap from './components/SimMap';
import KpiPanel from './components/KpiPanel';

export default function App() {
  return (
    <SimProvider>
      <div className="h-screen w-screen flex flex-col bg-gray-900 text-gray-100">
        <TopBar />
        <div className="flex flex-1 overflow-hidden">
          <SimMap />
          <KpiPanel />
        </div>
      </div>
    </SimProvider>
  );
}
