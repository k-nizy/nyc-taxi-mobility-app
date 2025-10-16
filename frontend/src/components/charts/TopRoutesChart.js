import React from 'react';
import { Navigation } from 'lucide-react';

const TopRoutesChart = ({ data, loading }) => {
  return (
    <div className="bg-white dark:bg-dark-800 rounded-xl shadow-sm dark:shadow-dark-950/50 p-6 border border-slate-200 dark:border-dark-700">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center">
          <Navigation className="h-5 w-5 mr-2 text-cyan-500" />
          Top Pickup Zones
        </h3>
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500"></div>
        </div>
      ) : data.length === 0 ? (
        <div className="h-64 flex items-center justify-center text-slate-500 dark:text-slate-400">
          No data available
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-slate-200 dark:border-dark-700">
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Rank
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Zone
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Trips
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Avg Fare
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Avg Distance
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-dark-700">
              {data.map((route, index) => (
                <tr
                  key={route.pickup_zone_id}
                  className="hover:bg-slate-50 dark:hover:bg-dark-700/50 transition-colors"
                >
                  <td className="px-4 py-3">
                    <span className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-400 font-semibold text-xs">
                      {index + 1}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm font-medium text-slate-900 dark:text-white">
                    {route.pickup_zone}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400 text-right">
                    {route.trip_count.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400 text-right">
                    ${route.avg_fare}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400 text-right">
                    {route.avg_distance} mi
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TopRoutesChart;
