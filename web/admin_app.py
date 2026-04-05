"""Flask web application - JDM Car Configurator (SERVICE CENTER / ADMIN ONLY)"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.data.storage import get_all_orders, get_order, update_order_status, get_order_stats

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'admin_templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = os.getenv('ADMIN_SECRET_KEY', 'jdm-admin-secret-key-2024')

# Admin settings
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'service2024')


# ==================== Page Routes ====================

@app.route('/')
def admin_home():
    """Admin login page"""
    return render_template('admin_login.html')


@app.route('/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    return render_template('admin_dashboard.html')


@app.route('/orders')
def admin_orders():
    """Admin orders list"""
    return render_template('admin_orders.html')


@app.route('/stats')
def admin_stats():
    """Admin statistics"""
    return render_template('admin_stats.html')


# ==================== API Routes - Admin Auth ====================

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


# ==================== API Routes - Orders ====================

@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    """Get all orders with optional status filter"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    status = request.args.get('status')
    orders = get_all_orders(status=status)
    return jsonify(orders)


@app.route('/api/orders/<order_id>', methods=['GET'])
def api_get_order(order_id):
    """Get specific order by ID"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
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


# ==================== API Routes - Statistics ====================

@app.route('/api/stats', methods=['GET'])
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
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('ADMIN_PORT', 5001))
    
    print("🔧 JDM Service Center App starting...")
    print(f"🌐 Service Center URL: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🔐 Password protected")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
