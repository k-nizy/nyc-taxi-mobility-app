# NYC Taxi Mobility Analytics Platform

A comprehensive fullstack application for analyzing and visualizing NYC taxi trip data, featuring advanced data processing, database storage, REST API, and an interactive React dashboard.

## 🏗️ System Architecture

**Backend**: Python Flask + SQLite/PostgreSQL  
**Frontend**: React + TailwindCSS + Recharts  
**Data Processing**: Pandas + NumPy + Custom Algorithms

## 📋 Features

- **Data Processing Pipeline**: Automated cleaning, validation, and feature engineering
- **Normalized Database**: Optimized schema with proper indexing (SQLite or PostgreSQL)
- **REST API**: High-performance endpoints for data querying and aggregation
- **Interactive Dashboard**: Real-time visualizations with advanced filtering
- **Custom Algorithm**: Manual multi-criteria filtering implementation

## 🚀 Quick Start

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

### Full Setup (with PostgreSQL)

#### Prerequisites

- Python 3.8+
- PostgreSQL 12+ (optional - use SQLite if you don't have it)
- Node.js 16+
- npm/yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database
python init_db.py

# Download and process NYC taxi data
python data_processor.py

# Start API server
python app.py
```

API will be available at `http://localhost:5000`

### Frontend Setup

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

## 📝 Documentation

See `docs/TECHNICAL_REPORT.md` for detailed technical documentation including:
- System architecture
- Database design rationale
- Algorithm complexity analysis
- Analytical insights

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

## 👥 Contributing

This is an academic project demonstrating fullstack development capabilities.

## 📞 Support

For issues or questions, please refer to the technical documentation.
