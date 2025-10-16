import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  CircularProgress,
  Chip,
} from '@mui/material';
import apiService from '../services/api';

const TripsPage = () => {
  const [routes, setRoutes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTripsData();
  }, []);

  const loadTripsData = async () => {
    try {
      setLoading(true);
      const data = await apiService.getTopRoutes({ limit: 20 });
      setRoutes(data.routes || []);
    } catch (error) {
      console.error('Error loading trips:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        Trips Overview
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Top Routes
        </Typography>
        
        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Rank</strong></TableCell>
                  <TableCell><strong>Pickup Zone</strong></TableCell>
                  <TableCell><strong>Dropoff Zone</strong></TableCell>
                  <TableCell align="right"><strong>Trip Count</strong></TableCell>
                  <TableCell align="right"><strong>Avg Fare</strong></TableCell>
                  <TableCell align="right"><strong>Avg Distance</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {routes.map((route, index) => (
                  <TableRow key={index} hover>
                    <TableCell>
                      <Chip 
                        label={index + 1} 
                        size="small" 
                        color={index < 3 ? 'primary' : 'default'}
                      />
                    </TableCell>
                    <TableCell>{route.pickup_zone || 'N/A'}</TableCell>
                    <TableCell>{route.dropoff_zone || 'N/A'}</TableCell>
                    <TableCell align="right">{route.trip_count?.toLocaleString()}</TableCell>
                    <TableCell align="right">${route.avg_fare?.toFixed(2)}</TableCell>
                    <TableCell align="right">{route.avg_distance?.toFixed(2)} mi</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
};

export default TripsPage;
