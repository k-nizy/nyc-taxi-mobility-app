import React from 'react';
import { Taxi, DollarSign, Clock, TrendingUp, MapPin, Users } from 'lucide-react';

const StatCard = ({ icon: Icon, title, value, unit, color, loading }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">
            {loading ? (
              <span className="animate-pulse">...</span>
            ) : (
              <>
                {value}
                {unit && <span className="text-lg text-gray-500 ml-1">{unit}</span>}
              </>
            )}
          </p>
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );
};

const StatsCards = ({ statistics, loading }) => {
  const stats = [
    {
      icon: Taxi,
      title: 'Total Trips',
      value: statistics?.total_trips?.toLocaleString() || '0',
      color: 'bg-blue-500',
    },
    {
      icon: DollarSign,
      title: 'Average Fare',
      value: `$${statistics?.avg_fare || '0'}`,
      color: 'bg-green-500',
    },
    {
      icon: MapPin,
      title: 'Avg Distance',
      value: statistics?.avg_distance || '0',
      unit: 'mi',
      color: 'bg-purple-500',
    },
    {
      icon: TrendingUp,
      title: 'Avg Speed',
      value: statistics?.avg_speed || '0',
      unit: 'mph',
      color: 'bg-yellow-500',
    },
    {
      icon: Clock,
      title: 'Avg Duration',
      value: Math.round((statistics?.avg_duration || 0) / 60),
      unit: 'min',
      color: 'bg-red-500',
    },
    {
      icon: DollarSign,
      title: 'Total Revenue',
      value: `$${(statistics?.total_revenue || 0).toLocaleString()}`,
      color: 'bg-indigo-500',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} loading={loading} />
      ))}
    </div>
  );
};

export default StatsCards;
