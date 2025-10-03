# API Testing Guide

Comprehensive guide for testing all API endpoints.

## Prerequisites

- Backend server running on `http://localhost:5000`
- Database populated with trip data
- Tools: `curl`, Postman, or browser

## Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "trip_count": 2799000
}
```

## API Root

```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "name": "NYC Taxi Mobility Analytics API",
  "version": "1.0.0",
  "endpoints": {
    "trips": "/api/trips",
    "statistics": "/api/statistics",
    ...
  }
}
```

## 1. Get Trips

### Basic Request
```bash
curl "http://localhost:5000/api/trips?limit=5"
```

### With Filters
```bash
curl "http://localhost:5000/api/trips?start_date=2023-01-01&end_date=2023-01-31&min_fare=10&max_fare=50&limit=10"
```

### With Pagination
```bash
curl "http://localhost:5000/api/trips?limit=100&offset=0"
curl "http://localhost:5000/api/trips?limit=100&offset=100"
```

### Filter by Zone
```bash
curl "http://localhost:5000/api/trips?pickup_zone_id=161&limit=20"
```

### Sort Results
```bash
curl "http://localhost:5000/api/trips?sort_by=fare_amount&sort_order=desc&limit=10"
```

### Expected Response Structure
```json
{
  "trips": [
    {
      "trip_id": 12345,
      "pickup_datetime": "2023-01-15T14:30:00",
      "dropoff_datetime": "2023-01-15T14:45:00",
      "pickup_zone": "Times Sq/Theatre District",
      "dropoff_zone": "Upper East Side South",
      "passenger_count": 1,
      "trip_distance": 2.5,
      "trip_duration": 900.0,
      "fare_amount": 15.50,
      "total_amount": 20.80,
      "trip_speed": 10.0,
      "fare_per_km": 3.85,
      "fare_per_minute": 1.03,
      "payment_type": "Credit card"
    }
  ],
  "total_count": 150000,
  "limit": 10,
  "offset": 0
}
```

## 2. Get Statistics

### Overall Statistics
```bash
curl "http://localhost:5000/api/statistics"
```

Expected response:
```json
{
  "overall": {
    "total_trips": 2799000,
    "avg_fare": 16.50,
    "avg_distance": 3.2,
    "avg_duration": 900.0,
    "avg_speed": 12.8,
    "total_revenue": 46183500.00
  },
  "grouped": []
}
```

### Statistics by Hour
```bash
curl "http://localhost:5000/api/statistics?group_by=hour"
```

### Statistics by Zone
```bash
curl "http://localhost:5000/api/statistics?group_by=zone"
```

### Statistics by Payment Type
```bash
curl "http://localhost:5000/api/statistics?group_by=payment_type"
```

### With Date Filter
```bash
curl "http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-07&group_by=hour"
```

## 3. Get Zones

```bash
curl "http://localhost:5000/api/zones"
```

Expected response:
```json
{
  "zones": [
    {
      "zone_id": 161,
      "zone_name": "Midtown Center",
      "borough": "Manhattan",
      "service_zone": "Yellow Zone"
    },
    ...
  ]
}
```

## 4. Time Series Data

### Hourly Time Series
```bash
curl "http://localhost:5000/api/time-series?interval=hour"
```

Expected response:
```json
{
  "time_series": [
    {
      "hour": 0,
      "trip_count": 45000,
      "avg_fare": 18.20,
      "avg_speed": 15.5,
      "total_revenue": 819000.00
    },
    ...
  ]
}
```

### Daily Time Series
```bash
curl "http://localhost:5000/api/time-series?interval=day&start_date=2023-01-01&end_date=2023-01-31"
```

Expected response includes `date` field instead of `hour`.

## 5. Heatmap Data

```bash
curl "http://localhost:5000/api/heatmap"
```

Expected response:
```json
{
  "pickup": [
    {
      "zone_id": 161,
      "zone_name": "Midtown Center",
      "borough": "Manhattan",
      "count": 145000
    },
    ...
  ],
  "dropoff": [
    {
      "zone_id": 234,
      "zone_name": "Upper East Side South",
      "borough": "Manhattan",
      "count": 128000
    },
    ...
  ]
}
```

### With Date Filter
```bash
curl "http://localhost:5000/api/heatmap?start_date=2023-01-15&end_date=2023-01-15"
```

## 6. Anomalies Detection

### Detect Fare Anomalies
```bash
curl "http://localhost:5000/api/anomalies?field=fare_amount&threshold=3.0&limit=50"
```

Expected response:
```json
{
  "anomalies": [
    {
      "trip_id": 12345,
      "pickup_datetime": "2023-01-15T10:30:00",
      "fare_amount": 450.00,
      "trip_distance": 45.0,
      "anomaly_score": 4.5,
      "anomaly_field": "fare_amount",
      ...
    }
  ],
  "total_anomalies": 120,
  "field": "fare_amount",
  "threshold": 3.0
}
```

### Detect Speed Anomalies
```bash
curl "http://localhost:5000/api/anomalies?field=trip_speed&threshold=2.5"
```

### Detect Duration Anomalies
```bash
curl "http://localhost:5000/api/anomalies?field=trip_duration&threshold=3.0"
```

## 7. Top Routes

```bash
curl "http://localhost:5000/api/top-routes?limit=20"
```

Expected response:
```json
{
  "routes": [
    {
      "pickup_zone": "Times Sq/Theatre District",
      "pickup_zone_id": 224,
      "trip_count": 145000,
      "avg_fare": 15.80,
      "avg_distance": 3.2
    },
    ...
  ]
}
```

## Python Testing Script

Create `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(name, url, params=None):
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response keys: {list(data.keys())}")
        
        if 'trips' in data:
            print(f"  - Trips returned: {len(data['trips'])}")
        if 'overall' in data:
            print(f"  - Total trips: {data['overall'].get('total_trips', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Run tests
print("=" * 60)
print("API Test Suite")
print("=" * 60)

tests = [
    ("Health Check", f"{BASE_URL}/health"),
    ("Get Trips", f"{BASE_URL}/api/trips", {"limit": 5}),
    ("Get Statistics", f"{BASE_URL}/api/statistics"),
    ("Get Zones", f"{BASE_URL}/api/zones"),
    ("Hourly Time Series", f"{BASE_URL}/api/time-series", {"interval": "hour"}),
    ("Heatmap", f"{BASE_URL}/api/heatmap"),
    ("Top Routes", f"{BASE_URL}/api/top-routes", {"limit": 10}),
    ("Anomalies", f"{BASE_URL}/api/anomalies", {"field": "fare_amount"}),
]

results = []
for test in tests:
    result = test_endpoint(*test)
    results.append(result)

print("\n" + "=" * 60)
print(f"Tests Passed: {sum(results)}/{len(results)}")
print("=" * 60)
```

Run with:
```bash
python test_api.py
```

## Postman Collection

Import this JSON into Postman for interactive testing:

```json
{
  "info": {
    "name": "NYC Taxi Analytics API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["health"]
        }
      }
    },
    {
      "name": "Get Trips",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:5000/api/trips?limit=10",
          "protocol": "http",
          "host": ["localhost"],
          "port": "5000",
          "path": ["api", "trips"],
          "query": [
            {"key": "limit", "value": "10"}
          ]
        }
      }
    }
  ]
}
```

## Performance Benchmarking

Test response times:

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5000/api/statistics

# Using curl with timing
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:5000/api/trips?limit=100"
```

Create `curl-format.txt`:
```
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
   time_pretransfer:  %{time_pretransfer}\n
      time_redirect:  %{time_redirect}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
```

## Expected Performance Targets

- Health check: < 50ms
- Get trips (no filters): < 200ms
- Get statistics: < 500ms
- Time series: < 300ms
- Heatmap: < 400ms
- Anomaly detection: < 2000ms (processes 10K records)

## Troubleshooting

### 500 Internal Server Error
- Check backend logs
- Verify database connection
- Ensure data is loaded

### Empty Results
- Verify date ranges match your data
- Check filter parameters
- Confirm database has records

### Slow Responses
- Check database indexes
- Monitor database connection pool
- Consider adding caching

### CORS Errors (from frontend)
- Verify CORS is enabled in Flask
- Check allowed origins configuration
