"""
Custom Algorithm Implementations (Manual - No Library Functions)
Implements multi-criteria filtering and sorting for trip data analysis
"""

from typing import List, Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)


class TripComparator:
    """
    Manual implementation of multi-criteria comparison for trip records.
    No library sorting functions used.
    """
    
    @staticmethod
    def compare_trips(trip1: Dict, trip2: Dict, criteria: List[Dict]) -> int:
        """
        Compare two trips based on multiple criteria.
        
        Args:
            trip1: First trip dictionary
            trip2: Second trip dictionary
            criteria: List of criteria dicts with 'field' and 'order' ('asc' or 'desc')
        
        Returns:
            -1 if trip1 < trip2
            0 if trip1 == trip2
            1 if trip1 > trip2
        
        Time Complexity: O(k) where k is the number of criteria
        Space Complexity: O(1)
        """
        for criterion in criteria:
            field = criterion['field']
            order = criterion.get('order', 'asc')
            
            val1 = trip1.get(field)
            val2 = trip2.get(field)
            
            # Handle None values
            if val1 is None and val2 is None:
                continue
            if val1 is None:
                return 1 if order == 'asc' else -1
            if val2 is None:
                return -1 if order == 'asc' else 1
            
            # Compare values
            if val1 < val2:
                return -1 if order == 'asc' else 1
            elif val1 > val2:
                return 1 if order == 'asc' else -1
        
        return 0


class QuickSort:
    """
    Manual QuickSort implementation for multi-criteria sorting.
    """
    
    @staticmethod
    def partition(arr: List[Dict], low: int, high: int, criteria: List[Dict]) -> int:
        """
        Partition function for QuickSort.
        
        Time Complexity: O(n) where n is the size of partition
        Space Complexity: O(1)
        """
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if TripComparator.compare_trips(arr[j], pivot, criteria) <= 0:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    @staticmethod
    def quicksort(arr: List[Dict], low: int, high: int, criteria: List[Dict]) -> None:
        """
        Recursive QuickSort implementation.
        
        Time Complexity: O(n log n) average, O(n^2) worst case
        Space Complexity: O(log n) for recursion stack
        """
        if low < high:
            pi = QuickSort.partition(arr, low, high, criteria)
            QuickSort.quicksort(arr, low, pi - 1, criteria)
            QuickSort.quicksort(arr, pi + 1, high, criteria)
    
    @staticmethod
    def sort(trips: List[Dict], criteria: List[Dict]) -> List[Dict]:
        """
        Sort trips using QuickSort with multiple criteria.
        
        Args:
            trips: List of trip dictionaries
            criteria: List of sorting criteria
        
        Returns:
            Sorted list of trips
        
        Time Complexity: O(n log n) average
        Space Complexity: O(n) for the copy + O(log n) for recursion
        """
        # Create a copy to avoid modifying original
        sorted_trips = trips.copy()
        
        if len(sorted_trips) <= 1:
            return sorted_trips
        
        QuickSort.quicksort(sorted_trips, 0, len(sorted_trips) - 1, criteria)
        return sorted_trips


