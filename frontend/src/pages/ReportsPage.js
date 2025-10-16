import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Download,
  DateRange,
} from '@mui/icons-material';

const ReportCard = ({ title, description, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box display="flex" alignItems="center" mb={2}>
        <Typography variant="h6">{title}</Typography>
      </Box>
      <Typography variant="body2" color="text.secondary" mb={2}>
        {description}
      </Typography>
      <Button
        variant="contained"
        startIcon={<Download />}
        fullWidth
        sx={{ backgroundColor: color }}
      >
        Generate Report
      </Button>
    </CardContent>
  </Card>
);

const ReportsPage = () => {
  const reports = [
    {
      title: 'Monthly Summary',
      description: 'Comprehensive monthly performance report with key metrics and trends',
      color: '#2196F3',
    },
    {
      title: 'Trip Analysis',
      description: 'Detailed analysis of trip patterns, routes, and customer behavior',
      color: '#F44336',
    },
    {
      title: 'Revenue Report',
      description: 'Financial breakdown including revenue, fares, and payment methods',
      color: '#4CAF50',
    },
    {
      title: 'Driver Performance',
      description: 'Individual driver statistics and performance metrics',
      color: '#FF9800',
    },
  ];

  const recentReports = [
    { name: 'October 2025 Summary', date: '2025-10-15', type: 'PDF' },
    { name: 'Q3 Revenue Analysis', date: '2025-10-01', type: 'Excel' },
    { name: 'September Trip Report', date: '2025-09-30', type: 'PDF' },
    { name: 'Driver Performance Q3', date: '2025-09-28', type: 'PDF' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        Reports & Analytics
      </Typography>

      <Grid container spacing={3} mb={4}>
        {reports.map((report, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <ReportCard {...report} />
          </Grid>
        ))}
      </Grid>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Reports
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <List>
            {recentReports.map((report, index) => (
              <ListItem
                key={index}
                secondaryAction={
                  <Button size="small" startIcon={<Download />}>
                    Download
                  </Button>
                }
              >
                <ListItemIcon>
                  <DateRange />
                </ListItemIcon>
                <ListItemText
                  primary={report.name}
                  secondary={`Generated on ${report.date} • ${report.type}`}
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ReportsPage;
