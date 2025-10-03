import React from 'react';
import { Navigation } from 'lucide-react';

const TopRoutesChart = ({ data, loading }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-gray-800 flex items-center">
          <Navigation className="h-5 w-5 mr-2 text-yellow-600" />
          Top Pickup Zones
        </h3>
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-600"></div>
        </div>
      ) : data.length === 0 ? (
        <div className="h-64 flex items-center justify-center text-gray-500">
          No data available
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Rank
                </th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Zone
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Trips
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Avg Fare
                </th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Avg Distance
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data.map((route, index) => (
                <tr
                  key={route.pickup_zone_id}
                  className="hover:bg-gray-50 transition-colors"
                >
                  <td className="px-4 py-4">
                    <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-yellow-100 text-yellow-800 font-semibold text-sm">
                      {index + 1}
                    </span>
                  </td>
                  <td className="px-4 py-4 text-sm font-medium text-gray-900">
                    {route.pickup_zone}
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-600 text-right">
                    {route.trip_count.toLocaleString()}
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-600 text-right">
                    ${route.avg_fare}
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-600 text-right">
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
