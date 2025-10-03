"""
Unit tests for custom algorithm implementations.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms import (
    QuickSort, MultiCriteriaFilter, TripGrouper,
    AnomalyDetector, TopKSelector, TripComparator
)


class TestTripComparator(unittest.TestCase):
    """Test trip comparison logic."""
    
    def test_single_criterion_asc(self):
        trip1 = {'fare': 10}
        trip2 = {'fare': 20}
        criteria = [{'field': 'fare', 'order': 'asc'}]
        
        result = TripComparator.compare_trips(trip1, trip2, criteria)
        self.assertEqual(result, -1)
    
    def test_single_criterion_desc(self):
        trip1 = {'fare': 10}
        trip2 = {'fare': 20}
        criteria = [{'field': 'fare', 'order': 'desc'}]
        
        result = TripComparator.compare_trips(trip1, trip2, criteria)
        self.assertEqual(result, 1)
    
    def test_multiple_criteria(self):
        trip1 = {'zone': 1, 'fare': 20}
        trip2 = {'zone': 1, 'fare': 10}
        criteria = [
            {'field': 'zone', 'order': 'asc'},
            {'field': 'fare', 'order': 'desc'}
        ]
        
        result = TripComparator.compare_trips(trip1, trip2, criteria)
        self.assertEqual(result, -1)  # trip1 has higher fare


class TestQuickSort(unittest.TestCase):
    """Test QuickSort implementation."""
    
    def test_sort_single_criterion(self):
        trips = [
            {'id': 1, 'fare': 30},
            {'id': 2, 'fare': 10},
            {'id': 3, 'fare': 20}
        ]
        criteria = [{'field': 'fare', 'order': 'asc'}]
        
        sorted_trips = QuickSort.sort(trips, criteria)
        
        self.assertEqual(sorted_trips[0]['id'], 2)
        self.assertEqual(sorted_trips[1]['id'], 3)
        self.assertEqual(sorted_trips[2]['id'], 1)
    
    def test_sort_multi_criteria(self):
        trips = [
            {'zone': 2, 'fare': 20},
            {'zone': 1, 'fare': 30},
            {'zone': 1, 'fare': 10},
            {'zone': 2, 'fare': 10}
        ]
        criteria = [
            {'field': 'zone', 'order': 'asc'},
            {'field': 'fare', 'order': 'desc'}
        ]
        
        sorted_trips = QuickSort.sort(trips, criteria)
        
        # Zone 1 trips should come first, with higher fare first
        self.assertEqual(sorted_trips[0], {'zone': 1, 'fare': 30})
        self.assertEqual(sorted_trips[1], {'zone': 1, 'fare': 10})
    
    def test_empty_array(self):
        trips = []
        criteria = [{'field': 'fare', 'order': 'asc'}]
        
        sorted_trips = QuickSort.sort(trips, criteria)
        
        self.assertEqual(sorted_trips, [])


class TestMultiCriteriaFilter(unittest.TestCase):
    """Test filtering implementation."""
    
    def test_single_filter_min(self):
        trips = [
            {'fare': 10},
            {'fare': 20},
            {'fare': 30}
        ]
        filters = [{'field': 'fare', 'min': 15}]
        
        result = MultiCriteriaFilter.filter_trips(trips, filters)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['fare'], 20)
    
    def test_single_filter_max(self):
        trips = [
            {'fare': 10},
            {'fare': 20},
            {'fare': 30}
        ]
        filters = [{'field': 'fare', 'max': 25}]
        
        result = MultiCriteriaFilter.filter_trips(trips, filters)
        
        self.assertEqual(len(result), 2)
    
    def test_range_filter(self):
        trips = [
            {'fare': 10},
            {'fare': 20},
            {'fare': 30},
            {'fare': 40}
        ]
        filters = [{'field': 'fare', 'min': 15, 'max': 35}]
        
        result = MultiCriteriaFilter.filter_trips(trips, filters)
        
        self.assertEqual(len(result), 2)
        self.assertIn({'fare': 20}, result)
        self.assertIn({'fare': 30}, result)
    
    def test_multiple_filters(self):
        trips = [
            {'fare': 20, 'distance': 5},
            {'fare': 30, 'distance': 3},
            {'fare': 15, 'distance': 8}
        ]
        filters = [
            {'field': 'fare', 'min': 18},
            {'field': 'distance', 'max': 6}
        ]
        
        result = MultiCriteriaFilter.filter_trips(trips, filters)
        
        self.assertEqual(len(result), 2)
    
    def test_no_filters(self):
        trips = [{'fare': 10}, {'fare': 20}]
        filters = []
        
        result = MultiCriteriaFilter.filter_trips(trips, filters)
        
        self.assertEqual(len(result), 2)


class TestTripGrouper(unittest.TestCase):
    """Test grouping functionality."""
    
    def test_group_by_field(self):
        trips = [
            {'zone': 1, 'fare': 10},
            {'zone': 2, 'fare': 20},
            {'zone': 1, 'fare': 15}
        ]
        
        groups = TripGrouper.group_by_field(trips, 'zone')
        
        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[1]), 2)
        self.assertEqual(len(groups[2]), 1)


class TestAnomalyDetector(unittest.TestCase):
    """Test anomaly detection."""
    
    def test_calculate_mean(self):
        values = [10, 20, 30, 40, 50]
        mean = AnomalyDetector.calculate_mean(values)
        self.assertEqual(mean, 30.0)
    
    def test_calculate_std_dev(self):
        values = [2, 4, 4, 4, 5, 5, 7, 9]
        mean = AnomalyDetector.calculate_mean(values)
        std_dev = AnomalyDetector.calculate_std_dev(values, mean)
        
        # Should be approximately 2.0
        self.assertAlmostEqual(std_dev, 2.0, places=1)
    
    def test_detect_outliers(self):
        trips = [
            {'fare': 10},
            {'fare': 12},
            {'fare': 11},
            {'fare': 100},  # Outlier
            {'fare': 13}
        ]
        
        anomalies = AnomalyDetector.detect_outliers(trips, 'fare', threshold=2.0)
        
        self.assertGreater(len(anomalies), 0)
        self.assertEqual(anomalies[0]['fare'], 100)


class TestTopKSelector(unittest.TestCase):
    """Test top-k selection."""
    
    def test_select_top_k(self):
        trips = [
            {'id': 1, 'fare': 10},
            {'id': 2, 'fare': 50},
            {'id': 3, 'fare': 30},
            {'id': 4, 'fare': 20},
            {'id': 5, 'fare': 40}
        ]
        criteria = {'field': 'fare', 'order': 'desc'}
        
        top_3 = TopKSelector.select_top_k(trips, 3, criteria)
        
        self.assertEqual(len(top_3), 3)
        self.assertEqual(top_3[0]['id'], 2)  # fare: 50
        self.assertEqual(top_3[1]['id'], 5)  # fare: 40
        self.assertEqual(top_3[2]['id'], 3)  # fare: 30


if __name__ == '__main__':
    unittest.main()
