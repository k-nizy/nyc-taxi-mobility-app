import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CircularProgress,
} from '@mui/material';
import apiService from '../services/api';
import TimeSeriesChart from '../components/charts/TimeSeriesChart';

const RevenueCard = ({ title, value, change }) => (
  <Card>
    <CardContent>
      <Box display="flex" justifyContent="space-between" alignItems="flex-start">
        <Box>
          <Typography color="text.secondary" gutterBottom variant="body2">
            {title}
          </Typography>
          <Typography variant="h4" fontWeight="bold">
            {value}
          </Typography>
          {change && (
            <Typography variant="body2" color="success.main" sx={{ mt: 1 }}>
              {change}
            </Typography>
          )}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const RevenuesPage = () => {
  const [stats, setStats] = useState(null);
  const [timeSeries, setTimeSeries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRevenueData();
  }, []);

  const loadRevenueData = async () => {
    try {
      setLoading(true);
      const [statsData, timeSeriesData] = await Promise.all([
        apiService.getStatistics({}),
        apiService.getTimeSeries({ interval: 'day' }),
      ]);
      setStats(statsData.overall);
      setTimeSeries(timeSeriesData.time_series || []);
    } catch (error) {
      console.error('Error loading revenue data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        Revenue Analytics
      </Typography>

      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <RevenueCard
            title="Total Revenue"
            value={`$${(stats?.total_revenue || 0).toLocaleString()}`}
            change="+12.5% from last month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <RevenueCard
            title="Average Fare"
            value={`$${stats?.avg_fare?.toFixed(2) || '0'}`}
            change="+5.2% from last month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <RevenueCard
            title="Revenue per Mile"
            value={`$${((stats?.total_revenue || 0) / (stats?.total_trips || 1) / (stats?.avg_distance || 1)).toFixed(2)}`}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <RevenueCard
            title="Total Trips"
            value={(stats?.total_trips || 0).toLocaleString()}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 2 }}>
            <TimeSeriesChart
              data={timeSeries}
              title="Daily Revenue Trends"
              dataKey="avg_fare"
              xAxisKey="date"
              color="#4CAF50"
              loading={loading}
              prefix="$"
            />
          </Paper>
        </Grid>
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 2 }}>
            <TimeSeriesChart
              data={timeSeries}
              title="Trip Volume Trends"
              dataKey="trip_count"
              xAxisKey="date"
              color="#2196F3"
              loading={loading}
            />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RevenuesPage;
