import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import apiService from '../services/api';
import TimeSeriesChart from './charts/TimeSeriesChart';
import HeatmapChart from './charts/HeatmapChart';
import TopRoutesChart from './charts/TopRoutesChart';
import PaymentDistribution from './charts/PaymentDistribution';

/**
 * Dashboard component that displays various data visualizations
 * @param {Object} props - Component props
 * @param {Object} props.filters - Current filter values
 * @param {Array} props.zones - List of available zones
 */
const Dashboard = ({ filters = {}, zones = [] }) => {
  const [timeSeries, setTimeSeries] = useState([]);
  const [heatmap, setHeatmap] = useState({ pickup: [], dropoff: [] });
  const [topRoutes, setTopRoutes] = useState([]);
  const [hourlyStats, setHourlyStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState('');
  
  // Show loading state
  if (loading) {
    return <div>Loading dashboard data...</div>;
  }
  
  // Show error state
  if (error) {
    return <div>Error: {error}</div>;
  }

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
        apiService.getTimeSeries({ ...filters, interval: 'day' })
          .catch(err => {
            console.error('Error loading time series:', err);
            return { time_series: [] };
          }),
        apiService.getHeatmap(filters)
          .catch(err => {
            console.error('Error loading heatmap:', err);
            return { pickup: [], dropoff: [] };
          }),
        apiService.getTopRoutes({ ...filters, limit: 10 })
          .catch(err => {
            console.error('Error loading top routes:', err);
            return { routes: [] };
          }),
        apiService.getTimeSeries({ ...filters, interval: 'hour' })
          .catch(err => {
            console.error('Error loading hourly stats:', err);
            return { time_series: [] };
          })
      ]);

      setTimeSeries(timeSeriesData.time_series || []);
      setHeatmap(heatmapData);
      setTopRoutes(routesData.routes || []);
      setHourlyStats(hourlyData.time_series || []);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (error) {
      console.error('Unexpected error in loadDashboardData:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {lastUpdated && (
        <div className="text-sm text-gray-500">
          Last updated: {lastUpdated}
        </div>
      )}
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

Dashboard.propTypes = {
  /**
   * Filter values for data fetching
   */
  filters: PropTypes.shape({
    dateRange: PropTypes.shape({
      startDate: PropTypes.string,
      endDate: PropTypes.string
    }),
    paymentTypes: PropTypes.arrayOf(PropTypes.string),
    // Add other filter props as needed
  }),
  
  /**
   * List of available zones
   */
  zones: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      // Add other zone props as needed
    })
  )
};

Dashboard.defaultProps = {
  filters: {},
  zones: []
};

export default React.memo(Dashboard);
