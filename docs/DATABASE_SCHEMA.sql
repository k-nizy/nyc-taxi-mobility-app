-- NYC Taxi Mobility Analytics Database Schema
-- PostgreSQL 12+
-- This file can be used to manually create the database schema

-- Create zones dimension table
CREATE TABLE IF NOT EXISTS zones (
    zone_id INTEGER PRIMARY KEY,
    borough VARCHAR(50),
    zone_name VARCHAR(100),
    service_zone VARCHAR(50)
);

-- Create payment types dimension table
CREATE TABLE IF NOT EXISTS payment_types (
    payment_type_id INTEGER PRIMARY KEY,
    payment_name VARCHAR(50) NOT NULL
);

-- Create rate codes dimension table
CREATE TABLE IF NOT EXISTS rate_codes (
    rate_code_id INTEGER PRIMARY KEY,
    rate_name VARCHAR(50) NOT NULL
);

-- Create trips fact table
CREATE TABLE IF NOT EXISTS trips (
    trip_id SERIAL PRIMARY KEY,
    
    -- Timestamps
    pickup_datetime TIMESTAMP NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,
    
    -- Foreign keys to dimension tables
    pickup_zone_id INTEGER REFERENCES zones(zone_id),
    dropoff_zone_id INTEGER REFERENCES zones(zone_id),
    payment_type_id INTEGER REFERENCES payment_types(payment_type_id),
    rate_code_id INTEGER REFERENCES rate_codes(rate_code_id),
    
    -- Trip metrics
    passenger_count INTEGER,
    trip_distance FLOAT,
    trip_duration FLOAT,  -- in seconds
    
    -- Fare information
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    improvement_surcharge FLOAT,
    total_amount FLOAT,
    
    -- Derived features (engineered)
    trip_speed FLOAT,
    fare_per_km FLOAT,
    fare_per_minute FLOAT
);

-- Create indexes for query optimization
CREATE INDEX IF NOT EXISTS idx_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX IF NOT EXISTS idx_pickup_zone_id ON trips(pickup_zone_id);
CREATE INDEX IF NOT EXISTS idx_dropoff_zone_id ON trips(dropoff_zone_id);
CREATE INDEX IF NOT EXISTS idx_fare_amount ON trips(fare_amount);
CREATE INDEX IF NOT EXISTS idx_trip_distance ON trips(trip_distance);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_pickup_datetime_zone ON trips(pickup_datetime, pickup_zone_id);
CREATE INDEX IF NOT EXISTS idx_fare_distance ON trips(fare_amount, trip_distance);
CREATE INDEX IF NOT EXISTS idx_datetime_range ON trips(pickup_datetime, dropoff_datetime);

-- Insert payment types reference data
INSERT INTO payment_types (payment_type_id, payment_name) VALUES
    (1, 'Credit card'),
    (2, 'Cash'),
    (3, 'No charge'),
    (4, 'Dispute'),
    (5, 'Unknown'),
    (6, 'Voided trip')
ON CONFLICT (payment_type_id) DO NOTHING;

-- Insert rate codes reference data
INSERT INTO rate_codes (rate_code_id, rate_name) VALUES
    (1, 'Standard rate'),
    (2, 'JFK'),
    (3, 'Newark'),
    (4, 'Nassau or Westchester'),
    (5, 'Negotiated fare'),
    (6, 'Group ride')
ON CONFLICT (rate_code_id) DO NOTHING;

