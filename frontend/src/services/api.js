/**
 * API service for communicating with Flask backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Get trips with filters
  getTrips: async (params) => {
    const response = await api.get('/api/trips', { params });
    return response.data;
  },

  // Get statistics
  getStatistics: async (params) => {
    const response = await api.get('/api/statistics', { params });
    return response.data;
  },

  // Get zones
  getZones: async () => {
    const response = await api.get('/api/zones');
    return response.data;
  },

  // Get time series data
  getTimeSeries: async (params) => {
    const response = await api.get('/api/time-series', { params });
    return response.data;
  },

  // Get heatmap data
  getHeatmap: async (params) => {
    const response = await api.get('/api/heatmap', { params });
    return response.data;
  },

  // Get anomalies
  getAnomalies: async (params) => {
    const response = await api.get('/api/anomalies', { params });
    return response.data;
  },

  // Get top routes
  getTopRoutes: async (params) => {
    const response = await api.get('/api/top-routes', { params });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;
