"""
Database initialization script.
Run this to create the database schema and populate lookup tables.

Usage:
    python init_db.py              # Initialize database
    python init_db.py --reset      # Drop and recreate all tables
    python init_db.py --verify     # Verify database setup
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database components
from models import (
    Base, create_db_engine, get_session,
    Zone, PaymentType, RateCode, Trip
)

def check_database_connection():
    """Check if database connection is working."""
    print("\n[1/5] Checking database connection...")
    try:
        engine = create_db_engine()
        with engine.connect() as conn:
            print("  ✓ Database connection successful")
            print(f"  ✓ Connected to: {os.getenv('DB_NAME')} on {os.getenv('DB_HOST')}")
            return True
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        print("\n  Please check:")
        print("    1. PostgreSQL is running")
        print("    2. Database exists (CREATE DATABASE nyc_taxi_db;)")
        print("    3. Credentials in .env are correct")
        return False


def create_tables(drop_existing=False):
    """Create all database tables."""
    print(f"\n[2/5] {'Recreating' if drop_existing else 'Creating'} database tables...")
    try:
        engine = create_db_engine()
        
        if drop_existing:
            print("  ⚠ Dropping existing tables...")
            Base.metadata.drop_all(engine)
            print("  ✓ Existing tables dropped")
        
        Base.metadata.create_all(engine)
        print("  ✓ Tables created successfully:")
        print("    - zones (dimension table)")
        print("    - payment_types (dimension table)")
        print("    - rate_codes (dimension table)")
        print("    - trips (fact table)")
        return True
    except Exception as e:
        print(f"  ✗ Error creating tables: {e}")
        return False


def populate_payment_types():
    """Initialize payment types lookup table."""
    print("\n[3/5] Populating payment types...")
    try:
        session = get_session()
        
        # Check if already populated
        existing_count = session.query(PaymentType).count()
        if existing_count > 0:
            print(f"  ℹ Payment types already populated ({existing_count} records)")
            session.close()
            return True
        
        payment_types = [
            PaymentType(payment_type_id=1, payment_name='Credit card'),
            PaymentType(payment_type_id=2, payment_name='Cash'),
            PaymentType(payment_type_id=3, payment_name='No charge'),
            PaymentType(payment_type_id=4, payment_name='Dispute'),
            PaymentType(payment_type_id=5, payment_name='Unknown'),
            PaymentType(payment_type_id=6, payment_name='Voided trip'),
        ]
        
        session.add_all(payment_types)
        session.commit()
        print(f"  ✓ Added {len(payment_types)} payment types")
        session.close()
        return True
    except Exception as e:
        print(f"  ✗ Error populating payment types: {e}")
        return False


def populate_rate_codes():
    """Initialize rate codes lookup table."""
    print("\n[4/5] Populating rate codes...")
    try:
        session = get_session()
        
        # Check if already populated
        existing_count = session.query(RateCode).count()
        if existing_count > 0:
            print(f"  ℹ Rate codes already populated ({existing_count} records)")
            session.close()
            return True
        
        rate_codes = [
            RateCode(rate_code_id=1, rate_name='Standard rate'),
            RateCode(rate_code_id=2, rate_name='JFK'),
            RateCode(rate_code_id=3, rate_name='Newark'),
            RateCode(rate_code_id=4, rate_name='Nassau or Westchester'),
            RateCode(rate_code_id=5, rate_name='Negotiated fare'),
            RateCode(rate_code_id=6, rate_name='Group ride'),
        ]
        
        session.add_all(rate_codes)
        session.commit()
        print(f"  ✓ Added {len(rate_codes)} rate codes")
        session.close()
        return True
    except Exception as e:
        print(f"  ✗ Error populating rate codes: {e}")
        return False


def populate_zones():
    """Initialize NYC taxi zones lookup table."""
    print("\n[5/5] Populating NYC taxi zones...")
    try:
        session = get_session()
        
        # Check if already populated
        existing_count = session.query(Zone).count()
        if existing_count > 0:
            print(f"  ℹ Zones already populated ({existing_count} records)")
            session.close()
            return True
        
        # Sample of major NYC taxi zones
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
        
        for zone_data in zones_data:
            zone = Zone(**zone_data)
            session.add(zone)
        
        session.commit()
        print(f"  ✓ Added {len(zones_data)} NYC taxi zones")
        session.close()
        return True
    except Exception as e:
        print(f"  ✗ Error populating zones: {e}")
        return False


def verify_database():
    """Verify database setup and show statistics."""
    print("\n" + "="*60)
    print("Database Verification")
    print("="*60)
    
    try:
        session = get_session()
        
        # Count records in each table
        zone_count = session.query(Zone).count()
        payment_count = session.query(PaymentType).count()
        rate_count = session.query(RateCode).count()
        trip_count = session.query(Trip).count()
        
        print(f"\n✓ Database: {os.getenv('DB_NAME')}")
        print(f"✓ Host: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
        print("\nTable Statistics:")
        print(f"  - zones:         {zone_count:>8} records")
        print(f"  - payment_types: {payment_count:>8} records")
        print(f"  - rate_codes:    {rate_count:>8} records")
        print(f"  - trips:         {trip_count:>8} records")
        
        if trip_count == 0:
            print("\n⚠ No trip data loaded yet.")
            print("  Run: python data_processor.py <data_file>")
        else:
            print(f"\n✓ Database contains {trip_count:,} trip records")
        
        session.close()
        print("\n" + "="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ Verification failed: {e}")
        return False


def main():
    """Main initialization flow."""
    print("="*60)
    print("NYC Taxi Database Initialization")
    print("="*60)
    
    # Parse command line arguments
    reset_mode = '--reset' in sys.argv
    verify_only = '--verify' in sys.argv
    
    if verify_only:
        verify_database()
        return
    
    if reset_mode:
        print("\n⚠ WARNING: Reset mode enabled. All existing data will be lost!")
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    
    # Execute initialization steps
    success = True
    
    success = check_database_connection() and success
    if not success:
        print("\n✗ Initialization failed at connection check")
        sys.exit(1)
    
    success = create_tables(drop_existing=reset_mode) and success
    success = populate_payment_types() and success
    success = populate_rate_codes() and success
    success = populate_zones() and success
    
    if success:
        print("\n" + "="*60)
        print("✓ Database initialization complete!")
        print("="*60)
        verify_database()
        print("\nNext steps:")
        print("  1. Download data: python download_data.py")
        print("  2. Process data:  python data_processor.py ../data/<data_file>")
        print("  3. Start API:     python app.py")
    else:
        print("\n✗ Initialization completed with errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
