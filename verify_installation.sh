#!/bin/bash
# Installation and Verification Script for ML Web App

echo "🔍 ML Web App - Installation Verification"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python 3 found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found. Install Python 3.8+"
    exit 1
fi

# Check Node.js
echo ""
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js found: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found. Install Node.js 14+"
    exit 1
fi

# Check npm
echo ""
echo "Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm found: $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found"
    exit 1
fi

# Check backend files
echo ""
echo "Checking Backend Files..."
BACKEND_FILES=(
    "backend/main.py"
    "backend/requirements.txt"
    "backend/routes/dataset_routes.py"
    "backend/routes/model_routes.py"
    "backend/routes/health_routes.py"
    "backend/models/ann.py"
    "backend/models/rf.py"
    "backend/models/xgb.py"
    "backend/models/orchestrator.py"
)

for file in "${BACKEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file NOT FOUND"
    fi
done

# Check frontend files
echo ""
echo "Checking Frontend Files..."
FRONTEND_FILES=(
    "frontend/src/components/DatasetManager.js"
    "frontend/src/components/ModelTrainer.js"
    "frontend/src/components/ModelComparison.js"
    "frontend/src/components/PerformanceChart.js"
    "frontend/src/components/PredictionPlot.js"
    "frontend/src/styles/DatasetManager.css"
    "frontend/src/styles/ModelTrainer.css"
    "frontend/src/styles/ModelComparison.css"
    "frontend/package.json"
    "frontend/.env"
)

for file in "${FRONTEND_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file NOT FOUND"
    fi
done

# Check documentation
echo ""
echo "Checking Documentation..."
DOC_FILES=(
    "README.md"
    "QUICK_START.md"
    "BUILD_SUMMARY.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file NOT FOUND"
    fi
done

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Installation verification complete!${NC}"
echo ""
echo "Next steps:"
echo "1. cd backend && pip install -r requirements.txt"
echo "2. cd ../frontend && npm install"
echo "3. Read QUICK_START.md for running the application"
echo ""
