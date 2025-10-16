import React from 'react';
import { Grid, Card, CardContent, Typography, Box, CircularProgress, LinearProgress } from '@mui/material';

const StatCard = ({ title, value, unit, loading }) => {
  return (
    <Card 
      sx={{ 
        height: '100%',
        background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-5px)',
          boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
        },
      }}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box flex={1}>
            <Typography 
              variant="caption" 
              color="text.secondary" 
              fontWeight="600" 
              textTransform="uppercase"
              sx={{ letterSpacing: 0.5 }}
            >
              {title}
            </Typography>
            <Box display="flex" alignItems="baseline" gap={1} mt={1}>
              {loading ? (
                <CircularProgress size={24} />
              ) : (
                <>
                  <Typography variant="h4" fontWeight="bold" sx={{ color: '#212121' }}>
                    {value}
                  </Typography>
                  {unit && (
                    <Typography variant="body2" color="text.secondary" fontWeight="500">
                      {unit}
                    </Typography>
                  )}
                </>
              )}
            </Box>
          </Box>
        </Box>
        <LinearProgress
          variant={loading ? 'indeterminate' : 'determinate'}
          value={75}
          sx={{ 
            mt: 2, 
            height: 6, 
            borderRadius: 3,
            backgroundColor: '#e0e0e0',
            '& .MuiLinearProgress-bar': {
              background: 'linear-gradient(90deg, #2196F3 0%, #2196F3dd 100%)',
              borderRadius: 3,
            }
          }}
        />
      </CardContent>
    </Card>
  );
};

const StatsCards = ({ statistics, loading }) => {
  const stats = [
    {
      title: 'Total Trips',
      value: statistics?.total_trips?.toLocaleString() || '0',
    },
    {
      title: 'Average Fare',
      value: `$${statistics?.avg_fare || '0'}`,
    },
    {
      title: 'Avg Distance',
      value: statistics?.avg_distance || '0',
      unit: 'mi',
    },
    {
      title: 'Avg Speed',
      value: statistics?.avg_speed || '0',
      unit: 'mph',
    },
    {
      title: 'Avg Duration',
      value: Math.round((statistics?.avg_duration || 0) / 60),
      unit: 'min',
    },
    {
      title: 'Total Revenue',
      value: `$${(statistics?.total_revenue || 0).toLocaleString()}`,
    },
  ];

  return (
    <Box sx={{ my: 3 }}>
      <Grid container spacing={3}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={index}>
            <StatCard {...stat} loading={loading} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default StatsCards;
