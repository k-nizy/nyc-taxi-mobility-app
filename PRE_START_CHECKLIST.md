# Pre-Start Checklist ✅

Complete this checklist before starting the NYC Taxi Analytics app.

## 🔑 API Keys & Configuration

### ✅ **No External API Keys Needed!**

This application is **completely self-contained** and does NOT require:
- ❌ NYC Open Data API key (data is publicly available)
- ❌ Google Maps API key
- ❌ Any cloud service API keys
- ❌ External authentication tokens

### ✅ **What You DO Need:**

Only basic configuration in your `.env` file:

1. **Database Configuration** - Already set to SQLite by default ✅
2. **Flask SECRET_KEY** - Already has a development default ✅

That's it! No API keys to sign up for.

---

## 📋 Step-by-Step Pre-Start Checklist

### Backend Setup

#### 1. Check Python Installation
```bash
python3 --version
```
✅ **Required**: Python 3.8 or higher

---

#### 2. Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```
✅ You should see `(venv)` in your terminal prompt

---

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
✅ Should complete without errors (psycopg2 not needed for SQLite!)

---

#### 4. Create .env File
```bash
cp .env.example .env
```

Your `.env` should look like this (default is fine):
```bash
USE_SQLITE=true
SQLITE_DB_PATH=nyc_taxi.db

FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=dev-secret-key-change-for-production-abc123xyz789

DATA_URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
BATCH_SIZE=10000
```

✅ **No changes needed for development!** This works out of the box.

**Optional: Generate a secure SECRET_KEY** (only needed for production):
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# Copy the output to .env as SECRET_KEY
```

---

#### 5. Initialize Database
```bash
python init_db.py
```

✅ Expected output:
```
============================================================
NYC Taxi Database Initialization
============================================================

Using SQLite database: nyc_taxi.db

[1/5] Checking database connection...
  ✓ Database connection successful
  
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

---

#### 6. Test Database Connection
```bash
python test_db_connection.py
```

✅ Expected output:
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

✓ Database is working correctly!
============================================================
```

---

#### 7. Load Sample Data (Optional but Recommended)
```bash
# Generate 10,000 sample trips
python create_sample_data.py 10000

# Load into database
python data_processor.py ../data/sample_taxi_data.csv
```

✅ Expected output:
```
Generating 10000 sample trip records...
✓ Sample data saved to: ../data/sample_taxi_data.csv

Loading data...
Loaded 10000 records
Cleaning timestamps...
Removing outliers...
Engineering features...
Saving to database...
✓ Complete! Final records: 9850 (98.5% quality)
```

---

#### 8. Test Backend API
```bash
python app.py
```

✅ Expected output:
```
Using SQLite database: nyc_taxi.db
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

✅ **Test in browser**: Open http://localhost:5000/health

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "trip_count": 9850
}
```

**Keep this terminal running!** ✅

---

### Frontend Setup

#### 9. Check Node.js Installation (New Terminal!)
```bash
node --version
npm --version
```
✅ **Required**: Node.js 16+ and npm 8+

---

#### 10. Install Frontend Dependencies
```bash
cd frontend
npm install
```

✅ Should complete without errors

---

#### 11. Start Frontend
```bash
npm start
```

✅ Expected output:
```
Compiled successfully!

Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

Browser should automatically open to http://localhost:3000

---

## ✅ Final Verification

### Backend Checklist
- [x] Python 3.8+ installed
- [x] Virtual environment created and activated
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] `.env` file created (from `.env.example`)
- [x] Database initialized (`python init_db.py`)
- [x] Database connection tested (`python test_db_connection.py`)
- [x] Sample data loaded (optional)
- [x] Backend running on http://localhost:5000
- [x] Health endpoint responds: http://localhost:5000/health

### Frontend Checklist
- [x] Node.js 16+ and npm 8+ installed
- [x] Dependencies installed (`npm install`)
- [x] Frontend running on http://localhost:3000
- [x] Dashboard loads with visualizations

### Test the Complete System
1. **Open** http://localhost:3000
2. **Verify** you see:
   - Yellow header with "NYC Taxi Analytics"
   - 6 statistics cards (Total Trips, Avg Fare, etc.)
   - Filter panel on the left
   - Multiple charts below

3. **Test filtering**:
   - Select a date range
   - Set min/max fare
   - Click "Apply Filters"
   - Charts should update

4. **Test API directly**:
   ```bash
   # In a new terminal
   curl http://localhost:5000/api/statistics
   curl http://localhost:5000/api/zones
   ```

---

## 🚨 Common Issues & Solutions

### "ModuleNotFoundError: No module named 'flask'"
**Solution**: Activate virtual environment
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### "Connection refused" or "Database error"
**Solution**: Re-initialize database
```bash
rm nyc_taxi.db  # Delete old database
python init_db.py
```

### Frontend shows "Failed to fetch" errors
**Solution**: Make sure backend is running
```bash
# Check if backend is running
curl http://localhost:5000/health

# If not, start it:
cd backend
source venv/bin/activate
python app.py
```

### Empty charts on dashboard
**Solution**: Load sample data
```bash
cd backend
source venv/bin/activate
python create_sample_data.py 10000
python data_processor.py ../data/sample_taxi_data.csv
```

### Port 5000 or 3000 already in use
**Solution**: Kill the process or use different port
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port for frontend
PORT=3001 npm start
```

---

## 🎯 Quick Summary

**Required**:
- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ .env file (copy from .env.example)

**NOT Required**:
- ❌ PostgreSQL (using SQLite)
- ❌ Any API keys
- ❌ External services
- ❌ Cloud accounts

**Time to Start**:
- First time: ~5-10 minutes
- Subsequent times: ~30 seconds

---

## 🚀 Ready to Start!

If all checkboxes above are ✅, you're ready to use the app!

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
python app.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm start
```

**Browser**: http://localhost:3000

Enjoy analyzing NYC taxi data! 🚕📊
