import React from 'react';
import { useSim } from '../context/SimContext';

export default function ControlBar() {
  const { state, actions } = useSim();
  const { simStatus, speed, showHeatmap, showComparison } = state;

  const buttonBase =
    'px-3 py-1.5 rounded text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500';

  return (
    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-[1000] bg-gray-900/95 backdrop-blur border border-gray-700 rounded-lg px-4 py-3 flex items-center gap-4 shadow-xl">
      {/* Playback Controls */}
      <div className="flex items-center gap-2">
        {simStatus === 'running' ? (
          <button
            onClick={actions.pause}
            className={`${buttonBase} bg-yellow-600 hover:bg-yellow-500 text-white`}
          >
            Pause
          </button>
        ) : (
          <button
            onClick={actions.start}
            className={`${buttonBase} bg-green-600 hover:bg-green-500 text-white`}
          >
            {simStatus === 'paused' ? 'Resume' : 'Start'}
          </button>
        )}
        <button
          onClick={actions.reset}
          className={`${buttonBase} bg-gray-700 hover:bg-gray-600 text-gray-200`}
        >
          Reset
        </button>
      </div>

      {/* Divider */}
      <div className="w-px h-8 bg-gray-600" />

      {/* Speed Selector */}
      <div className="flex items-center gap-1">
        <span className="text-xs text-gray-400 mr-1">Speed:</span>
        {[1, 5, 10].map((s) => (
          <button
            key={s}
            onClick={() => actions.setSpeed(s)}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              speed === s
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            {s}x
          </button>
        ))}
      </div>

      {/* Divider */}
      <div className="w-px h-8 bg-gray-600" />

      {/* Toggles */}
      <div className="flex items-center gap-3">
        <label className="flex items-center gap-1.5 cursor-pointer">
          <input
            type="checkbox"
            checked={showHeatmap}
            onChange={actions.toggleHeatmap}
            className="w-3.5 h-3.5 rounded border-gray-500 text-blue-600 focus:ring-blue-500 bg-gray-700"
          />
          <span className="text-xs text-gray-300">Heatmap</span>
        </label>
        <label className="flex items-center gap-1.5 cursor-pointer">
          <input
            type="checkbox"
            checked={showComparison}
            onChange={actions.toggleComparison}
            className="w-3.5 h-3.5 rounded border-gray-500 text-blue-600 focus:ring-blue-500 bg-gray-700"
          />
          <span className="text-xs text-gray-300">Comparison</span>
        </label>
      </div>
    </div>
  );
}
