"""
NYC Taxi Data Processing Pipeline
Handles data loading, cleaning, validation, and feature engineering
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from models import get_session, Trip, Zone
from sqlalchemy import text
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TaxiDataProcessor:
    """Process and clean NYC Taxi trip data."""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.stats = {
            'total_records': 0,
            'duplicates_removed': 0,
            'missing_values': 0,
            'invalid_timestamps': 0,
            'invalid_coordinates': 0,
            'outliers_removed': 0,
            'final_records': 0
        }
    
    def load_data(self):
        """Load NYC taxi data from CSV or Parquet."""
        logger.info(f"Loading data from {self.data_path}")
        
        try:
            if self.data_path.endswith('.csv'):
                self.df = pd.read_csv(self.data_path)
            elif self.data_path.endswith('.parquet'):
                self.df = pd.read_parquet(self.data_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Parquet.")
            
            self.stats['total_records'] = len(self.df)
            logger.info(f"Loaded {self.stats['total_records']} records")
            logger.info(f"Columns: {list(self.df.columns)}")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def detect_missing_values(self):
        """Detect and log missing values."""
        logger.info("Detecting missing values...")
        
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100
        
        for col in self.df.columns:
            if missing[col] > 0:
                logger.warning(f"Column '{col}': {missing[col]} missing ({missing_percent[col]:.2f}%)")
        
        self.stats['missing_values'] = self.df.isnull().any(axis=1).sum()
    
    def remove_duplicates(self):
        """Remove duplicate records."""
        logger.info("Removing duplicates...")
        
        initial_count = len(self.df)
        
        # Check for exact duplicates
        self.df = self.df.drop_duplicates()
        
        duplicates_removed = initial_count - len(self.df)
        self.stats['duplicates_removed'] = duplicates_removed
        
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate records")
    
    def clean_timestamps(self):
        """Clean and normalize timestamp fields."""
        logger.info("Cleaning timestamps...")
        
        # Convert to datetime
        datetime_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
        
        for col in datetime_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Remove records with invalid timestamps
        invalid_timestamps = self.df['tpep_pickup_datetime'].isnull() | self.df['tpep_dropoff_datetime'].isnull()
        invalid_count = invalid_timestamps.sum()
        
        if invalid_count > 0:
            logger.warning(f"Removing {invalid_count} records with invalid timestamps")
            self.df = self.df[~invalid_timestamps]
            self.stats['invalid_timestamps'] = invalid_count
        
        # Remove records where dropoff is before pickup
        invalid_order = self.df['tpep_dropoff_datetime'] <= self.df['tpep_pickup_datetime']
        invalid_order_count = invalid_order.sum()
        
        if invalid_order_count > 0:
            logger.warning(f"Removing {invalid_order_count} records with dropoff before pickup")
            self.df = self.df[~invalid_order]
            self.stats['invalid_timestamps'] += invalid_order_count
    
    def remove_outliers(self):
        """Remove outliers based on reasonable thresholds."""
        logger.info("Removing outliers...")
        
        initial_count = len(self.df)
        
        # Calculate trip duration in seconds
        self.df['trip_duration_seconds'] = (
            self.df['tpep_dropoff_datetime'] - self.df['tpep_pickup_datetime']
        ).dt.total_seconds()
        
        # Define thresholds
        MAX_TRIP_DURATION = 12 * 3600  # 12 hours
        MIN_TRIP_DURATION = 60  # 1 minute
        MAX_DISTANCE = 100  # miles
        MIN_DISTANCE = 0.1  # miles
        MAX_FARE = 500  # dollars
        MIN_FARE = 2.5  # minimum fare
        MAX_SPEED = 100  # mph (preliminary speed check)
        
        # Calculate preliminary speed
        self.df['prelim_speed'] = (self.df['trip_distance'] / (self.df['trip_duration_seconds'] / 3600)).replace([np.inf, -np.inf], np.nan)
        
        # Apply filters
        valid_duration = (self.df['trip_duration_seconds'] >= MIN_TRIP_DURATION) & \
                        (self.df['trip_duration_seconds'] <= MAX_TRIP_DURATION)
        
        valid_distance = (self.df['trip_distance'] >= MIN_DISTANCE) & \
                        (self.df['trip_distance'] <= MAX_DISTANCE)
        
        valid_fare = (self.df['fare_amount'] >= MIN_FARE) & \
                    (self.df['fare_amount'] <= MAX_FARE)
        
        valid_speed = (self.df['prelim_speed'] <= MAX_SPEED) | self.df['prelim_speed'].isna()
        
        valid_passengers = (self.df['passenger_count'] >= 1) & (self.df['passenger_count'] <= 6)
        
        # Combine all filters
        valid_records = valid_duration & valid_distance & valid_fare & valid_speed & valid_passengers
        
        self.df = self.df[valid_records]
        
        outliers_removed = initial_count - len(self.df)
        self.stats['outliers_removed'] = outliers_removed
        
        logger.info(f"Removed {outliers_removed} outlier records")
    
    def engineer_features(self):
        """Engineer derived features for urban mobility insights."""
        logger.info("Engineering features...")
        
        # Feature 1: Trip speed (mph)
        # Justification: Speed patterns reveal traffic conditions and route efficiency
        self.df['trip_speed'] = (
            self.df['trip_distance'] / (self.df['trip_duration_seconds'] / 3600)
        )
        
        # Feature 2: Fare per kilometer
        # Justification: Identifies pricing efficiency and route profitability
        self.df['fare_per_km'] = self.df['fare_amount'] / (self.df['trip_distance'] * 1.60934)
        
        # Feature 3: Fare per minute
        # Justification: Measures time-based revenue, important for driver economics
        self.df['fare_per_minute'] = self.df['fare_amount'] / (self.df['trip_duration_seconds'] / 60)
        
        # Replace infinite values with NaN
        self.df = self.df.replace([np.inf, -np.inf], np.nan)
        
        # Drop rows with NaN in critical derived features
        critical_features = ['trip_speed', 'fare_per_km', 'fare_per_minute']
        before_drop = len(self.df)
        self.df = self.df.dropna(subset=critical_features)
        after_drop = len(self.df)
        
        if before_drop > after_drop:
            logger.info(f"Dropped {before_drop - after_drop} records with invalid derived features")
        
        logger.info("Feature engineering complete")
        logger.info(f"Average trip speed: {self.df['trip_speed'].mean():.2f} mph")
        logger.info(f"Average fare per km: ${self.df['fare_per_km'].mean():.2f}")
        logger.info(f"Average fare per minute: ${self.df['fare_per_minute'].mean():.2f}")
    
    def normalize_data(self):
        """Normalize and format data for database insertion."""
        logger.info("Normalizing data...")
        
        # Map column names to database schema
        column_mapping = {
            'tpep_pickup_datetime': 'pickup_datetime',
            'tpep_dropoff_datetime': 'dropoff_datetime',
            'PULocationID': 'pickup_zone_id',
            'DOLocationID': 'dropoff_zone_id',
            'payment_type': 'payment_type_id',
            'RatecodeID': 'rate_code_id',
            'passenger_count': 'passenger_count',
            'trip_distance': 'trip_distance',
            'trip_duration_seconds': 'trip_duration',
            'fare_amount': 'fare_amount',
            'extra': 'extra',
            'mta_tax': 'mta_tax',
            'tip_amount': 'tip_amount',
            'tolls_amount': 'tolls_amount',
            'improvement_surcharge': 'improvement_surcharge',
            'total_amount': 'total_amount',
            'trip_speed': 'trip_speed',
            'fare_per_km': 'fare_per_km',
            'fare_per_minute': 'fare_per_minute'
        }
        
        # Select and rename columns
        available_columns = {k: v for k, v in column_mapping.items() if k in self.df.columns}
        self.df = self.df[list(available_columns.keys())].rename(columns=available_columns)
        
        # Fill NaN values with defaults
        self.df['extra'] = self.df.get('extra', 0).fillna(0)
        self.df['mta_tax'] = self.df.get('mta_tax', 0).fillna(0)
        self.df['tip_amount'] = self.df.get('tip_amount', 0).fillna(0)
        self.df['tolls_amount'] = self.df.get('tolls_amount', 0).fillna(0)
        self.df['improvement_surcharge'] = self.df.get('improvement_surcharge', 0).fillna(0)
        
        # Ensure integer types for IDs
        for col in ['pickup_zone_id', 'dropoff_zone_id', 'payment_type_id', 'rate_code_id', 'passenger_count']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(0).astype(int)
        
        self.stats['final_records'] = len(self.df)
        logger.info(f"Normalized {self.stats['final_records']} records for database insertion")
    
    def save_to_database(self, batch_size=10000):
        """Save cleaned data to PostgreSQL database."""
        logger.info("Saving data to database...")
        
        session = get_session()
        
        try:
            total_rows = len(self.df)
            batches = (total_rows // batch_size) + 1
            
            for i in range(batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, total_rows)
                
                batch_df = self.df.iloc[start_idx:end_idx]
                
                # Convert to dict and insert
                records = batch_df.to_dict('records')
                
                for record in records:
                    trip = Trip(**record)
                    session.add(trip)
                
                session.commit()
                logger.info(f"Batch {i+1}/{batches} inserted ({end_idx}/{total_rows} records)")
            
            logger.info("Data successfully saved to database!")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving to database: {e}")
            raise
        finally:
            session.close()
    
    def print_summary(self):
        """Print processing summary."""
        logger.info("\n" + "="*50)
        logger.info("DATA PROCESSING SUMMARY")
        logger.info("="*50)
        logger.info(f"Total records loaded: {self.stats['total_records']}")
        logger.info(f"Duplicates removed: {self.stats['duplicates_removed']}")
        logger.info(f"Records with missing values: {self.stats['missing_values']}")
        logger.info(f"Invalid timestamps removed: {self.stats['invalid_timestamps']}")
        logger.info(f"Outliers removed: {self.stats['outliers_removed']}")
        logger.info(f"Final records inserted: {self.stats['final_records']}")
        logger.info(f"Data quality: {(self.stats['final_records']/self.stats['total_records']*100):.2f}%")
        logger.info("="*50 + "\n")
    
    def process_and_save(self):
        """Execute complete processing pipeline."""
        self.load_data()
        self.detect_missing_values()
        self.remove_duplicates()
        self.clean_timestamps()
        self.remove_outliers()
        self.engineer_features()
        self.normalize_data()
        self.print_summary()
        self.save_to_database()


def load_taxi_zones():
    """Load NYC taxi zone data."""
    logger.info("Loading NYC taxi zones...")
    
    # NYC Taxi zones data
    zones_data = [
        {'zone_id': 1, 'borough': 'EWR', 'zone_name': 'Newark Airport', 'service_zone': 'EWR'},
        {'zone_id': 4, 'borough': 'Manhattan', 'zone_name': 'Alphabet City', 'service_zone': 'Yellow Zone'},
        {'zone_id': 12, 'borough': 'Manhattan', 'zone_name': 'Battery Park', 'service_zone': 'Yellow Zone'},
        {'zone_id': 13, 'borough': 'Manhattan', 'zone_name': 'Battery Park City', 'service_zone': 'Yellow Zone'},
        {'zone_id': 43, 'borough': 'Manhattan', 'zone_name': 'Central Park', 'service_zone': 'Yellow Zone'},
        {'zone_id': 45, 'borough': 'Manhattan', 'zone_name': 'Chinatown', 'service_zone': 'Yellow Zone'},
        {'zone_id': 48, 'borough': 'Manhattan', 'zone_name': 'Clinton East', 'service_zone': 'Yellow Zone'},
        {'zone_id': 50, 'borough': 'Manhattan', 'zone_name': 'Clinton West', 'service_zone': 'Yellow Zone'},
        {'zone_id': 68, 'borough': 'Manhattan', 'zone_name': 'East Chelsea', 'service_zone': 'Yellow Zone'},
        {'zone_id': 79, 'borough': 'Manhattan', 'zone_name': 'East Village', 'service_zone': 'Yellow Zone'},
        {'zone_id': 87, 'borough': 'Manhattan', 'zone_name': 'Financial District North', 'service_zone': 'Yellow Zone'},
        {'zone_id': 88, 'borough': 'Manhattan', 'zone_name': 'Financial District South', 'service_zone': 'Yellow Zone'},
        {'zone_id': 90, 'borough': 'Manhattan', 'zone_name': 'Flatiron', 'service_zone': 'Yellow Zone'},
        {'zone_id': 100, 'borough': 'Manhattan', 'zone_name': 'Garment District', 'service_zone': 'Yellow Zone'},
        {'zone_id': 107, 'borough': 'Manhattan', 'zone_name': 'Gramercy', 'service_zone': 'Yellow Zone'},
        {'zone_id': 113, 'borough': 'Manhattan', 'zone_name': 'Greenwich Village North', 'service_zone': 'Yellow Zone'},
        {'zone_id': 114, 'borough': 'Manhattan', 'zone_name': 'Greenwich Village South', 'service_zone': 'Yellow Zone'},
        {'zone_id': 125, 'borough': 'Manhattan', 'zone_name': 'Hamilton Heights', 'service_zone': 'Boro Zone'},
        {'zone_id': 127, 'borough': 'Manhattan', 'zone_name': 'Harlem', 'service_zone': 'Boro Zone'},
        {'zone_id': 128, 'borough': 'Manhattan', 'zone_name': 'Highbridge Park', 'service_zone': 'Boro Zone'},
        {'zone_id': 137, 'borough': 'Queens', 'zone_name': 'JFK Airport', 'service_zone': 'Airports'},
        {'zone_id': 140, 'borough': 'Manhattan', 'zone_name': 'Kips Bay', 'service_zone': 'Yellow Zone'},
        {'zone_id': 141, 'borough': 'Manhattan', 'zone_name': 'Lenox Hill East', 'service_zone': 'Yellow Zone'},
        {'zone_id': 142, 'borough': 'Manhattan', 'zone_name': 'Lenox Hill West', 'service_zone': 'Yellow Zone'},
        {'zone_id': 143, 'borough': 'Manhattan', 'zone_name': 'Lincoln Square East', 'service_zone': 'Yellow Zone'},
        {'zone_id': 144, 'borough': 'Manhattan', 'zone_name': 'Lincoln Square West', 'service_zone': 'Yellow Zone'},
        {'zone_id': 148, 'borough': 'Manhattan', 'zone_name': 'Little Italy/NoLiTa', 'service_zone': 'Yellow Zone'},
        {'zone_id': 151, 'borough': 'Manhattan', 'zone_name': 'Lower East Side', 'service_zone': 'Yellow Zone'},
        {'zone_id': 152, 'borough': 'Queens', 'zone_name': 'Long Island City', 'service_zone': 'Boro Zone'},
        {'zone_id': 153, 'borough': 'Manhattan', 'zone_name': 'Manhattan Valley', 'service_zone': 'Yellow Zone'},
        {'zone_id': 158, 'borough': 'Manhattan', 'zone_name': 'Meatpacking/West Village West', 'service_zone': 'Yellow Zone'},
        {'zone_id': 161, 'borough': 'Manhattan', 'zone_name': 'Midtown Center', 'service_zone': 'Yellow Zone'},
        {'zone_id': 162, 'borough': 'Manhattan', 'zone_name': 'Midtown East', 'service_zone': 'Yellow Zone'},
        {'zone_id': 163, 'borough': 'Manhattan', 'zone_name': 'Midtown North', 'service_zone': 'Yellow Zone'},
        {'zone_id': 164, 'borough': 'Manhattan', 'zone_name': 'Midtown South', 'service_zone': 'Yellow Zone'},
        {'zone_id': 166, 'borough': 'Manhattan', 'zone_name': 'Morningside Heights', 'service_zone': 'Boro Zone'},
        {'zone_id': 170, 'borough': 'Manhattan', 'zone_name': 'Murray Hill', 'service_zone': 'Yellow Zone'},
        {'zone_id': 186, 'borough': 'Manhattan', 'zone_name': 'Penn Station/Madison Sq West', 'service_zone': 'Yellow Zone'},
        {'zone_id': 194, 'borough': 'Manhattan', 'zone_name': 'Randalls Island', 'service_zone': 'Yellow Zone'},
        {'zone_id': 202, 'borough': 'Manhattan', 'zone_name': 'Seaport', 'service_zone': 'Yellow Zone'},
        {'zone_id': 209, 'borough': 'Manhattan', 'zone_name': 'SoHo', 'service_zone': 'Yellow Zone'},
        {'zone_id': 211, 'borough': 'Manhattan', 'zone_name': 'Stuy Town/Peter Cooper Village', 'service_zone': 'Yellow Zone'},
        {'zone_id': 224, 'borough': 'Manhattan', 'zone_name': 'Times Sq/Theatre District', 'service_zone': 'Yellow Zone'},
        {'zone_id': 229, 'borough': 'Manhattan', 'zone_name': 'Tribeca/Civic Center', 'service_zone': 'Yellow Zone'},
        {'zone_id': 230, 'borough': 'Manhattan', 'zone_name': 'Two Bridges/Seward Park', 'service_zone': 'Yellow Zone'},
        {'zone_id': 231, 'borough': 'Manhattan', 'zone_name': 'UN/Turtle Bay South', 'service_zone': 'Yellow Zone'},
        {'zone_id': 232, 'borough': 'Manhattan', 'zone_name': 'Union Sq', 'service_zone': 'Yellow Zone'},
        {'zone_id': 233, 'borough': 'Manhattan', 'zone_name': 'Upper East Side North', 'service_zone': 'Yellow Zone'},
        {'zone_id': 234, 'borough': 'Manhattan', 'zone_name': 'Upper East Side South', 'service_zone': 'Yellow Zone'},
        {'zone_id': 236, 'borough': 'Manhattan', 'zone_name': 'Upper West Side North', 'service_zone': 'Yellow Zone'},
        {'zone_id': 237, 'borough': 'Manhattan', 'zone_name': 'Upper West Side South', 'service_zone': 'Yellow Zone'},
        {'zone_id': 238, 'borough': 'Manhattan', 'zone_name': 'Washington Heights North', 'service_zone': 'Boro Zone'},
        {'zone_id': 239, 'borough': 'Manhattan', 'zone_name': 'Washington Heights South', 'service_zone': 'Boro Zone'},
        {'zone_id': 243, 'borough': 'Manhattan', 'zone_name': 'West Chelsea/Hudson Yards', 'service_zone': 'Yellow Zone'},
        {'zone_id': 244, 'borough': 'Manhattan', 'zone_name': 'West Village', 'service_zone': 'Yellow Zone'},
        {'zone_id': 246, 'borough': 'Manhattan', 'zone_name': 'World Trade Center', 'service_zone': 'Yellow Zone'},
        {'zone_id': 249, 'borough': 'Manhattan', 'zone_name': 'Yorkville East', 'service_zone': 'Yellow Zone'},
        {'zone_id': 250, 'borough': 'Manhattan', 'zone_name': 'Yorkville West', 'service_zone': 'Yellow Zone'},
        {'zone_id': 261, 'borough': 'Brooklyn', 'zone_name': 'Williamsburg', 'service_zone': 'Boro Zone'},
        {'zone_id': 262, 'borough': 'Brooklyn', 'zone_name': 'Park Slope', 'service_zone': 'Boro Zone'},
        {'zone_id': 263, 'borough': 'Unknown', 'zone_name': 'Unknown', 'service_zone': 'N/A'},
    ]
    
    session = get_session()
    
    try:
        # Check if zones already loaded
        if session.query(Zone).count() == 0:
            for zone_data in zones_data:
                zone = Zone(**zone_data)
                session.add(zone)
            session.commit()
            logger.info(f"Loaded {len(zones_data)} taxi zones")
        else:
            logger.info("Taxi zones already loaded")
    except Exception as e:
        session.rollback()
        logger.error(f"Error loading zones: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_processor.py <path_to_data_file>")
        print("Example: python data_processor.py data/yellow_tripdata_2023-01.parquet")
        sys.exit(1)
    
    data_file = sys.argv[1]
    
    # Load taxi zones first
    load_taxi_zones()
    
    # Process data
    processor = TaxiDataProcessor(data_file)
    processor.process_and_save()
