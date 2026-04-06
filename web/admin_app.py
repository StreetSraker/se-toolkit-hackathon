"""Flask web application - JDM Car Configurator (SERVICE CENTER / ADMIN ONLY)"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.data.storage import get_all_orders, get_order, update_order_status, get_order_stats
from bot.data.for_sale_storage import (
    get_all_cars, get_car, save_car, update_car, delete_car, save_uploaded_image,
    UPLOADS_DIR as FOR_SALE_UPLOADS_DIR
)
from bot.data.car_config_data import CARS, BODYKITS, WHEELS, SUSPENSIONS, ENGINES

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


@app.route('/for-sale')
def admin_for_sale():
    """Admin for-sale cars management"""
    return render_template('admin_for_sale.html')


@app.route('/for-sale/new')
def admin_for_sale_new():
    """Admin create new for-sale car"""
    return render_template('admin_for_sale_edit.html', car=None)


@app.route('/for-sale/<car_id>')
def admin_for_sale_edit(car_id):
    """Admin edit for-sale car"""
    return render_template('admin_for_sale_edit.html', car=car_id)


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


# ==================== API Routes - For Sale Cars ====================

@app.route('/api/for-sale', methods=['GET'])
def api_get_for_sale_cars():
    """Get all for-sale cars"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    available_only = request.args.get('available_only') == 'true'
    cars = get_all_cars(available_only=available_only)
    return jsonify(cars)


@app.route('/api/for-sale/<car_id>', methods=['GET'])
def api_get_for_sale_car(car_id):
    """Get specific for-sale car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404
    return jsonify(car)


@app.route('/api/for-sale', methods=['POST'])
def api_create_for_sale_car():
    """Create a new for-sale car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    if not data or not data.get('name'):
        return jsonify({'error': 'Missing required field: name'}), 400

    car_data = {
        'name': data.get('name', ''),
        'base_car_id': data.get('base_car_id', ''),
        'description': data.get('description', ''),
        'price': data.get('price', ''),
        'questionnaire': data.get('questionnaire', {}),
        'engine': data.get('engine', {}),
        'suspension': data.get('suspension', {}),
        'bodykit': data.get('bodykit', {}),
        'wheels': data.get('wheels', {}),
        'images': data.get('images', []),
        'is_available': data.get('is_available', True),
    }

    saved = save_car(car_data)
    return jsonify(saved), 201


@app.route('/api/for-sale/<car_id>', methods=['PUT'])
def api_update_for_sale_car(car_id):
    """Update a for-sale car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    updated = update_car(car_id, data)
    if not updated:
        return jsonify({'error': 'Car not found'}), 404

    return jsonify(updated)


@app.route('/api/for-sale/<car_id>', methods=['DELETE'])
def api_delete_for_sale_car(car_id):
    """Delete a for-sale car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    deleted = delete_car(car_id)
    if not deleted:
        return jsonify({'error': 'Car not found'}), 404

    return jsonify({'success': True})


@app.route('/api/for-sale/<car_id>/images', methods=['POST'])
def api_upload_for_sale_images(car_id):
    """Upload images for a for-sale car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400

    files = request.files.getlist('images')
    existing_images = car.get('images', [])
    new_images = []

    for i, file in enumerate(files):
        image_path = save_uploaded_image(file, car_id, len(existing_images) + i)
        if image_path:
            new_images.append(image_path)

    # Update car with new images
    all_images = existing_images + new_images
    update_car(car_id, {'images': all_images})

    return jsonify({'success': True, 'images': new_images})


@app.route('/api/for-sale/<car_id>/images/<int:image_index>', methods=['DELETE'])
def api_delete_for_sale_image(car_id, image_index):
    """Delete a specific image from a for-sale car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    images = car.get('images', [])
    if image_index >= len(images):
        return jsonify({'error': 'Image not found'}), 404

    # Remove the image file
    image_path = images[image_index]
    if image_path:
        full_path = os.path.join(os.path.dirname(__file__), '..', image_path.lstrip('/'))
        if os.path.exists(full_path):
            os.remove(full_path)

    # Update car
    images.pop(image_index)
    update_car(car_id, {'images': images})

    return jsonify({'success': True})


@app.route('/api/config/bodykits', methods=['GET'])
def api_get_bodykits():
    """Get all bodykit options with images"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(BODYKITS)


@app.route('/api/config/wheels', methods=['GET'])
def api_get_wheels():
    """Get all wheel options with images"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(WHEELS)


@app.route('/api/config/suspensions', methods=['GET'])
def api_get_suspensions():
    """Get all suspension options"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(SUSPENSIONS)


@app.route('/api/config/engines/<car_id>', methods=['GET'])
def api_get_engines(car_id):
    """Get engines for specific car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    engines = ENGINES.get(car_id, [])
    return jsonify(engines)


@app.route('/api/config/cars', methods=['GET'])
def api_get_base_cars():
    """Get all base cars"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(CARS)


# ==================== Static File Routes - For Sale Images ====================

@app.route('/for-sale-images/<filename>')
def admin_serve_for_sale_image(filename):
    """Serve for-sale car images from the shared data volume"""
    return send_from_directory(FOR_SALE_UPLOADS_DIR, filename)


# ==================== Run Application ====================

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('ADMIN_PORT', 5001))
    
    print("🔧 JDM Service Center App starting...")
    print(f"🌐 Service Center URL: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🔐 Password protected")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
