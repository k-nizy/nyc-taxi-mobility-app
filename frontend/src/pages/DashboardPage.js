import React, { useState, useEffect, useCallback } from 'react';
import { Box, Grid, Paper } from '@mui/material';
import apiService from '../services/api';
import FilterPanel from '../components/FilterPanel';
import StatsCards from '../components/StatsCardsMUI';
import TimeSeriesChart from '../components/charts/TimeSeriesChart';
import HeatmapChart from '../components/charts/HeatmapChart';
import TopRoutesChart from '../components/charts/TopRoutesChart';

const DashboardPage = () => {
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
  const [timeSeries, setTimeSeries] = useState([]);
  const [heatmap, setHeatmap] = useState({ pickup: [], dropoff: [] });
  const [topRoutes, setTopRoutes] = useState([]);
  const [hourlyStats, setHourlyStats] = useState([]);
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true);
      const [
        timeSeriesData,
        heatmapData,
        routesData,
        hourlyData,
        statsData
      ] = await Promise.all([
        apiService.getTimeSeries({ ...filters, interval: 'day' }),
        apiService.getHeatmap(filters),
        apiService.getTopRoutes({ ...filters, limit: 10 }),
        apiService.getTimeSeries({ ...filters, interval: 'hour' }),
        apiService.getStatistics(filters)
      ]);

      setTimeSeries(timeSeriesData.time_series || []);
      setHeatmap(heatmapData);
      setTopRoutes(routesData.routes || []);
      setHourlyStats(hourlyData.time_series || []);
      setStatistics(statsData.overall);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true);
        const zonesData = await apiService.getZones();
        setZones(zonesData.zones);
        await loadDashboardData();
      } catch (error) {
        console.error('Error loading initial data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    loadInitialData();
  }, [loadDashboardData]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleApplyFilters = async () => {
    loadDashboardData();
  };

  return (
    <Box>
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

      <Box sx={{ mt: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 2 }}>
              <TimeSeriesChart
                data={timeSeries}
                title="Daily Trip Volume"
                dataKey="trip_count"
                xAxisKey="date"
                color="#f59e0b"
                loading={loading}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 2 }}>
              <TimeSeriesChart
                data={timeSeries}
                title="Average Fare Trends"
                dataKey="avg_fare"
                xAxisKey="date"
                color="#10b981"
                loading={loading}
                prefix="$"
              />
            </Paper>
          </Grid>
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 2 }}>
              <TimeSeriesChart
                data={hourlyStats}
                title="Hourly Trip Distribution"
                dataKey="trip_count"
                xAxisKey="hour"
                color="#3b82f6"
                loading={loading}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 2 }}>
              <TimeSeriesChart
                data={hourlyStats}
                title="Average Speed by Hour"
                dataKey="avg_speed"
                xAxisKey="hour"
                color="#8b5cf6"
                loading={loading}
                suffix=" mph"
              />
            </Paper>
          </Grid>
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 2 }}>
              <HeatmapChart
                data={heatmap.pickup}
                title="Top Pickup Locations"
                loading={loading}
              />
            </Paper>
          </Grid>
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 2 }}>
              <HeatmapChart
                data={heatmap.dropoff}
                title="Top Dropoff Locations"
                loading={loading}
              />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <TopRoutesChart data={topRoutes} loading={loading} />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default DashboardPage;
