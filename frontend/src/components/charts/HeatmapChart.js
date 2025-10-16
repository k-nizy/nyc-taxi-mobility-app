import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { MapPin } from 'lucide-react';

const HeatmapChart = ({ data, title, loading }) => {
  const colors = [
    '#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16',
    '#22c55e', '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9'
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-dark-800 p-3 border border-slate-200 dark:border-dark-700 rounded-lg shadow-lg">
          <p className="font-medium text-slate-900 dark:text-white">{payload[0].payload.zone_name}</p>
          <p className="text-sm text-slate-600 dark:text-slate-400">{payload[0].payload.borough}</p>
          <p className="text-sm font-semibold text-cyan-500">
            {payload[0].value?.toLocaleString()} trips
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white dark:bg-dark-800 rounded-xl shadow-sm dark:shadow-dark-950/50 p-6 border border-slate-200 dark:border-dark-700">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center">
          <MapPin className="h-5 w-5 mr-2 text-cyan-500" />
          {title}
        </h3>
      </div>

      {loading ? (
        <div className="h-80 flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500"></div>
        </div>
      ) : data.length === 0 ? (
        <div className="h-80 flex items-center justify-center text-slate-500 dark:text-slate-400">
          No data available
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={data.slice(0, 10)}
            layout="vertical"
            margin={{ left: 100 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.1} />
            <XAxis type="number" stroke="#64748b" style={{ fontSize: '11px' }} />
            <YAxis
              type="category"
              dataKey="zone_name"
              stroke="#64748b"
              style={{ fontSize: '10px' }}
              width={100}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
              {data.slice(0, 10).map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default HeatmapChart;
