"""Flask web application - JDM Car Configurator"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.data.car_config_data import CARS, ENGINES, SUSPENSIONS, BODYKITS, WHEELS
from bot.data.storage import save_order, get_all_orders, get_order, update_order_status, get_order_stats

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'jdm-config-secret-key-2024')

# Admin settings
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'service2024')


# ==================== Helper Functions ====================

def generate_order_id():
    """Generate unique order ID"""
    orders = get_all_orders()
    order_num = len(orders) + 1
    return f"ORD-{order_num:04d}"


# ==================== Page Routes ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/configurator')
def configurator():
    """Car configurator page"""
    return render_template('configurator.html', 
                         cars=CARS, 
                         suspensions=SUSPENSIONS, 
                         bodykits=BODYKITS, 
                         wheels=WHEELS)


@app.route('/orders')
def orders_page():
    """User orders page"""
    return render_template('orders.html')


@app.route('/admin')
def admin_page():
    """Admin panel page"""
    return render_template('admin.html')


@app.route('/admin/stats')
def admin_stats_page():
    """Admin statistics page"""
    return render_template('admin_stats.html')


# ==================== API Routes - Configuration ====================

@app.route('/api/cars', methods=['GET'])
def get_cars():
    """Get all cars"""
    return jsonify(CARS)


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
        'contacts': data.get('contacts', ''),
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


@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def api_update_order_status(order_id):
    """Update order status"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    new_status = data.get('status')
    
    if new_status not in ['new', 'in_progress', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    updated = update_order_status(order_id, new_status)
    if not updated:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(updated)


# ==================== API Routes - Admin ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin authentication"""
    data = request.json
    password = data.get('password', '')
    
    if password == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({'success': True, 'message': 'Authenticated'})
    
    return jsonify({'success': False, 'message': 'Invalid password'}), 401


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    session.pop('is_admin', None)
    return jsonify({'success': True})


@app.route('/api/admin/check', methods=['GET'])
def admin_check():
    """Check if admin is authenticated"""
    return jsonify({'is_admin': session.get('is_admin', False)})


@app.route('/api/admin/stats', methods=['GET'])
def api_get_stats():
    """Get order statistics"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = get_order_stats()
    orders = get_all_orders()
    
    # Calculate popular cars
    car_count = {}
    for order in orders:
        car_name = order.get('car', {}).get('name', 'N/A')
        car_count[car_name] = car_count.get(car_name, 0) + 1
    
    popular_cars = sorted(car_count.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calculate conversion rate
    conversion = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
    
    return jsonify({
        **stats,
        'popular_cars': [{'name': name, 'count': count} for name, count in popular_cars],
        'conversion_rate': round(conversion, 1)
    })


# ==================== Run Application ====================

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)
    
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    print("🚗 JDM Configurator Web App starting...")
    print(f"🌐 Running on http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
