# Quick Start with SQLite (No PostgreSQL Required!)

Get the app running in **5 minutes** using SQLite - no database setup needed!

## Why SQLite?

- ✅ **No installation required** - SQLite is built into Python
- ✅ **Zero configuration** - Just run and go
- ✅ **Perfect for testing** - Quick development and demos
- ✅ **Easy to share** - Single database file

> **Note**: For production or large datasets (>1M records), use PostgreSQL for better performance.

## Quick Setup (5 minutes)

### 1. Install Python Dependencies (1 min)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (psycopg2 not needed for SQLite!)
pip install -r requirements.txt
```

### 2. Configure for SQLite (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# The default .env is already set for SQLite!
# USE_SQLITE=true is the default
```

Your `.env` should look like this:
```bash
USE_SQLITE=true
SQLITE_DB_PATH=nyc_taxi.db

FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=dev-secret-key-change-in-production
```

### 3. Initialize Database (30 seconds)

```bash
python init_db.py
```

Expected output:
```
============================================================
NYC Taxi Database Initialization
============================================================

Using SQLite database: nyc_taxi.db

[1/5] Checking database connection...
  ✓ Database connection successful
  ✓ Connected to: nyc_taxi.db

[2/5] Creating database tables...
  ✓ Tables created successfully

[3/5] Populating payment types...
  ✓ Added 6 payment types

[4/5] Populating rate codes...
  ✓ Added 6 rate codes

[5/5] Populating NYC taxi zones...
  ✓ Added 60 NYC taxi zones

✓ Database initialization complete!
```

### 4. Test Database Connection (30 seconds)

```bash
python test_db_connection.py
```

Expected output:
```
============================================================
Database Connection Test
============================================================

[1/4] Loading models...
  ✓ Models loaded successfully

[2/4] Testing database connection...
  ✓ Database connection successful

[3/4] Testing session creation...
  ✓ Session created successfully

[4/4] Querying tables...
  ✓ Zones: 60
  ✓ Payment types: 6
  ✓ Trips: 0

============================================================
✓ Database is working correctly!
============================================================
```

### 5. Generate Sample Data (1 min)

```bash
# Generate 10,000 sample trips (fast!)
python create_sample_data.py 10000

# Process the data into database
python data_processor.py ../data/sample_taxi_data.csv
```

### 6. Start the Backend (10 seconds)

```bash
python app.py
```

Expected output:
```
Using SQLite database: nyc_taxi.db
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

✅ **Backend is running!** Test it: http://localhost:5000/health

### 7. Start the Frontend (1 min)

**Open a NEW terminal:**

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm start
```

✅ **Done!** Open http://localhost:3000

## Verify Everything Works

### Test the API:
```bash
# Health check
curl http://localhost:5000/health

# Get trip statistics
curl http://localhost:5000/api/statistics

# Get zones
curl http://localhost:5000/api/zones
```

### Use the Dashboard:
1. Open http://localhost:3000
2. You should see statistics cards and charts
3. Try applying filters (dates, fares, etc.)
4. Explore the visualizations

## SQLite Database File

Your data is stored in: `backend/nyc_taxi.db`

This is a single file containing all your data. You can:
- **Back it up**: Just copy the file
- **Share it**: Send the file to others
- **Reset it**: Delete the file and run `python init_db.py` again
- **Inspect it**: Use [DB Browser for SQLite](https://sqlitebrowser.org/)

## Loading Real NYC Taxi Data

SQLite works great for datasets up to **500K-1M trips**:

```bash
# Download real data (3M trips, ~45MB)
python download_data.py

# Process it (this will take 2-5 minutes with SQLite)
python data_processor.py ../data/yellow_tripdata_2023-01.parquet
```

> **Performance Note**: Processing 3M records with SQLite is slower than PostgreSQL but still works! For large datasets, consider PostgreSQL.

## Switching to PostgreSQL Later

Want to upgrade to PostgreSQL for better performance? Easy!

1. **Install PostgreSQL**
2. **Update `.env`**:
   ```bash
   USE_SQLITE=false
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=nyc_taxi_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```
3. **Install PostgreSQL driver**:
   ```bash
   pip install psycopg2-binary
   ```
4. **Re-initialize**:
   ```bash
   python init_db.py
   python data_processor.py <data_file>
   ```

## Troubleshooting

### "No such table" error
```bash
# Re-initialize database
rm nyc_taxi.db  # Delete old database
python init_db.py
```

### Empty charts on frontend
```bash
# Make sure you loaded data
python create_sample_data.py 10000
python data_processor.py ../data/sample_taxi_data.csv
```

### Backend won't start
```bash
# Check if virtual environment is activated
source venv/bin/activate

# Verify dependencies
pip install -r requirements.txt

# Test database connection
python test_db_connection.py
```

## Complete Command Summary

**First Time Setup:**
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python init_db.py
python create_sample_data.py 10000
python data_processor.py ../data/sample_taxi_data.csv
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

**Subsequent Runs:**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend
cd frontend
npm start
```

## Performance Comparison

| Operation | SQLite | PostgreSQL |
|-----------|--------|------------|
| Initial setup | 30 seconds | 5 minutes |
| Process 10K trips | ~5 seconds | ~3 seconds |
| Process 1M trips | ~2 minutes | ~1 minute |
| Process 3M trips | ~6 minutes | ~3 minutes |
| API queries | Fast | Faster |
| Best for | Testing, demos | Production, large data |

---

**You're all set!** 🎉 

The app is now running with SQLite - no PostgreSQL needed!

For questions, check the main README.md or QUICKSTART.md
