#!/usr/bin/env python
"""Diagnose the 405 error with the /api/models/predict endpoint"""

import sys
import os

# First, verify the route exists in the source code
print("\n=== CHECKING SOURCE CODE ===\n")
model_routes_path = os.path.join(os.path.dirname(__file__), 'backend', 'routes', 'model_routes.py')
with open(model_routes_path, 'r') as f:
    content = f.read()
    if "@model_bp.route('/predict'" in content:
        print("✓ Found @model_bp.route('/predict'...")
        # Find the methods
        import re
        match = re.search(r"@model_bp\.route\('/predict',\s*methods=\[(.*?)\]", content)
        if match:
            methods = match.group(1)
            print(f"✓ Methods: [{methods}]")
            if "'POST'" in methods or '"POST"' in methods:
                print("✓ POST method is enabled")
            else:
                print("✗ POST method NOT found!")
    else:
        print("✗ Route /predict NOT found in source!")

print("\n=== CHECKING FLASK APP ===\n")

os.chdir('backend')
sys.path.insert(0, '.')

from main import app

routes_info = []
for rule in app.url_map.iter_rules():
    if 'predict' in rule.rule:
        routes_info.append({
            'rule': rule.rule,
            'methods': sorted(rule.methods - {'OPTIONS', 'HEAD'})
        })

if routes_info:
    print("✓ Found predict routes in Flask:")
    for route in routes_info:
        print(f"  - {route['rule']}")
        print(f"    Methods: {route['methods']}")
        if 'POST' in route['methods']:
            print("    ✓ POST is registered")
        else:
            print("    ✗ POST is NOT registered")
else:
    print("✗ No predict routes found in Flask!")

print("\n=== TESTING ENDPOINT ===\n")

client = app.test_client()

# Test OPTIONS (preflight)
print("1. Testing OPTIONS (CORS preflight)")
response = client.options('/api/models/predict')
print(f"   Status: {response.status_code}")
print(f"   Response: {response.data}")

# Test POST with no data
print("\n2. Testing POST (no data)")
response = client.post('/api/models/predict')
print(f"   Status: {response.status_code}")
try:
    print(f"   Response: {response.get_json()}")
except:
    print(f"   Response: {response.data}")

# Test GET (should fail)
print("\n3. Testing GET (should fail)")
response = client.get('/api/models/predict')
print(f"   Status: {response.status_code}")
try:
    print(f"   Response: {response.get_json()}")
except:
    print(f"   Response: {response.data}")

print("\n=== DONE ===\n")
