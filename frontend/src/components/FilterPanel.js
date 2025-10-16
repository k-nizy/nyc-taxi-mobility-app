import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Grid,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Box,
  Typography,
  Collapse,
  IconButton,
  Chip,
} from '@mui/material';
import {
  Refresh,
  ExpandMore,
  ExpandLess,
} from '@mui/icons-material';

const FilterPanel = ({ filters, zones, onFilterChange, onApplyFilters, loading }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ ...filters, [name]: value });
  };

  const handleReset = () => {
    const resetFilters = {
      start_date: '',
      end_date: '',
      min_fare: '',
      max_fare: '',
      min_distance: '',
      max_distance: '',
      pickup_zone_id: '',
      passenger_count: ''
    };
    onFilterChange(resetFilters);
  };

  const activeFiltersCount = Object.values(filters).filter(v => v !== '').length;

  return (
    <Card 
      sx={{ 
        mb: 3,
        background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Box display="flex" alignItems="center" gap={2}>
            <Box>
              <Typography variant="h6" fontWeight="bold" sx={{ color: '#212121' }}>
                Filters
              </Typography>
              {activeFiltersCount > 0 && (
                <Chip
                  label={`${activeFiltersCount} active`}
                  size="small"
                  sx={{
                    mt: 0.5,
                    background: 'linear-gradient(135deg, #FFC107 0%, #FFD54F 100%)',
                    color: '#212121',
                    fontWeight: 600,
                  }}
                />
              )}
            </Box>
          </Box>
          <Box display="flex" gap={1}>
            <Button
              startIcon={<Refresh />}
              onClick={handleReset}
              size="small"
              variant="outlined"
              sx={{
                borderColor: '#FFC107',
                color: '#FFC107',
                '&:hover': {
                  borderColor: '#FFD54F',
                  backgroundColor: 'rgba(255, 193, 7, 0.1)',
                },
              }}
            >
              Reset
            </Button>
            <IconButton 
              onClick={() => setIsExpanded(!isExpanded)} 
              size="small"
              sx={{
                color: '#FFC107',
                '&:hover': {
                  backgroundColor: 'rgba(255, 193, 7, 0.1)',
                },
              }}
            >
              {isExpanded ? <ExpandLess /> : <ExpandMore />}
            </IconButton>
          </Box>
        </Box>

        <Collapse in={isExpanded}>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                type="date"
                name="start_date"
                label="Start Date"
                value={filters.start_date}
                onChange={handleInputChange}
                InputLabelProps={{ shrink: true }}
                size="small"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                type="date"
                name="end_date"
                label="End Date"
                value={filters.end_date}
                onChange={handleInputChange}
                InputLabelProps={{ shrink: true }}
                size="small"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                type="number"
                name="min_fare"
                label="Min Fare ($)"
                value={filters.min_fare}
                onChange={handleInputChange}
                placeholder="0"
                size="small"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                type="number"
                name="max_fare"
                label="Max Fare ($)"
                value={filters.max_fare}
                onChange={handleInputChange}
                placeholder="1000"
                size="small"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                type="number"
                name="min_distance"
                label="Min Distance (mi)"
                value={filters.min_distance}
                onChange={handleInputChange}
                placeholder="0"
                inputProps={{ step: 0.1 }}
                size="small"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                type="number"
                name="max_distance"
                label="Max Distance (mi)"
                value={filters.max_distance}
                onChange={handleInputChange}
                placeholder="100"
                inputProps={{ step: 0.1 }}
                size="small"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Pickup Zone</InputLabel>
                <Select
                  name="pickup_zone_id"
                  value={filters.pickup_zone_id}
                  onChange={handleInputChange}
                  label="Pickup Zone"
                >
                  <MenuItem value="">All Zones</MenuItem>
                  {zones.map(zone => (
                    <MenuItem key={zone.zone_id} value={zone.zone_id}>
                      {zone.zone_name} ({zone.borough})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Passengers</InputLabel>
                <Select
                  name="passenger_count"
                  value={filters.passenger_count}
                  onChange={handleInputChange}
                  label="Passengers"
                >
                  <MenuItem value="">Any</MenuItem>
                  <MenuItem value="1">1</MenuItem>
                  <MenuItem value="2">2</MenuItem>
                  <MenuItem value="3">3</MenuItem>
                  <MenuItem value="4">4</MenuItem>
                  <MenuItem value="5">5</MenuItem>
                  <MenuItem value="6">6</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Collapse>

        <Button
          variant="contained"
          fullWidth
          onClick={onApplyFilters}
          disabled={loading}
          startIcon={loading ? <Refresh className="animate-spin" /> : null}
          sx={{ 
            mt: 2,
            background: 'linear-gradient(135deg, #FFC107 0%, #FFD54F 100%)',
            color: '#212121',
            fontWeight: 'bold',
            py: 1.5,
            fontSize: '1rem',
            boxShadow: '0 4px 15px rgba(255, 193, 7, 0.3)',
            '&:hover': {
              background: 'linear-gradient(135deg, #FFD54F 0%, #FFC107 100%)',
              boxShadow: '0 6px 20px rgba(255, 193, 7, 0.4)',
            },
            '&:disabled': {
              background: '#e0e0e0',
              color: '#9e9e9e',
            },
          }}
        >
          {loading ? 'Loading...' : 'Apply Filters'}
        </Button>
      </CardContent>
    </Card>
  );
};

export default FilterPanel;
