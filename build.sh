#!/bin/bash
set -e

echo "=== Building Frontend ==="
cd frontend
npm install
npm run build
cd ..

echo "=== Installing Backend Dependencies ==="
cd backend
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
cd ..

echo "=== Build Complete ==="
