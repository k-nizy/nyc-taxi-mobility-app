"""
Database models for NYC Taxi Trip application.
Fully normalized schema with proper relationships and indexing.
"""

from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Zone(Base):
    """NYC Taxi Zone lookup table."""
    __tablename__ = 'zones'
    
    zone_id = Column(Integer, primary_key=True)
    borough = Column(String(50))
    zone_name = Column(String(100))
    service_zone = Column(String(50))
    
    # Relationships
    pickup_trips = relationship('Trip', foreign_keys='Trip.pickup_zone_id', back_populates='pickup_zone')
    dropoff_trips = relationship('Trip', foreign_keys='Trip.dropoff_zone_id', back_populates='dropoff_zone')


class PaymentType(Base):
    """Payment type reference table."""
    __tablename__ = 'payment_types'
    
    payment_type_id = Column(Integer, primary_key=True)
    payment_name = Column(String(50), nullable=False)
    
    # Relationships
    trips = relationship('Trip', back_populates='payment_type')


class RateCode(Base):
    """Rate code reference table."""
    __tablename__ = 'rate_codes'
    
    rate_code_id = Column(Integer, primary_key=True)
    rate_name = Column(String(50), nullable=False)
    
    # Relationships
    trips = relationship('Trip', back_populates='rate_code')


class Trip(Base):
    """Main trip records table with derived features."""
    __tablename__ = 'trips'
    
    # Primary key
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Timestamps
    pickup_datetime = Column(DateTime, nullable=False, index=True)
    dropoff_datetime = Column(DateTime, nullable=False)
    
    # Foreign keys
    pickup_zone_id = Column(Integer, ForeignKey('zones.zone_id'), index=True)
    dropoff_zone_id = Column(Integer, ForeignKey('zones.zone_id'), index=True)
    payment_type_id = Column(Integer, ForeignKey('payment_types.payment_type_id'))
    rate_code_id = Column(Integer, ForeignKey('rate_codes.rate_code_id'))
    
    # Trip metrics
    passenger_count = Column(Integer)
    trip_distance = Column(Float, index=True)
    trip_duration = Column(Float)  # in seconds
    
    # Fare information
    fare_amount = Column(Float, index=True)
    extra = Column(Float)
    mta_tax = Column(Float)
    tip_amount = Column(Float)
    tolls_amount = Column(Float)
    improvement_surcharge = Column(Float)
    total_amount = Column(Float)
    
    # Derived features (engineered)
    trip_speed = Column(Float)  # km/h or mph
    fare_per_km = Column(Float)
    fare_per_minute = Column(Float)
    
    # Relationships
    pickup_zone = relationship('Zone', foreign_keys=[pickup_zone_id], back_populates='pickup_trips')
    dropoff_zone = relationship('Zone', foreign_keys=[dropoff_zone_id], back_populates='dropoff_trips')
    payment_type = relationship('PaymentType', back_populates='trips')
    rate_code = relationship('RateCode', back_populates='trips')
    
    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_pickup_datetime_zone', 'pickup_datetime', 'pickup_zone_id'),
        Index('idx_fare_distance', 'fare_amount', 'trip_distance'),
        Index('idx_datetime_range', 'pickup_datetime', 'dropoff_datetime'),
    )
    
    def to_dict(self):
        """Convert trip to dictionary for API responses."""
        return {
            'trip_id': self.trip_id,
            'pickup_datetime': self.pickup_datetime.isoformat() if self.pickup_datetime else None,
            'dropoff_datetime': self.dropoff_datetime.isoformat() if self.dropoff_datetime else None,
            'pickup_zone': self.pickup_zone.zone_name if self.pickup_zone else None,
            'dropoff_zone': self.dropoff_zone.zone_name if self.dropoff_zone else None,
            'passenger_count': self.passenger_count,
            'trip_distance': self.trip_distance,
            'trip_duration': self.trip_duration,
            'fare_amount': self.fare_amount,
            'total_amount': self.total_amount,
            'trip_speed': self.trip_speed,
            'fare_per_km': self.fare_per_km,
            'fare_per_minute': self.fare_per_minute,
            'payment_type': self.payment_type.payment_name if self.payment_type else None,
        }


def get_database_url():
    """
    Construct database URL from environment variables.
    Falls back to SQLite if PostgreSQL credentials not available.
    """
    # Check if we should use SQLite
    use_sqlite = os.getenv('USE_SQLITE', 'false').lower() == 'true'
    
    # Check if PostgreSQL credentials are available
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'nyc_taxi_db')
    
    # Use SQLite if explicitly requested or if PostgreSQL credentials missing
    if use_sqlite or not db_user or not db_password:
        db_path = os.getenv('SQLITE_DB_PATH', 'nyc_taxi.db')
        print(f"Using SQLite database: {db_path}")
        return f"sqlite:///{db_path}"
    
    # Use PostgreSQL
    print(f"Using PostgreSQL database: {db_name} on {db_host}")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_db_engine():
    """Create SQLAlchemy engine with appropriate settings."""
    db_url = get_database_url()
    
    # Different settings for SQLite vs PostgreSQL
    if db_url.startswith('sqlite'):
        # SQLite settings
        return create_engine(
            db_url,
            echo=False,
            connect_args={'check_same_thread': False}  # Allow multi-threading
        )
    else:
        # PostgreSQL settings
        return create_engine(
            db_url,
            echo=False,
            pool_size=10,
            max_overflow=20
        )


def get_session():
    """Get database session."""
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_database():
    """Initialize database schema."""
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    print("Database schema created successfully!")
    
    # Initialize lookup tables
    session = get_session()
    
    # Payment types
    payment_types = [
        PaymentType(payment_type_id=1, payment_name='Credit card'),
        PaymentType(payment_type_id=2, payment_name='Cash'),
        PaymentType(payment_type_id=3, payment_name='No charge'),
        PaymentType(payment_type_id=4, payment_name='Dispute'),
        PaymentType(payment_type_id=5, payment_name='Unknown'),
        PaymentType(payment_type_id=6, payment_name='Voided trip'),
    ]
    
    # Rate codes
    rate_codes = [
        RateCode(rate_code_id=1, rate_name='Standard rate'),
        RateCode(rate_code_id=2, rate_name='JFK'),
        RateCode(rate_code_id=3, rate_name='Newark'),
        RateCode(rate_code_id=4, rate_name='Nassau or Westchester'),
        RateCode(rate_code_id=5, rate_name='Negotiated fare'),
        RateCode(rate_code_id=6, rate_name='Group ride'),
    ]
    
    # Check if already populated
    if session.query(PaymentType).count() == 0:
        session.add_all(payment_types)
        print("Payment types initialized.")
    
    if session.query(RateCode).count() == 0:
        session.add_all(rate_codes)
        print("Rate codes initialized.")
    
    session.commit()
    session.close()
    print("Lookup tables initialized!")


if __name__ == '__main__':
    init_database()
