#!/bin/bash

# Complete test script for NYC Taxi App with SQLite

echo "============================================================"
echo "NYC Taxi App - Complete Test Script (SQLite)"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to backend directory
cd "$(dirname "$0")"

echo -e "${YELLOW}[1/7] Checking Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

echo ""
echo -e "${YELLOW}[2/7] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

echo ""
echo -e "${YELLOW}[3/7] Installing dependencies...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""
echo -e "${YELLOW}[4/7] Setting up .env file...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env from template (using SQLite)${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo ""
echo -e "${YELLOW}[5/7] Initializing database...${NC}"
python init_db.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${RED}✗ Database initialization failed${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}[6/7] Testing database connection...${NC}"
python test_db_connection.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database connection working${NC}"
else
    echo -e "${RED}✗ Database connection failed${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}[7/7] Generating sample data...${NC}"
python create_sample_data.py 1000
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Sample data generated${NC}"
    
    echo ""
    echo "Processing sample data..."
    python data_processor.py ../data/sample_taxi_data.csv
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Sample data loaded${NC}"
    else
        echo -e "${RED}✗ Data processing failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Sample data generation failed${NC}"
    exit 1
fi

echo ""
echo "============================================================"
echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
echo "============================================================"
echo ""
echo "Your NYC Taxi App is ready to run!"
echo ""
echo "To start the backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "To start the frontend (new terminal):"
echo "  cd frontend"
echo "  npm install"
echo "  npm start"
echo ""
echo "Database: SQLite (nyc_taxi.db)"
echo "Sample records loaded: 1000 trips"
echo ""
echo "============================================================"