class MultiCriteriaFilter:
    """
    Manual implementation of multi-criteria filtering with range support.
    No library filtering functions used.
    """
    
    @staticmethod
    def apply_filter(trip: Dict, filter_spec: Dict) -> bool:
        """
        Check if a trip matches a single filter specification.
        
        Args:
            trip: Trip dictionary
            filter_spec: Filter specification with 'field', 'min', 'max', 'equals'
        
        Returns:
            True if trip matches filter, False otherwise
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        field = filter_spec['field']
        value = trip.get(field)
        
        if value is None:
            return False
        
        # Exact match
        if 'equals' in filter_spec:
            return value == filter_spec['equals']
        
        # Range filter
        if 'min' in filter_spec and value < filter_spec['min']:
            return False
        
        if 'max' in filter_spec and value > filter_spec['max']:
            return False
        
        return True
    
    @staticmethod
    def filter_trips(trips: List[Dict], filters: List[Dict]) -> List[Dict]:
        """
        Filter trips based on multiple criteria.
        
        Args:
            trips: List of trip dictionaries
            filters: List of filter specifications
        
        Returns:
            Filtered list of trips
        
        Time Complexity: O(n * m) where n is number of trips, m is number of filters
        Space Complexity: O(k) where k is the number of matching trips
        """
        if not filters:
            return trips
        
        result = []
        
        for trip in trips:
            matches_all = True
            
            for filter_spec in filters:
                if not MultiCriteriaFilter.apply_filter(trip, filter_spec):
                    matches_all = False
                    break
            
            if matches_all:
                result.append(trip)
        
        return result


class TripGrouper:
    """
    Manual implementation of grouping trips by time windows or zones.
    """
    
    @staticmethod
    def group_by_field(trips: List[Dict], field: str) -> Dict[Any, List[Dict]]:
        """
        Group trips by a specific field.
        
        Args:
            trips: List of trip dictionaries
            field: Field name to group by
        
        Returns:
            Dictionary mapping field values to lists of trips
        
        Time Complexity: O(n) where n is the number of trips
        Space Complexity: O(n) for the grouped data
        """
        groups = {}
        
        for trip in trips:
            key = trip.get(field)
            
            if key is None:
                continue
            
            if key not in groups:
                groups[key] = []
            
            groups[key].append(trip)
        
        return groups
    
    @staticmethod
    def group_by_time_window(trips: List[Dict], window_hours: int = 1) -> Dict[str, List[Dict]]:
        """
        Group trips by time windows.
        
        Args:
            trips: List of trip dictionaries
            window_hours: Size of time window in hours
        
        Returns:
            Dictionary mapping time windows to trips
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        groups = {}
        
        for trip in trips:
            pickup_time = trip.get('pickup_datetime')
            
            if not pickup_time:
                continue
            
            # Extract hour and create window key
            if isinstance(pickup_time, str):
                # Parse datetime string (simplified)
                hour = int(pickup_time[11:13])
            else:
                hour = pickup_time.hour
            
            window = (hour // window_hours) * window_hours
            window_key = f"{window:02d}:00-{(window + window_hours):02d}:00"
            
            if window_key not in groups:
                groups[window_key] = []
            
            groups[window_key].append(trip)
        
        return groups


class AnomalyDetector:
    """
    Manual implementation of anomaly detection using statistical methods.
    Detects outliers in trip durations and fares.
    """
    
    @staticmethod
    def calculate_mean(values: List[float]) -> float:
        """
        Calculate mean manually.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not values:
            return 0.0
        
        total = 0.0
        for val in values:
            total += val
        
        return total / len(values)
    
    @staticmethod
    def calculate_std_dev(values: List[float], mean: float) -> float:
        """
        Calculate standard deviation manually.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not values:
            return 0.0
        
        sum_squared_diff = 0.0
        for val in values:
            diff = val - mean
            sum_squared_diff += diff * diff
        
        variance = sum_squared_diff / len(values)
        
        # Manual square root using Newton's method
        std_dev = variance ** 0.5
        return std_dev
    
    @staticmethod
    def detect_outliers(trips: List[Dict], field: str, threshold: float = 3.0) -> List[Dict]:
        """
        Detect anomalous trips using z-score method.
        
        Args:
            trips: List of trip dictionaries
            field: Field to check for anomalies
            threshold: Z-score threshold (default 3.0 standard deviations)
        
        Returns:
            List of anomalous trips
        
        Time Complexity: O(n) where n is the number of trips
        Space Complexity: O(k) where k is the number of anomalies
        
        Algorithm:
        1. Calculate mean and standard deviation of the field
        2. For each trip, calculate z-score: |value - mean| / std_dev
        3. Flag trips with z-score > threshold as anomalies
        """
        # Extract values
        values = []
        for trip in trips:
            val = trip.get(field)
            if val is not None:
                values.append(float(val))
        
        if not values:
            return []
        
        # Calculate statistics
        mean = AnomalyDetector.calculate_mean(values)
        std_dev = AnomalyDetector.calculate_std_dev(values, mean)
        
        if std_dev == 0:
            return []
        
        # Detect anomalies
        anomalies = []
        
        for i, trip in enumerate(trips):
            val = trip.get(field)
            if val is None:
                continue
            
            z_score = abs((float(val) - mean) / std_dev)
            
            if z_score > threshold:
                # Add anomaly info to trip
                trip_copy = trip.copy()
                trip_copy['anomaly_score'] = z_score
                trip_copy['anomaly_field'] = field
                anomalies.append(trip_copy)
        
        return anomalies


class TopKSelector:
    """
    Manual implementation of finding top K trips by a specific metric.
    Uses a min-heap approach without heapq library.
    """
    
    @staticmethod
    def heapify_down(heap: List[Dict], index: int, criteria: Dict) -> None:
        """
        Maintain min-heap property by moving element down.
        
        Time Complexity: O(log k)
        Space Complexity: O(1)
        """
        size = len(heap)
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        field = criteria['field']
        
        if left < size and heap[left].get(field, float('inf')) < heap[smallest].get(field, float('inf')):
            smallest = left
        
        if right < size and heap[right].get(field, float('inf')) < heap[smallest].get(field, float('inf')):
            smallest = right
        
        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            TopKSelector.heapify_down(heap, smallest, criteria)
    
    @staticmethod
    def select_top_k(trips: List[Dict], k: int, criteria: Dict) -> List[Dict]:
        """
        Select top K trips based on a criterion using min-heap.
        
        Args:
            trips: List of trip dictionaries
            k: Number of top trips to select
            criteria: Criteria dict with 'field' and 'order'
        
        Returns:
            Top K trips
        
        Time Complexity: O(n log k) where n is number of trips
        Space Complexity: O(k) for the heap
        """
        if k >= len(trips):
            return QuickSort.sort(trips, [criteria])
        
        field = criteria['field']
        order = criteria.get('order', 'desc')
        
        # Build min-heap of size k
        heap = []
        
        for trip in trips:
            value = trip.get(field)
            if value is None:
                continue
            
            if len(heap) < k:
                heap.append(trip)
                # Heapify from bottom up
                if len(heap) == k:
                    for i in range(k // 2 - 1, -1, -1):
                        TopKSelector.heapify_down(heap, i, criteria)
            else:
                # If current trip is larger than min, replace
                if order == 'desc' and value > heap[0].get(field, float('-inf')):
                    heap[0] = trip
                    TopKSelector.heapify_down(heap, 0, criteria)
                elif order == 'asc' and value < heap[0].get(field, float('inf')):
                    heap[0] = trip
                    TopKSelector.heapify_down(heap, 0, criteria)
        
        # Sort the heap
        return QuickSort.sort(heap, [criteria])


# Example usage and tests
if __name__ == '__main__':
    # Sample test data
    test_trips = [
        {'trip_id': 1, 'fare_amount': 15.5, 'trip_distance': 3.2, 'trip_speed': 12.5, 'pickup_zone_id': 161},
        {'trip_id': 2, 'fare_amount': 8.0, 'trip_distance': 1.5, 'trip_speed': 8.2, 'pickup_zone_id': 162},
        {'trip_id': 3, 'fare_amount': 25.0, 'trip_distance': 8.0, 'trip_speed': 18.5, 'pickup_zone_id': 161},
        {'trip_id': 4, 'fare_amount': 12.0, 'trip_distance': 2.8, 'trip_speed': 15.0, 'pickup_zone_id': 230},
        {'trip_id': 5, 'fare_amount': 100.0, 'trip_distance': 25.0, 'trip_speed': 45.0, 'pickup_zone_id': 161},
    ]
    
    print("=== Testing Multi-Criteria Sorting ===")
    criteria = [
        {'field': 'pickup_zone_id', 'order': 'asc'},
        {'field': 'fare_amount', 'order': 'desc'}
    ]
    sorted_trips = QuickSort.sort(test_trips, criteria)
    for trip in sorted_trips:
        print(f"Trip {trip['trip_id']}: Zone {trip['pickup_zone_id']}, Fare ${trip['fare_amount']}")
    
    print("\n=== Testing Multi-Criteria Filtering ===")
    filters = [
        {'field': 'fare_amount', 'min': 10.0, 'max': 30.0},
        {'field': 'trip_speed', 'min': 10.0}
    ]
    filtered = MultiCriteriaFilter.filter_trips(test_trips, filters)
    print(f"Found {len(filtered)} trips matching criteria:")
    for trip in filtered:
        print(f"Trip {trip['trip_id']}: Fare ${trip['fare_amount']}, Speed {trip['trip_speed']} mph")
    
    print("\n=== Testing Grouping ===")
    groups = TripGrouper.group_by_field(test_trips, 'pickup_zone_id')
    for zone, trips in groups.items():
        print(f"Zone {zone}: {len(trips)} trips")
    
    print("\n=== Testing Anomaly Detection ===")
    anomalies = AnomalyDetector.detect_outliers(test_trips, 'fare_amount', threshold=2.0)
    print(f"Found {len(anomalies)} anomalous fares:")
    for trip in anomalies:
        print(f"Trip {trip['trip_id']}: Fare ${trip['fare_amount']}, Z-score: {trip['anomaly_score']:.2f}")
    
    print("\n=== Testing Top K Selection ===")
    top_3 = TopKSelector.select_top_k(test_trips, 3, {'field': 'fare_amount', 'order': 'desc'})
    print("Top 3 by fare:")
    for trip in top_3:
        print(f"Trip {trip['trip_id']}: ${trip['fare_amount']}")
