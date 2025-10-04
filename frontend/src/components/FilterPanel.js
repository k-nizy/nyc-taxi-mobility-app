import React, { useState } from 'react';
import { Filter, RefreshCw, ChevronDown, ChevronUp, Sparkles } from 'lucide-react';

const FilterPanel = ({ filters, zones, onFilterChange, onApplyFilters, loading }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ ...filters, [name]: value });
  };

  const handleReset = () => {
    const resetFilters = {
      start_date: '',
      end_date: '',
      min_fare: '',
      max_fare: '',
      min_distance: '',
      max_distance: '',
      pickup_zone_id: '',
      passenger_count: ''
    };
    onFilterChange(resetFilters);
  };

  const activeFiltersCount = Object.values(filters).filter(v => v !== '').length;

  return (
    <div className="glass-card rounded-2xl p-6 mb-8 hover-lift">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-emerald-600 to-green-700 rounded-xl">
            <Filter className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-800">Advanced Filters</h2>
            {activeFiltersCount > 0 && (
              <p className="text-sm text-slate-500 flex items-center gap-1">
                <Sparkles className="h-3 w-3" />
                {activeFiltersCount} filter{activeFiltersCount > 1 ? 's' : ''} active
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-all duration-200"
          >
            <RefreshCw className="h-4 w-4" />
            <span className="font-medium">Reset</span>
          </button>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-slate-100 rounded-xl transition-all duration-200"
          >
            {isExpanded ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Collapsible Filter Grid */}
      {isExpanded && (

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-in">
        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Start Date
          </label>
          <input
            type="date"
            name="start_date"
            value={filters.start_date}
            onChange={handleInputChange}
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all duration-200"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            End Date
          </label>
          <input
            type="date"
            name="end_date"
            value={filters.end_date}
            onChange={handleInputChange}
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all duration-200"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Min Fare ($)
          </label>
          <input
            type="number"
            name="min_fare"
            value={filters.min_fare}
            onChange={handleInputChange}
            placeholder="0"
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all duration-200"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Max Fare ($)
          </label>
          <input
            type="number"
            name="max_fare"
            value={filters.max_fare}
            onChange={handleInputChange}
            placeholder="1000"
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 transition-all duration-200"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Min Distance (mi)
          </label>
          <input
            type="number"
            name="min_distance"
            value={filters.min_distance}
            onChange={handleInputChange}
            placeholder="0"
            step="0.1"
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-200"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Max Distance (mi)
          </label>
          <input
            type="number"
            name="max_distance"
            value={filters.max_distance}
            onChange={handleInputChange}
            placeholder="100"
            step="0.1"
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-200"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Pickup Zone
          </label>
          <select
            name="pickup_zone_id"
            value={filters.pickup_zone_id}
            onChange={handleInputChange}
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all duration-200 cursor-pointer"
          >
            <option value="">All Zones</option>
            {zones.map(zone => (
              <option key={zone.zone_id} value={zone.zone_id}>
                {zone.zone_name} ({zone.borough})
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-semibold text-slate-700">
            Passengers
          </label>
          <select
            name="passenger_count"
            value={filters.passenger_count}
            onChange={handleInputChange}
            className="w-full px-4 py-2.5 bg-white border-2 border-slate-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all duration-200 cursor-pointer"
          >
            <option value="">Any</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
          </select>
        </div>
      </div>
      )}

      {/* Apply Button */}
      <button
        onClick={onApplyFilters}
        disabled={loading}
        className="relative w-full group overflow-hidden bg-gradient-to-r from-emerald-600 via-green-600 to-teal-600 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-teal-600 via-green-600 to-emerald-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <span className="relative flex items-center justify-center gap-2">
          {loading ? (
            <>
              <RefreshCw className="h-5 w-5 animate-spin" />
              Loading...
            </>
          ) : (
            <>
              <Filter className="h-5 w-5" />
              Apply Filters
            </>
          )}
        </span>
      </button>
    </div>
  );
};

export default FilterPanel;
