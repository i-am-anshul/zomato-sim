import React from 'react';
import { useSim } from '../context/SimContext';

function MetricCard({ label, nudgedVal, naiveVal, unit, showComparison, lowerIsBetter }) {
  const delta = nudgedVal - naiveVal;
  const pctDelta = naiveVal !== 0 ? ((delta / naiveVal) * 100).toFixed(0) : 0;
  const isImprovement = lowerIsBetter ? delta < 0 : delta > 0;

  return (
    <div className="bg-gray-800 rounded-lg p-3">
      <div className="text-xs text-gray-400 uppercase tracking-wide mb-1">{label}</div>
      <div className="flex items-baseline gap-1">
        <span className="text-xl font-bold text-white">
          {typeof nudgedVal === 'number' ? nudgedVal.toLocaleString() : nudgedVal}
        </span>
        {unit && <span className="text-xs text-gray-400">{unit}</span>}
      </div>
      {showComparison && (
        <div className="mt-2 pt-2 border-t border-gray-700">
          <div className="flex justify-between items-center text-xs">
            <span className="text-gray-500">Naive:</span>
            <span className="text-gray-300">
              {typeof naiveVal === 'number' ? naiveVal.toLocaleString() : naiveVal}
              {unit ? ` ${unit}` : ''}
            </span>
          </div>
          <div className={`text-xs mt-1 font-medium ${isImprovement ? 'text-green-400' : 'text-red-400'}`}>
            {isImprovement ? 'Better' : 'Worse'} by {Math.abs(pctDelta)}%
          </div>
        </div>
      )}
    </div>
  );
}

export default function KpiPanel() {
  const { state } = useSim();
  const { kpis, showComparison, tick, simStatus } = state;

  const nudged = kpis?.nudged || {};
  const naive = kpis?.naive || {};

  return (
    <div className="w-64 bg-gray-900 border-l border-gray-700 flex flex-col shrink-0 overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-700">
        <h2 className="text-sm font-semibold text-gray-200 uppercase tracking-wide">
          KPI Dashboard
        </h2>
        <p className="text-xs text-gray-500 mt-0.5">
          {showComparison ? 'Nudged vs Naive' : 'Nudged Strategy'}
        </p>
      </div>

      {/* Metrics */}
      <div className="flex-1 overflow-y-auto kpi-scroll p-3 space-y-3">
        <MetricCard
          label="Avg Pickup Time"
          nudgedVal={nudged.avg_pickup ?? 0}
          naiveVal={naive.avg_pickup ?? 0}
          unit="min"
          showComparison={showComparison}
          lowerIsBetter={true}
        />
        <MetricCard
          label="Idle Riders"
          nudgedVal={nudged.idle_pct ?? 0}
          naiveVal={naive.idle_pct ?? 0}
          unit="%"
          showComparison={showComparison}
          lowerIsBetter={true}
        />
        <MetricCard
          label="Deliveries"
          nudgedVal={nudged.deliveries ?? 0}
          naiveVal={naive.deliveries ?? 0}
          unit=""
          showComparison={showComparison}
          lowerIsBetter={false}
        />
        <MetricCard
          label="Coverage"
          nudgedVal={nudged.coverage ?? 0}
          naiveVal={naive.coverage ?? 0}
          unit="%"
          showComparison={showComparison}
          lowerIsBetter={false}
        />
      </div>

      {/* Footer legend */}
      <div className="px-4 py-3 border-t border-gray-700 space-y-2">
        <div className="text-xs text-gray-500 uppercase tracking-wide font-medium mb-2">Legend</div>
        <div className="flex items-center gap-2">
          <span className="inline-block w-3 h-3 rounded-full bg-blue-600" />
          <span className="text-xs text-gray-300">Nudged Rider</span>
        </div>
        {showComparison && (
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full border-2 border-blue-600 opacity-40" />
            <span className="text-xs text-gray-300">Naive Rider (ghost)</span>
          </div>
        )}
        <div className="flex items-center gap-2">
          <span className="inline-block w-3 h-3 bg-red-600 rounded-sm" />
          <span className="text-xs text-gray-300">Restaurant</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-block w-5 h-2 rounded-sm bg-gradient-to-r from-green-400 via-yellow-400 to-red-500" />
          <span className="text-xs text-gray-300">Demand Heatmap</span>
        </div>
      </div>
    </div>
  );
}
