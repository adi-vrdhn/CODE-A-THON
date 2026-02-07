#!/bin/bash

# Interview Automation Engine - Setup Script
# This script sets up the development environment

set -e

echo "=========================================="
echo "Interview Automation Engine - Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
echo ""

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Create reports directory
echo -e "${YELLOW}Creating reports directory...${NC}"
if [ ! -d "backend/reports/output" ]; then
    mkdir -p backend/reports/output
    echo -e "${GREEN}✓ Reports directory created${NC}"
else
    echo -e "${GREEN}✓ Reports directory already exists${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the backend server:"
echo "   cd backend"
echo "   python app.py"
echo ""
echo "2. In another terminal, start a local server for frontend:"
echo "   cd frontend"
echo "   python -m http.server 8000"
echo ""
echo "3. Open browser and navigate to:"
echo "   http://localhost:8000"
echo ""
echo "=========================================="
