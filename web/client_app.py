"""Flask web application - JDM Car Configurator (CLIENT SIDE ONLY)"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.data.car_config_data import CARS, ENGINES, SUSPENSIONS, BODYKITS, WHEELS, PRESET_BUILDS
from bot.data.storage import save_order, get_all_orders, get_order
from bot.data.for_sale_storage import get_all_cars, get_car, UPLOADS_DIR as FOR_SALE_UPLOADS_DIR

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = os.getenv('SECRET_KEY', 'jdm-config-secret-key-2024')


# ==================== Page Routes ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/configurator')
def configurator():
    """Car configurator page"""
    return render_template('configurator.html')


@app.route('/orders')
def orders_page():
    """User orders page"""
    return render_template('orders.html')


@app.route('/marketplace')
def marketplace():
    """Pre-modified cars for sale marketplace"""
    return render_template('marketplace.html')


@app.route('/marketplace/<car_id>')
def marketplace_car(car_id):
    """View specific car for sale"""
    return render_template('marketplace_car.html', car_id=car_id)


@app.route('/presets')
def presets():
    """Ready-made preset builds page"""
    return render_template('presets.html')


# ==================== API Routes - Configuration ====================

@app.route('/api/cars', methods=['GET'])
def get_cars():
    """Get all cars"""
    return jsonify(CARS)


@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Get all preset builds with optional tag filter"""
    tag = request.args.get('tag')
    if tag:
        filtered = [p for p in PRESET_BUILDS if p.get('tag', '').lower() == tag.lower()]
        return jsonify(filtered)
    return jsonify(PRESET_BUILDS)


@app.route('/api/engines/<car_id>', methods=['GET'])
def get_engines(car_id):
    """Get engines for specific car"""
    engines = ENGINES.get(car_id, [])
    return jsonify(engines)


@app.route('/api/suspensions', methods=['GET'])
def get_suspensions():
    """Get all suspension options"""
    return jsonify(SUSPENSIONS)


@app.route('/api/bodykits', methods=['GET'])
def get_bodykits():
    """Get all bodykit options"""
    return jsonify(BODYKITS)


@app.route('/api/wheels', methods=['GET'])
def get_wheels():
    """Get all wheel options"""
    return jsonify(WHEELS)


# ==================== API Routes - Orders ====================

@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    """Get all orders with optional status filter"""
    status = request.args.get('status')
    orders = get_all_orders(status=status)
    return jsonify(orders)


@app.route('/api/orders', methods=['POST'])
def api_create_order():
    """Create a new order"""
    data = request.json
    
    if not data or not all(key in data for key in ['car', 'engine', 'suspension', 'bodykit', 'wheels']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    order_data = {
        'user_id': session.get('user_id', 'web-user'),
        'username': session.get('username', 'Web User'),
        'car': data.get('car'),
        'engine': data.get('engine'),
        'suspension': data.get('suspension'),
        'bodykit': data.get('bodykit'),
        'wheels': data.get('wheels'),
        'notes': data.get('notes', ''),
    }
    
    saved = save_order(order_data)
    return jsonify(saved), 201


@app.route('/api/orders/<order_id>', methods=['GET'])
def api_get_order(order_id):
    """Get specific order by ID"""
    order = get_order(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order)


# ==================== API Routes - Marketplace ====================

@app.route('/api/marketplace', methods=['GET'])
def api_get_marketplace():
    """Get all available cars for sale"""
    cars = get_all_cars(available_only=True)
    return jsonify(cars)


@app.route('/api/marketplace/<car_id>', methods=['GET'])
def api_get_marketplace_car(car_id):
    """Get specific car for sale"""
    car = get_car(car_id)
    if not car or not car.get('is_available', True):
        return jsonify({'error': 'Car not found'}), 404
    return jsonify(car)


# ==================== Static File Routes - For Sale Images ====================

@app.route('/for-sale-images/<filename>')
def serve_for_sale_image(filename):
    """Serve for-sale car images from the shared data volume"""
    return send_from_directory(FOR_SALE_UPLOADS_DIR, filename)


# ==================== Run Application ====================

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    print("🚗 JDM Client App starting...")
    print(f"🌐 Client URL: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
