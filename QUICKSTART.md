# NYC Taxi Analytics - Quick Start Guide

Get the application running in under 10 minutes!

## Prerequisites Check

```bash
# Check Python (need 3.8+)
python3 --version

# Check PostgreSQL (need 12+)
psql --version

# Check Node.js (need 16+)
node --version
npm --version
```

If any are missing, install them first.

## Step 1: Database Setup (2 minutes)

### Start PostgreSQL
```bash
# Linux/Ubuntu
sudo service postgresql start

# macOS
brew services start postgresql

# Check status
sudo service postgresql status
```

### Create Database
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Run these commands in psql:
CREATE DATABASE nyc_taxi_db;
CREATE USER taxi_user WITH PASSWORD 'taxi_password_123';
GRANT ALL PRIVILEGES ON DATABASE nyc_taxi_db TO taxi_user;
\q
```

## Step 2: Backend Setup (3 minutes)

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Edit `.env` file:
```bash
nano .env  # or use your preferred editor
```

Update with your database credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nyc_taxi_db
DB_USER=taxi_user
DB_PASSWORD=taxi_password_123
```

### Initialize Database
```bash
python init_db.py
```

Expected output:
```
Database schema created successfully!
Payment types initialized.
Rate codes initialized.
Lookup tables initialized!
```

## Step 3: Download Sample Data (2 minutes)

```bash
# Download January 2023 data (~45 MB)
python download_data.py

# This will download to ../data/yellow_tripdata_2023-01.parquet
```

## Step 4: Process Data (2-5 minutes depending on system)

```bash
python data_processor.py ../data/yellow_tripdata_2023-01.parquet
```

Expected output:
```
Loading data...
Loaded 3,000,000 records
Cleaning timestamps...
Removing outliers...
Engineering features...
Normalizing data...
Saving to database...
✓ Complete!
Final records: 2,799,000 (93.3% quality)
```

## Step 5: Start Backend (30 seconds)

```bash
python app.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Keep this terminal open!**

Test the API: Open browser to http://localhost:5000/health

## Step 6: Frontend Setup (2 minutes)

**Open a NEW terminal window:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Expected output:
```
Compiled successfully!
Local: http://localhost:3000
```

**Keep this terminal open!**

## Step 7: Use the Application! 🎉

Open your browser to: **http://localhost:3000**

You should see:
- Yellow header with "NYC Taxi Analytics"
- Filter panel with date, fare, distance options
- Six statistics cards showing metrics
- Multiple interactive charts

### Try These Features:

1. **Apply Filters**:
   - Set date range
   - Set min fare: $10, max fare: $50
   - Click "Apply Filters"

2. **Explore Charts**:
   - Hover over line charts for details
   - Check hourly trip distribution
   - View top pickup locations

3. **Test Different Views**:
   - Filter by specific zones
   - Adjust passenger count
   - Observe chart updates

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'psycopg2'"**
```bash
pip install psycopg2-binary
```

**"Connection refused" or database errors**
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Verify credentials in .env match database
psql -U taxi_user -d nyc_taxi_db -h localhost
```

**"No such file or directory: data file"**
```bash
# Make sure you downloaded the data
python download_data.py
```

### Frontend Issues

**"npm: command not found"**
```bash
# Install Node.js first
# Ubuntu: sudo apt install nodejs npm
# macOS: brew install node
```

**Port 3000 already in use**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm start
```

**"Module not found" errors**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Data Loading Issues

**Download fails**
```bash
# Manual download alternative:
# Visit: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
# Download yellow_tripdata_2023-01.parquet
# Place in data/ folder
```

**Processing is slow**
```bash
# This is normal - processing 3M records takes 2-5 minutes
# Watch the log output for progress
# Use smaller dataset for testing if needed
```

## Running Tests

### Backend Tests
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

### Algorithm Tests
```bash
cd backend
python algorithms.py  # Runs built-in tests
python -m pytest tests/test_algorithms.py -v
```

## Quick Commands Reference

### Start Everything
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python app.py

# Terminal 2 - Frontend
cd frontend && npm start
```

### Stop Everything
```bash
# Press Ctrl+C in each terminal
```

### Reset Database
```bash
cd backend
source venv/bin/activate
python init_db.py
python data_processor.py ../data/yellow_tripdata_2023-01.parquet
```

## What's Next?

- Read `docs/TECHNICAL_REPORT.md` for detailed documentation
- Review custom algorithms in `backend/algorithms.py`
- Explore API endpoints: `backend/app.py`
- Customize frontend: `frontend/src/components/`
- Add more data: Download additional months and process

## Getting Help

- Check logs in backend terminal for error details
- Review browser console for frontend errors
- Consult `README.md` for comprehensive setup
- Check `docs/` folder for detailed documentation

## Success Checklist

- [x] PostgreSQL running
- [x] Database created and initialized
- [x] Backend running on port 5000
- [x] Frontend running on port 3000
- [x] Data loaded (2.8M+ trips)
- [x] Dashboard displays charts
- [x] Filters work correctly
- [x] API returns data

**Congratulations! Your NYC Taxi Analytics Platform is live!** 🚕📊
