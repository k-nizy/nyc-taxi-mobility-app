import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from '@mui/material';
import apiService from '../services/api';

const DriverStatCard = ({ title, value }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box display="flex" alignItems="center" mb={2}>
        <Typography variant="h6" component="div">
          {title}
        </Typography>
      </Box>
      <Typography variant="h4" fontWeight="bold">
        {value}
      </Typography>
    </CardContent>
  </Card>
);

const DriversPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDriverStats();
  }, []);

  const loadDriverStats = async () => {
    try {
      setLoading(true);
      const data = await apiService.getStatistics({});
      setStats(data.overall);
    } catch (error) {
      console.error('Error loading driver stats:', error);
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
        Drivers Overview
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <DriverStatCard
            title="Total Trips"
            value={stats?.total_trips?.toLocaleString() || '0'}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DriverStatCard
            title="Avg Speed"
            value={`${stats?.avg_speed?.toFixed(1) || '0'} mph`}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DriverStatCard
            title="Avg Rating"
            value="4.8"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DriverStatCard
            title="Active Drivers"
            value="1,234"
          />
        </Grid>
      </Grid>

      <Box mt={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Driver Performance Metrics
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Average trip duration: {Math.round((stats?.avg_duration || 0) / 60)} minutes
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Average distance per trip: {stats?.avg_distance?.toFixed(2)} miles
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Average fare per trip: ${stats?.avg_fare?.toFixed(2)}
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default DriversPage;
