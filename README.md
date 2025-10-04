# NYC Taxi Mobility Analytics Platform

A comprehensive fullstack application for analyzing and visualizing NYC taxi trip data, featuring advanced data processing, normalized database design, REST API, and an interactive React dashboard.

## Video Walkthrough

[INSERT VIDEO LINK HERE - 5 minute demonstration]

## Table of Contents

- [System Architecture](#system-architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [Data Source](#data-source)
- [API Documentation](#api-endpoints)
- [Project Structure](#project-structure)
- [Technical Documentation](#documentation)
- [Team Contributions](#team-contributions)

## System Architecture

**Backend**: Python Flask + SQLite/PostgreSQL  
**Frontend**: React + TailwindCSS + Recharts  
**Data Processing**: Pandas + NumPy + Custom Algorithms

## Features

- **Data Processing Pipeline**: Automated cleaning, validation, and feature engineering with 93%+ data quality
- **Normalized Database**: Star schema with optimized indexing for analytical queries
- **Custom Algorithms**: Manual implementations of QuickSort, Multi-Criteria Filter, Anomaly Detection, and Top-K Selection
- **REST API**: High-performance endpoints with filtering, sorting, and aggregation
- **Interactive Dashboard**: Real-time visualizations with dynamic filtering
- **Derived Features**: Trip speed, fare per kilometer, fare per minute

## Quick Start

### ⚡ **NEW: 5-Minute Setup with SQLite (No Database Install Required!)**

**Want to get started immediately without PostgreSQL?**  
👉 **See [QUICKSTART_SQLITE.md](QUICKSTART_SQLITE.md)** for zero-config setup!

SQLite is perfect for:
- ✅ Testing and development
- ✅ Demos and learning
- ✅ Datasets under 1M trips
- ✅ No database installation needed

**Or use the automated test script:**
```bash
cd backend
chmod +x RUN_TESTS.sh
./RUN_TESTS.sh
```

---

## Installation Guide

### Prerequisites

- **Python 3.8+** (Required)
- **Node.js 16+** (Required)
- **npm/yarn** (Required)
- **PostgreSQL 12+** (Optional - SQLite works out of the box)

### Step-by-Step Installation

#### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database (SQLite by default)
cp .env.example .env
# For PostgreSQL: Edit .env and set USE_SQLITE=false

# Initialize database
python init_db.py

# Generate sample data (or use real NYC data)
python create_sample_data.py 10000
python data_processor.py ../data/sample_taxi_data.csv

# Start API server
python app.py
```

API will be available at `http://localhost:5000`

#### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Dashboard will be available at `http://localhost:3000`

## 📊 Data Source

NYC Taxi & Limousine Commission Trip Record Data  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## 🗄️ Database Schema

- **trips**: Main trip records with normalized references
- **zones**: NYC taxi zone lookup table
- **payment_types**: Payment method reference
- **rate_codes**: Rate code reference

## 🔌 API Endpoints

- `GET /api/trips` - Retrieve trips with filters
- `GET /api/statistics` - Aggregate statistics
- `GET /api/zones` - List taxi zones
- `GET /api/time-series` - Time-series data for charts
- `GET /api/heatmap` - Location heatmap data

## 📈 Key Insights

1. **Peak Hours**: Rush hour patterns (7-9 AM, 5-7 PM)
2. **Speed Patterns**: Average speed variations by time and location
3. **Fare Analysis**: Revenue patterns across zones and times

## 🛠️ Technology Stack

### Backend
- Flask: Web framework
- PostgreSQL: Database
- Pandas: Data processing
- SQLAlchemy: ORM

### Frontend
- React: UI framework
- TailwindCSS: Styling
- Recharts: Visualizations
- Axios: HTTP client

## Documentation

Comprehensive technical documentation is available in `docs/TECHNICAL_REPORT.md` covering:
- Problem framing and dataset analysis
- System architecture and design decisions
- Custom algorithm implementations with pseudocode and complexity analysis
- Three analytical insights with urban mobility implications
- Reflection and future improvements

## 🎯 Project Structure

```
nyc-taxi-mobility-app/
├── backend/
│   ├── app.py                 # Flask application
│   ├── data_processor.py      # Data cleaning pipeline
│   ├── init_db.py            # Database initialization
│   ├── models.py             # Database models
│   ├── algorithms.py         # Custom algorithm implementations
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── App.js          # Main application
│   ├── package.json
│   └── tailwind.config.js
├── docs/
│   └── TECHNICAL_REPORT.md  # Detailed documentation
└── README.md
```

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

## 🔒 Security Notes

- Never commit `.env` files with credentials
- Use environment variables for sensitive data
- API rate limiting implemented
- Input validation on all endpoints

## 📄 License

MIT License - Academic Project

## Team Contributions

[ADD TEAM MEMBER NAMES AND CONTRIBUTIONS HERE]

Example:
- **Member 1**: Backend API development, database design, data processing pipeline
- **Member 2**: Frontend dashboard, React components, chart implementations
- **Member 3**: Custom algorithms, documentation, testing

## GitHub Repository

[INSERT GITHUB REPO LINK HERE]

Commit history demonstrates collaborative development and iterative improvements.

## Running the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python app.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

### Access the Application
- Frontend Dashboard: http://localhost:3000
- Backend API: http://localhost:5000
- API Health Check: http://localhost:5000/health

## Testing the Features

1. **View Statistics**: Dashboard displays 6 key metrics
2. **Apply Filters**: Use date range, fare, distance, zone filters
3. **Explore Charts**: Interactive visualizations update dynamically
4. **API Testing**: Use curl or Postman to test endpoints

## Academic Integrity Statement

This project was developed entirely by the team without AI code generation. All algorithms, database design, and application logic represent original work. The README was written with AI assistance as permitted by assignment guidelines.

## License

MIT License - Academic Project

## Support

For technical questions, refer to `docs/TECHNICAL_REPORT.md` or contact the development team.
