#!/bin/bash

# ===============================
# Maintenance Service Setup Script
# ===============================

set -e  # Exit on error

echo "======================================"
echo "🚀 Maintenance Service Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ .env file created${NC}"
    else
        echo -e "${RED}❌ .env.example not found. Please create .env manually.${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}📦 Step 1: Installing Python dependencies...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

echo -e "${BLUE}🐳 Step 2: Starting Docker containers...${NC}"
docker-compose up -d postgres-maintenance
echo "Waiting for PostgreSQL to be ready..."
sleep 10
echo -e "${GREEN}✅ PostgreSQL is running${NC}"
echo ""

echo -e "${BLUE}🗄️  Step 3: Database is initialized via init-db.sql${NC}"
echo -e "${GREEN}✅ Database schema created and sample data inserted${NC}"
echo ""

echo -e "${BLUE}🔧 Step 4: Running database migrations (if needed)...${NC}"
# Initialize Flask-Migrate if not already done
if [ ! -d "migrations" ]; then
    export FLASK_APP=run.py
    flask db init
    echo -e "${GREEN}✅ Flask-Migrate initialized${NC}"
fi
echo ""

echo "======================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "======================================"
echo ""
echo "📝 Next steps:"
echo "   1. Start the service:"
echo "      ${BLUE}docker-compose up${NC}"
echo "      or run locally:"
echo "      ${BLUE}python run.py${NC}"
echo ""
echo "   2. Access the API:"
echo "      ${BLUE}http://localhost:5001${NC}"
echo ""
echo "   3. Health check:"
echo "      ${BLUE}http://localhost:5001/health${NC}"
echo ""
echo "   4. API endpoints:"
echo "      ${BLUE}http://localhost:5001/api/maintenance${NC}"
echo ""
echo "   5. Database management (optional):"
echo "      ${BLUE}docker-compose --profile admin up pgadmin-maintenance${NC}"
echo "      ${BLUE}http://localhost:5051${NC}"
echo "      Email: admin@maintenance.local"
echo "      Password: admin123"
echo ""


