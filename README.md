# NYC Taxi Mobility Analytics Platform

A comprehensive full-stack application for analyzing and visualizing NYC taxi trip data, featuring advanced data processing, normalized database design, REST API, and an interactive React dashboard.

## 📹 Video Walkthrough

**[(https://youtu.be/Z1QR78wCf20)]**

> 🎥 Watch our complete system demonstration, technical explanation, and insights presentation.

## 🔗 GitHub Repository

**[INSERT GITHUB REPO LINK HERE]**

## 👥 Team Members

- **KEVIN NIZEYIMANA** - Backend API, database design, custom algorithms
- **ARNAUD MANZI INEZA** - Video presentation  
- **TUYISHIME CHRISTIAN** - Data processing, insights analysis, documentation
- **ANGE KARIGIRWA & KETSIA ANGE TETA** - Frontend dashboard, React components, visualizations

---

## 🚀 Deployment

### Deploy to Vercel (Frontend)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. **Fork or clone this repository**
2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Vercel will auto-detect the React app
3. **Set Environment Variables:**
   - Add `REACT_APP_API_URL` with your backend URL
4. **Deploy!**

### Backend Deployment

The backend requires a separate deployment. Options:
- **Render.com** - Free tier available
- **Railway.app** - Easy Python deployment
- **Heroku** - Classic PaaS
- **AWS Lambda** - Serverless option

## Table of Contents

- [Deployment](#deployment)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [API Documentation](#api-endpoints)

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

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Access at `http://localhost:3000`

---

## Installation Guide

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm**

### Environment Setup

**Backend (.env):**
```bash
cd backend
cp .env.example .env
# Edit .env if needed
```

**Frontend (.env):**
```bash
cd frontend
cp .env.example .env
# Set REACT_APP_API_URL to your backend URL
```

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

## 🎯 Project Structure

```
nyc-taxi-mobility-app/
├── backend/
│   ├── app.py              # Flask REST API
│   ├── models.py           # Database models
│   ├── algorithms.py       # Custom algorithms
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── nyc_taxi.db         # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.js          # Main application
│   ├── package.json
│   └── .env.example        # Frontend config
├── vercel.json             # Vercel deployment config
└── README.md
```

## 📄 License

MIT License - Academic Project

## 🔒 Security

- Never commit `.env` files
- Use environment variables for all sensitive data
- Update `REACT_APP_API_URL` in production deployment

