#!/bin/bash

# NYC Taxi Mobility App Setup Script

echo "=================================="
echo "NYC Taxi Analytics Platform Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check PostgreSQL
echo ""
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "PostgreSQL found"
    psql_version=$(psql --version | awk '{print $3}')
    echo "PostgreSQL version: $psql_version"
else
    echo "WARNING: PostgreSQL not found. Please install PostgreSQL 12+"
    echo "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "macOS: brew install postgresql"
fi

# Check Node.js
echo ""
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    echo "Node.js found"
    node_version=$(node --version)
    echo "Node.js version: $node_version"
else
    echo "WARNING: Node.js not found. Please install Node.js 16+"
    echo "Visit: https://nodejs.org/"
fi

echo ""
echo "=================================="
echo "Backend Setup"
echo "=================================="

# Navigate to backend
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "IMPORTANT: Please edit backend/.env with your PostgreSQL credentials"
    echo ""
fi

echo "Backend setup complete!"

# Go back to root
cd ..

echo ""
echo "=================================="
echo "Frontend Setup"
echo "=================================="

# Navigate to frontend
cd frontend

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

echo "Frontend setup complete!"

# Go back to root
cd ..

echo ""
echo "=================================="
echo "Database Setup Instructions"
echo "=================================="
echo ""
echo "1. Start PostgreSQL service"
echo "   Ubuntu/Debian: sudo service postgresql start"
echo "   macOS: brew services start postgresql"
echo ""
echo "2. Create database and user:"
echo "   sudo -u postgres psql"
echo "   CREATE DATABASE nyc_taxi_db;"
echo "   CREATE USER your_user WITH PASSWORD 'your_password';"
echo "   GRANT ALL PRIVILEGES ON DATABASE nyc_taxi_db TO your_user;"
echo "   \\q"
echo ""
echo "3. Update backend/.env with your credentials"
echo ""
echo "4. Initialize database schema:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python init_db.py"
echo ""
echo "5. Download and process data:"
echo "   python download_data.py"
echo "   python data_processor.py ../data/yellow_tripdata_2023-01.parquet"
echo ""
echo "=================================="
echo "Running the Application"
echo "=================================="
echo ""
echo "Backend (Terminal 1):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Frontend (Terminal 2):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "=================================="
echo "Setup script complete!"
echo "=================================="
