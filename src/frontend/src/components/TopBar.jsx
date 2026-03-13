import React from 'react';
import { useSim } from '../context/SimContext';

export default function TopBar() {
  const { state } = useSim();

  const statusColor = {
    stopped: 'bg-gray-500',
    running: 'bg-green-500',
    paused: 'bg-yellow-500',
  }[state.simStatus];

  return (
    <div className="h-12 bg-gray-900 border-b border-gray-700 flex items-center justify-between px-4 shrink-0">
      {/* Left: Clock */}
      <div className="flex items-center gap-3">
        <div className="bg-gray-800 px-3 py-1 rounded text-sm font-mono text-gray-200">
          {state.simTime}
        </div>
        <div className="flex items-center gap-1.5">
          <span className={`inline-block w-2 h-2 rounded-full ${statusColor}`} />
          <span className="text-xs text-gray-400 uppercase tracking-wide">
            {state.simStatus}
          </span>
        </div>
      </div>

      {/* Center: Title */}
      <h1 className="text-sm font-semibold text-gray-100 tracking-wide uppercase">
        Rider Repositioning Simulation
      </h1>

      {/* Right: Connection + Tick */}
      <div className="flex items-center gap-3">
        <span className="text-xs text-gray-500 font-mono">
          Tick #{state.tick}
        </span>
        <div className="flex items-center gap-1.5">
          <span
            className={`inline-block w-2 h-2 rounded-full ${
              state.wsConnected ? 'bg-green-400' : 'bg-red-400'
            }`}
          />
          <span className="text-xs text-gray-400">
            {state.wsConnected ? 'Live' : 'Mock'}
          </span>
        </div>
      </div>
    </div>
  );
}
