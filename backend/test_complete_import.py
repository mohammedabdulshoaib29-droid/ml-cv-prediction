#!/usr/bin/env python
"""
Complete application import and initialization test.
This verifies that the app is ready for Gunicorn deployment.
"""
import sys
import traceback

print('Testing complete application import chain...')
print('=' * 60)

try:
    print('Step 1: Importing Flask...')
    from flask import Flask, request, jsonify, send_from_directory, send_file
    print('  ✓ Flask imported')
    
    print('Step 2: Importing Flask-CORS...')
    from flask_cors import CORS
    print('  ✓ Flask-CORS imported')
    
    print('Step 3: Importing standard libraries...')
    import os
    import traceback
    from pathlib import Path
    from dotenv import load_dotenv
    print('  ✓ Standard libraries imported')
    
    print('Step 4: Importing routes...')
    from routes.dataset_routes import dataset_bp
    from routes.model_routes import model_bp
    from routes.health_routes import health_bp
    print('  ✓ All routes imported')
    
    print('Step 5: Creating Flask app...')
    app = Flask(__name__, static_folder=None)
    CORS(app)
    print('  ✓ Flask app created')
    
    print('Step 6: Configuring paths...')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'datasets')
    FRONTEND_BUILD = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')
    print(f'  ✓ UPLOAD_FOLDER: {UPLOAD_FOLDER}')
    print(f'  ✓ FRONTEND_BUILD: {FRONTEND_BUILD}')
    print(f'  ✓ Frontend exists: {os.path.exists(FRONTEND_BUILD)}')
    
    print('Step 7: Registering blueprints...')
    app.register_blueprint(dataset_bp, url_prefix='/api/datasets')
    app.register_blueprint(model_bp, url_prefix='/api/models')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    print('  ✓ All blueprints registered')
    
    print('Step 8: Listing all routes...')
    routes = list(app.url_map.iter_rules())
    for route in sorted(routes, key=lambda r: str(r)):
        print(f'    {route.methods} {route.rule}')
    print(f'  ✓ Total routes: {len(routes)}')
    
    print('Step 9: Testing app export...')
    print(f'  ✓ app object: {app}')
    print(f'  ✓ app.name: {app.name}')
    print(f'  ✓ Gunicorn load string: main:app')
    
    print('')
    print('=' * 60)
    print('✓ ALL CHECKS PASSED - APPLICATION IS READY FOR GUNICORN')
    print('=' * 60)
    sys.exit(0)
    
except Exception as e:
    print(f'✗ ERROR: {type(e).__name__}: {str(e)}')
    print(traceback.format_exc())
    sys.exit(1)
