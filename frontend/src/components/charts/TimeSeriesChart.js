import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { TrendingUp } from 'lucide-react';

const TimeSeriesChart = ({
  data,
  title,
  dataKey,
  xAxisKey,
  color,
  loading,
  prefix = '',
  suffix = ''
}) => {
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-dark-800 p-3 border border-slate-200 dark:border-dark-700 rounded-lg shadow-lg">
          <p className="font-medium text-slate-900 dark:text-white">
            {payload[0].payload[xAxisKey]}
          </p>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            {prefix}{payload[0].value?.toLocaleString()}{suffix}
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
          <TrendingUp className="h-5 w-5 mr-2 text-cyan-500" />
          {title}
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
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.1} />
            <XAxis
              dataKey={xAxisKey}
              stroke="#64748b"
              style={{ fontSize: '11px' }}
            />
            <YAxis
              stroke="#64748b"
              style={{ fontSize: '11px' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke={color}
              strokeWidth={3}
              dot={{ fill: color, r: 3 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default TimeSeriesChart;
