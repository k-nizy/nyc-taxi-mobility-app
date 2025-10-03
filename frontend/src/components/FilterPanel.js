import React from 'react';
import { Filter, RefreshCw } from 'lucide-react';

const FilterPanel = ({ filters, zones, onFilterChange, onApplyFilters, loading }) => {
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

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-8 border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Filter className="h-5 w-5 text-yellow-600" />
          <h2 className="text-xl font-bold text-gray-800">Data Filters</h2>
        </div>
        <button
          onClick={handleReset}
          className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <RefreshCw className="h-4 w-4" />
          <span>Reset</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Start Date
          </label>
          <input
            type="date"
            name="start_date"
            value={filters.start_date}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            End Date
          </label>
          <input
            type="date"
            name="end_date"
            value={filters.end_date}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Min Fare ($)
          </label>
          <input
            type="number"
            name="min_fare"
            value={filters.min_fare}
            onChange={handleInputChange}
            placeholder="0"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Max Fare ($)
          </label>
          <input
            type="number"
            name="max_fare"
            value={filters.max_fare}
            onChange={handleInputChange}
            placeholder="1000"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Min Distance (mi)
          </label>
          <input
            type="number"
            name="min_distance"
            value={filters.min_distance}
            onChange={handleInputChange}
            placeholder="0"
            step="0.1"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Max Distance (mi)
          </label>
          <input
            type="number"
            name="max_distance"
            value={filters.max_distance}
            onChange={handleInputChange}
            placeholder="100"
            step="0.1"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Pickup Zone
          </label>
          <select
            name="pickup_zone_id"
            value={filters.pickup_zone_id}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          >
            <option value="">All Zones</option>
            {zones.map(zone => (
              <option key={zone.zone_id} value={zone.zone_id}>
                {zone.zone_name} ({zone.borough})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Passengers
          </label>
          <select
            name="passenger_count"
            value={filters.passenger_count}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
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

      <button
        onClick={onApplyFilters}
        disabled={loading}
        className="w-full bg-gradient-to-r from-yellow-400 to-yellow-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-yellow-500 hover:to-yellow-700 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Loading...' : 'Apply Filters'}
      </button>
    </div>
  );
};

export default FilterPanel;