-- Insert sample NYC taxi zones
INSERT INTO zones (zone_id, borough, zone_name, service_zone) VALUES
    (1, 'EWR', 'Newark Airport', 'EWR'),
    (4, 'Manhattan', 'Alphabet City', 'Yellow Zone'),
    (12, 'Manhattan', 'Battery Park', 'Yellow Zone'),
    (13, 'Manhattan', 'Battery Park City', 'Yellow Zone'),
    (43, 'Manhattan', 'Central Park', 'Yellow Zone'),
    (45, 'Manhattan', 'Chinatown', 'Yellow Zone'),
    (48, 'Manhattan', 'Clinton East', 'Yellow Zone'),
    (50, 'Manhattan', 'Clinton West', 'Yellow Zone'),
    (68, 'Manhattan', 'East Chelsea', 'Yellow Zone'),
    (79, 'Manhattan', 'East Village', 'Yellow Zone'),
    (87, 'Manhattan', 'Financial District North', 'Yellow Zone'),
    (88, 'Manhattan', 'Financial District South', 'Yellow Zone'),
    (90, 'Manhattan', 'Flatiron', 'Yellow Zone'),
    (100, 'Manhattan', 'Garment District', 'Yellow Zone'),
    (107, 'Manhattan', 'Gramercy', 'Yellow Zone'),
    (113, 'Manhattan', 'Greenwich Village North', 'Yellow Zone'),
    (114, 'Manhattan', 'Greenwich Village South', 'Yellow Zone'),
    (125, 'Manhattan', 'Hamilton Heights', 'Boro Zone'),
    (127, 'Manhattan', 'Harlem', 'Boro Zone'),
    (128, 'Manhattan', 'Highbridge Park', 'Boro Zone'),
    (137, 'Queens', 'JFK Airport', 'Airports'),
    (140, 'Manhattan', 'Kips Bay', 'Yellow Zone'),
    (141, 'Manhattan', 'Lenox Hill East', 'Yellow Zone'),
    (142, 'Manhattan', 'Lenox Hill West', 'Yellow Zone'),
    (143, 'Manhattan', 'Lincoln Square East', 'Yellow Zone'),
    (144, 'Manhattan', 'Lincoln Square West', 'Yellow Zone'),
    (148, 'Manhattan', 'Little Italy/NoLiTa', 'Yellow Zone'),
    (151, 'Manhattan', 'Lower East Side', 'Yellow Zone'),
    (152, 'Queens', 'Long Island City', 'Boro Zone'),
    (153, 'Manhattan', 'Manhattan Valley', 'Yellow Zone'),
    (158, 'Manhattan', 'Meatpacking/West Village West', 'Yellow Zone'),
    (161, 'Manhattan', 'Midtown Center', 'Yellow Zone'),
    (162, 'Manhattan', 'Midtown East', 'Yellow Zone'),
    (163, 'Manhattan', 'Midtown North', 'Yellow Zone'),
    (164, 'Manhattan', 'Midtown South', 'Yellow Zone'),
    (166, 'Manhattan', 'Morningside Heights', 'Boro Zone'),
    (170, 'Manhattan', 'Murray Hill', 'Yellow Zone'),
    (186, 'Manhattan', 'Penn Station/Madison Sq West', 'Yellow Zone'),
    (194, 'Manhattan', 'Randalls Island', 'Yellow Zone'),
    (202, 'Manhattan', 'Seaport', 'Yellow Zone'),
    (209, 'Manhattan', 'SoHo', 'Yellow Zone'),
    (211, 'Manhattan', 'Stuy Town/Peter Cooper Village', 'Yellow Zone'),
    (224, 'Manhattan', 'Times Sq/Theatre District', 'Yellow Zone'),
    (229, 'Manhattan', 'Tribeca/Civic Center', 'Yellow Zone'),
    (230, 'Manhattan', 'Two Bridges/Seward Park', 'Yellow Zone'),
    (231, 'Manhattan', 'UN/Turtle Bay South', 'Yellow Zone'),
    (232, 'Manhattan', 'Union Sq', 'Yellow Zone'),
    (233, 'Manhattan', 'Upper East Side North', 'Yellow Zone'),
    (234, 'Manhattan', 'Upper East Side South', 'Yellow Zone'),
    (236, 'Manhattan', 'Upper West Side North', 'Yellow Zone'),
    (237, 'Manhattan', 'Upper West Side South', 'Yellow Zone'),
    (238, 'Manhattan', 'Washington Heights North', 'Boro Zone'),
    (239, 'Manhattan', 'Washington Heights South', 'Boro Zone'),
    (243, 'Manhattan', 'West Chelsea/Hudson Yards', 'Yellow Zone'),
    (244, 'Manhattan', 'West Village', 'Yellow Zone'),
    (246, 'Manhattan', 'World Trade Center', 'Yellow Zone'),
    (249, 'Manhattan', 'Yorkville East', 'Yellow Zone'),
    (250, 'Manhattan', 'Yorkville West', 'Yellow Zone'),
    (261, 'Brooklyn', 'Williamsburg', 'Boro Zone'),
    (262, 'Brooklyn', 'Park Slope', 'Boro Zone'),
    (263, 'Unknown', 'Unknown', 'N/A')
ON CONFLICT (zone_id) DO NOTHING;

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_username;

-- Verify setup
SELECT 'Schema created successfully!' AS status;
SELECT COUNT(*) AS zone_count FROM zones;
SELECT COUNT(*) AS payment_type_count FROM payment_types;
SELECT COUNT(*) AS rate_code_count FROM rate_codes;
