import React, { useState, useEffect } from 'react';
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
    <div className="min-h-screen">
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

      {/* Modern Footer */}
      <footer className="relative mt-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900"></div>
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-40"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 mb-4">
              <div className="h-px w-12 bg-gradient-to-r from-transparent to-purple-500"></div>
              <p className="text-purple-300 text-sm font-semibold uppercase tracking-wider">
                NYC Taxi Analytics Platform
              </p>
              <div className="h-px w-12 bg-gradient-to-l from-transparent to-purple-500"></div>
            </div>
            <p className="text-slate-400 text-sm">
              Urban Mobility Intelligence Platform © 2024
            </p>
            <p className="text-slate-500 text-xs mt-2">
              Data Source: NYC Taxi & Limousine Commission
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
