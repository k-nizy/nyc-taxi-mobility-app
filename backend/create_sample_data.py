"""
Generate sample/mock data for testing without downloading full dataset.
Useful for development and testing the application flow.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

def generate_sample_data(num_records=10000):
    """
    Generate synthetic NYC taxi trip data for testing.
    
    Args:
        num_records: Number of trip records to generate
    """
    print(f"Generating {num_records} sample trip records...")
    
    # Date range: January 2024
    start_date = datetime(2024, 1, 1)
    
    # Popular NYC taxi zones
    zones = [
        4, 12, 13, 43, 45, 48, 50, 68, 79, 87, 88, 90, 100, 107,
        113, 114, 137, 140, 141, 142, 143, 144, 148, 151, 158,
        161, 162, 163, 164, 170, 186, 224, 229, 230, 231, 232,
        233, 234, 236, 237, 243, 244, 246, 249, 250
    ]
    
    # Generate data
    data = []
    
    for i in range(num_records):
        # Random datetime within January 2024
        days_offset = random.randint(0, 30)
        hour = random.choices(
            range(24),
            weights=[2, 1, 1, 1, 2, 4, 8, 10, 8, 6, 5, 5, 5, 5, 6, 7, 8, 10, 8, 6, 5, 4, 3, 2]
        )[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        pickup_datetime = start_date + timedelta(
            days=days_offset,
            hours=hour,
            minutes=minute,
            seconds=second
        )
        
        # Trip duration: 2-45 minutes
        duration_minutes = random.gauss(15, 8)
        duration_minutes = max(2, min(45, duration_minutes))
        trip_duration = duration_minutes * 60
        
        dropoff_datetime = pickup_datetime + timedelta(seconds=trip_duration)
        
        # Trip distance: 0.5-15 miles
        trip_distance = random.gauss(3.5, 2.5)
        trip_distance = max(0.5, min(15, trip_distance))
        
        # Calculate speed (realistic for NYC)
        avg_speed = (trip_distance / (trip_duration / 3600))
        # Add some variation
        avg_speed = max(3, min(45, avg_speed))
        
        # Fare calculation (simplified NYC formula)
        base_fare = 2.50
        per_mile = 2.50
        per_minute = 0.50
        
        fare_amount = base_fare + (trip_distance * per_mile) + (duration_minutes * per_minute)
        fare_amount = round(fare_amount + random.gauss(0, 2), 2)
        fare_amount = max(2.50, fare_amount)
        
        # Additional charges
        mta_tax = 0.50
        improvement_surcharge = 0.30
        extra = 0.0 if hour < 20 and hour >= 6 else 1.00  # Night surcharge
        
        # Tip (for credit card payments)
        payment_type = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        tip_amount = 0.0
        if payment_type == 1:  # Credit card
            tip_percent = random.gauss(0.18, 0.05)
            tip_percent = max(0.10, min(0.30, tip_percent))
            tip_amount = round(fare_amount * tip_percent, 2)
        
        tolls_amount = 0.0
        if trip_distance > 8:
            tolls_amount = random.choice([0, 5.76, 6.12])
        
        total_amount = fare_amount + extra + mta_tax + tip_amount + tolls_amount + improvement_surcharge
        
        # Rate code (mostly standard)
        rate_code = random.choices([1, 2, 3, 4, 5], weights=[92, 3, 2, 2, 1])[0]
        
        # Passenger count (1-4 typical)
        passenger_count = random.choices([1, 2, 3, 4, 5, 6], weights=[70, 15, 8, 4, 2, 1])[0]
        
        # Zones
        pickup_zone = random.choice(zones)
        dropoff_zone = random.choice(zones)
        
        # Create record
        record = {
            'tpep_pickup_datetime': pickup_datetime,
            'tpep_dropoff_datetime': dropoff_datetime,
            'passenger_count': passenger_count,
            'trip_distance': round(trip_distance, 2),
            'RatecodeID': rate_code,
            'PULocationID': pickup_zone,
            'DOLocationID': dropoff_zone,
            'payment_type': payment_type,
            'fare_amount': fare_amount,
            'extra': extra,
            'mta_tax': mta_tax,
            'tip_amount': tip_amount,
            'tolls_amount': tolls_amount,
            'improvement_surcharge': improvement_surcharge,
            'total_amount': round(total_amount, 2)
        }
        
        data.append(record)
        
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1}/{num_records} records...")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_dir = Path(__file__).parent.parent / 'data'
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'sample_taxi_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Sample data saved to: {output_file}")
    print(f"Records: {len(df)}")
    print(f"\nSample statistics:")
    print(f"  Avg fare: ${df['fare_amount'].mean():.2f}")
    print(f"  Avg distance: {df['trip_distance'].mean():.2f} miles")
    print(f"  Date range: {df['tpep_pickup_datetime'].min()} to {df['tpep_pickup_datetime'].max()}")
    
    return output_file


if __name__ == '__main__':
    import sys
    
    num_records = 10000
    if len(sys.argv) > 1:
        num_records = int(sys.argv[1])
    
    print("Sample Data Generator for NYC Taxi Analytics")
    print("=" * 60)
    output_file = generate_sample_data(num_records)
    
    print("\nTo process this data:")
    print(f"  python data_processor.py {output_file}")
