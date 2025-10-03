import React, { useState, useEffect } from 'react';
import { Taxi, BarChart3, Clock, DollarSign, TrendingUp, MapPin } from 'lucide-react';
import apiService from './services/api';
import Dashboard from './components/Dashboard';
import FilterPanel from './components/FilterPanel';
import StatsCards from './components/StatsCards';
import Header from './components/Header';

function App() {
  const [filters, setFilters] = useState({
    start_date: '',
    end_date: '',
    min_fare: '',
    max_fare: '',
    min_distance: '',
    max_distance: '',
    pickup_zone_id: '',
    passenger_count: ''
  });

  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [zones, setZones] = useState([]);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [zonesData, statsData] = await Promise.all([
        apiService.getZones(),
        apiService.getStatistics({})
      ]);
      setZones(zonesData.zones);
      setStatistics(statsData.overall);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleApplyFilters = async () => {
    try {
      setLoading(true);
      const statsData = await apiService.getStatistics(filters);
      setStatistics(statsData.overall);
    } catch (error) {
      console.error('Error applying filters:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <FilterPanel
          filters={filters}
          zones={zones}
          onFilterChange={handleFilterChange}
          onApplyFilters={handleApplyFilters}
          loading={loading}
        />

        {statistics && (
          <StatsCards statistics={statistics} loading={loading} />
        )}

        <Dashboard filters={filters} zones={zones} />
      </main>

      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            NYC Taxi Mobility Analytics Platform © 2024 | Data Source: NYC TLC
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
