import React from 'react';
import { Car, DollarSign, Clock, TrendingUp, MapPin, Zap } from 'lucide-react';

const StatCard = ({ icon: Icon, title, value, unit, color, gradient, loading }) => {
  return (
    <div className="group relative">
      {/* Glow effect on hover */}
      <div className={`absolute -inset-0.5 ${gradient} rounded-2xl opacity-0 group-hover:opacity-100 blur transition duration-500`}></div>
      
      <div className="relative glass-card rounded-2xl p-6 hover-lift">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <p className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-2">
              {title}
            </p>
            <div className="flex items-baseline gap-2">
              {loading ? (
                <div className="shimmer h-8 w-32 rounded"></div>
              ) : (
                <>
                  <p className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                    {value}
                  </p>
                  {unit && (
                    <span className="text-lg font-medium text-slate-400">{unit}</span>
                  )}
                </>
              )}
            </div>
          </div>
          
          {/* Icon with gradient background */}
          <div className={`relative ${color} p-4 rounded-xl shadow-lg group-hover:scale-110 transition-transform duration-300`}>
            <div className="absolute inset-0 bg-white/20 rounded-xl"></div>
            <Icon className="relative h-7 w-7 text-white" />
          </div>
        </div>
        
        {/* Progress bar */}
        <div className="mt-4 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div 
            className={`h-full ${gradient} rounded-full transition-all duration-1000 ease-out`}
            style={{ width: loading ? '0%' : '75%' }}
          ></div>
        </div>
      </div>
    </div>
  );
};

const StatsCards = ({ statistics, loading }) => {
  const stats = [
    {
      icon: Car,
      title: 'Total Trips',
      value: statistics?.total_trips?.toLocaleString() || '0',
      color: 'bg-gradient-to-br from-blue-500 to-blue-600',
      gradient: 'bg-gradient-to-r from-blue-400 to-blue-600',
    },
    {
      icon: DollarSign,
      title: 'Average Fare',
      value: `$${statistics?.avg_fare || '0'}`,
      color: 'bg-gradient-to-br from-emerald-500 to-emerald-600',
      gradient: 'bg-gradient-to-r from-emerald-400 to-emerald-600',
    },
    {
      icon: MapPin,
      title: 'Avg Distance',
      value: statistics?.avg_distance || '0',
      unit: 'mi',
      color: 'bg-gradient-to-br from-purple-500 to-purple-600',
      gradient: 'bg-gradient-to-r from-purple-400 to-purple-600',
    },
    {
      icon: Zap,
      title: 'Avg Speed',
      value: statistics?.avg_speed || '0',
      unit: 'mph',
      color: 'bg-gradient-to-br from-amber-500 to-amber-600',
      gradient: 'bg-gradient-to-r from-amber-400 to-amber-600',
    },
    {
      icon: Clock,
      title: 'Avg Duration',
      value: Math.round((statistics?.avg_duration || 0) / 60),
      unit: 'min',
      color: 'bg-gradient-to-br from-rose-500 to-rose-600',
      gradient: 'bg-gradient-to-r from-rose-400 to-rose-600',
    },
    {
      icon: TrendingUp,
      title: 'Total Revenue',
      value: `$${(statistics?.total_revenue || 0).toLocaleString()}`,
      color: 'bg-gradient-to-br from-indigo-500 to-indigo-600',
      gradient: 'bg-gradient-to-r from-indigo-400 to-indigo-600',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      {stats.map((stat, index) => (
        <div 
          key={index} 
          className="fade-in"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          <StatCard {...stat} loading={loading} />
        </div>
      ))}
    </div>
  );
};

export default StatsCards;
