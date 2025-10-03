import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import TimeSeriesChart from './charts/TimeSeriesChart';
import HeatmapChart from './charts/HeatmapChart';
import TopRoutesChart from './charts/TopRoutesChart';
import PaymentDistribution from './charts/PaymentDistribution';

const Dashboard = ({ filters, zones }) => {
  const [timeSeries, setTimeSeries] = useState([]);
  const [heatmap, setHeatmap] = useState({ pickup: [], dropoff: [] });
  const [topRoutes, setTopRoutes] = useState([]);
  const [hourlyStats, setHourlyStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, [filters]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [
        timeSeriesData,
        heatmapData,
        routesData,
        hourlyData
      ] = await Promise.all([
        apiService.getTimeSeries({ ...filters, interval: 'day' }),
        apiService.getHeatmap(filters),
        apiService.getTopRoutes({ ...filters, limit: 10 }),
        apiService.getTimeSeries({ ...filters, interval: 'hour' })
      ]);

      setTimeSeries(timeSeriesData.time_series || []);
      setHeatmap(heatmapData);
      setTopRoutes(routesData.routes || []);
      setHourlyStats(hourlyData.time_series || []);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Time Series Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <TimeSeriesChart
          data={timeSeries}
          title="Daily Trip Volume"
          dataKey="trip_count"
          xAxisKey="date"
          color="#f59e0b"
          loading={loading}
        />
        <TimeSeriesChart
          data={timeSeries}
          title="Average Fare Trends"
          dataKey="avg_fare"
          xAxisKey="date"
          color="#10b981"
          loading={loading}
          prefix="$"
        />
      </div>

      {/* Hourly Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <TimeSeriesChart
          data={hourlyStats}
          title="Hourly Trip Distribution"
          dataKey="trip_count"
          xAxisKey="hour"
          color="#3b82f6"
          loading={loading}
        />
        <TimeSeriesChart
          data={hourlyStats}
          title="Average Speed by Hour"
          dataKey="avg_speed"
          xAxisKey="hour"
          color="#8b5cf6"
          loading={loading}
          suffix=" mph"
        />
      </div>

      {/* Heatmap and Top Routes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <HeatmapChart
          data={heatmap.pickup}
          title="Top Pickup Locations"
          loading={loading}
        />
        <HeatmapChart
          data={heatmap.dropoff}
          title="Top Dropoff Locations"
          loading={loading}
        />
      </div>

      {/* Top Routes */}
      <TopRoutesChart data={topRoutes} loading={loading} />
    </div>
  );
};

export default Dashboard;
