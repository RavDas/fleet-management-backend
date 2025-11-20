#!/bin/bash

# ===============================
# Maintenance Service - Complete Setup & Run Script (Linux/Mac)
# ===============================
# This script does EVERYTHING:
# 1. Creates virtual environment (if needed)
# 2. Installs dependencies
# 3. Creates .env file (if needed)
# 4. Checks if PostgreSQL is running, starts it if not
# 5. Runs the Flask application
#
# Perfect for: Fresh clone, first-time setup, or daily use
# ===============================

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}🚀 Maintenance Service - Complete Setup & Run${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# ===============================
# Step 1: Check Docker is Running
# ===============================
echo -e "${BLUE}🐳 Step 1: Checking Docker...${NC}"
if ! docker ps >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first!${NC}"
    echo -e "${YELLOW}   After starting Docker, run this script again.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker is running${NC}"
echo ""

# ===============================
# Step 2: Create .env file if needed
# ===============================
echo -e "${BLUE}⚙️  Step 2: Checking configuration...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    
    cat > .env << 'EOF'
# Flask Configuration
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=dev-secret-key-change-in-production-f89a7d6c8b4e3a2d

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/maintenance_db

# Server Configuration
PORT=5001
HOST=0.0.0.0

# CORS Configuration
CORS_ORIGINS=*

# Pagination
ITEMS_PER_PAGE=10

# Logging
LOG_LEVEL=DEBUG
EOF
    
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi
echo ""

# ===============================
# Step 3: Setup Python Virtual Environment
# ===============================
echo -e "${BLUE}🐍 Step 3: Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}   Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

echo -e "${YELLOW}   Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}   Installing/updating dependencies...${NC}"
pip install --quiet -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# ===============================
# Step 4: Check & Start PostgreSQL
# ===============================
echo -e "${BLUE}🗄️  Step 4: Checking PostgreSQL database...${NC}"

# Check if postgres-maintenance container exists and is running
containerStatus=$(docker ps -a --filter "name=postgres-maintenance" --format "{{.Status}}" || echo "")

if [[ $containerStatus == Up* ]]; then
    echo -e "${GREEN}✅ PostgreSQL is already running${NC}"
elif [ -n "$containerStatus" ]; then
    echo -e "${YELLOW}⚠️  PostgreSQL container exists but is not running. Starting...${NC}"
    docker-compose up -d postgres-maintenance
    echo -e "${YELLOW}   Waiting for PostgreSQL to be ready...${NC}"
    sleep 15
    echo -e "${GREEN}✅ PostgreSQL started successfully${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL not found. Starting for the first time...${NC}"
    docker-compose up -d postgres-maintenance
    echo -e "${YELLOW}   Waiting for PostgreSQL to initialize (first-time setup)...${NC}"
    sleep 20
    echo -e "${GREEN}✅ PostgreSQL started successfully${NC}"
fi
echo ""

# ===============================
# Step 5: Verify Database Connection
# ===============================
echo -e "${BLUE}🔍 Step 5: Verifying database connection...${NC}"
maxRetries=5
retryCount=0
connected=false

while [ "$connected" = false ] && [ $retryCount -lt $maxRetries ]; do
    if docker exec postgres-maintenance pg_isready -U postgres -d maintenance_db >/dev/null 2>&1; then
        connected=true
        echo -e "${GREEN}✅ Database is ready${NC}"
    else
        retryCount=$((retryCount + 1))
        if [ $retryCount -lt $maxRetries ]; then
            echo -e "${YELLOW}   Waiting for database... (attempt $retryCount/$maxRetries)${NC}"
            sleep 3
        else
            echo -e "${RED}❌ Database is not responding. Please check Docker logs:${NC}"
            echo -e "${YELLOW}   docker logs postgres-maintenance${NC}"
            exit 1
        fi
    fi
done
echo ""

# ===============================
# Step 6: Run Flask Application
# ===============================
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}✅ All Setup Complete! Starting Flask Application...${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${CYAN}📝 Quick Reference:${NC}"
echo -e "${WHITE}   🌐 API:              http://localhost:5001${NC}"
echo -e "${WHITE}   📚 Swagger Docs:     http://localhost:5001/docs${NC}"
echo -e "${WHITE}   💚 Health Check:     http://localhost:5001/health${NC}"
echo -e "${WHITE}   📋 Maintenance API:  http://localhost:5001/api/maintenance/${NC}"
echo ""
echo -e "${YELLOW}🛑 To stop the server: Press Ctrl+C${NC}"
echo ""
echo -e "${CYAN}============================================================${NC}"
echo ""

# Run the application
python run.py

