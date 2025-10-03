"""
Quick test script to verify database connection and setup.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*60)
print("Database Connection Test")
print("="*60)

try:
    print("\n[1/4] Loading models...")
    from models import create_db_engine, get_session, Zone, PaymentType, Trip
    print("  ✓ Models loaded successfully")
    
    print("\n[2/4] Testing database connection...")
    engine = create_db_engine()
    with engine.connect() as conn:
        print("  ✓ Database connection successful")
    
    print("\n[3/4] Testing session creation...")
    session = get_session()
    print("  ✓ Session created successfully")
    
    print("\n[4/4] Querying tables...")
    try:
        zone_count = session.query(Zone).count()
        payment_count = session.query(PaymentType).count()
        trip_count = session.query(Trip).count()
        
        print(f"  ✓ Zones: {zone_count}")
        print(f"  ✓ Payment types: {payment_count}")
        print(f"  ✓ Trips: {trip_count}")
    except Exception as e:
        print(f"  ⚠ Tables not initialized yet: {e}")
        print("  → Run: python init_db.py")
    
    session.close()
    
    print("\n" + "="*60)
    print("✓ Database is working correctly!")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("  1. Make sure you have a .env file (copy from .env.example)")
    print("  2. Run: python init_db.py")
    print("  3. Check your database credentials")
    print("\n" + "="*60)
    exit(1)
