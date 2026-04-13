"""
Health Check Routes
"""

from flask import Blueprint, jsonify
import os
from datetime import datetime

health_bp = Blueprint('health', __name__)


@health_bp.route('/status', methods=['GET'])
def health_status():
    """Get overall application health status"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {
            'api': 'running',
            'datasets': 'ready',
            'models': 'ready'
        }
    }), 200


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Check if app is ready to serve requests"""
    return jsonify({
        'ready': True,
        'message': 'Application is ready to serve requests'
    }), 200
