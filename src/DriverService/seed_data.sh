#!/bin/bash

# ===============================
# Driver Service - Database Seeder
# ===============================
# Seeds the database with sample data from JSON files.
# Idempotent: Checks for existing records before adding.
# ===============================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}🌱 Driver Service - Database Seeder${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Check if Python is installed
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}❌ Python not found. Please install Python to run the seeder.${NC}"
    exit 1
fi

# Check if service is likely running (simple port check)
# Note: The python script does a better check, but this saves startup time
if ! echo > /dev/tcp/localhost/6001 &>/dev/null && ! nc -z localhost 6001 &>/dev/null; then
    echo -e "${YELLOW}⚠️  Warning: Driver Service (port 6001) might not be running.${NC}"
    echo -e "${YELLOW}   The seeder will attempt to connect anyway...${NC}"
    echo ""
fi

echo -e "${BLUE}🚀 Running seeder script...${NC}"
echo ""

$PYTHON_CMD seed_db.py

echo ""
echo -e "${GREEN}✅ Done.${NC}"
echo ""

