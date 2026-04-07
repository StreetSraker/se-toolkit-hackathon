"""Flask web application - JDM Car Configurator (SERVICE CENTER / ADMIN ONLY)"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.data.storage import get_all_orders, get_order, update_order_status, get_order_stats, claim_order, release_order
from bot.data.services_storage import (
    register_service, get_all_services, get_service, get_service_by_username,
    authenticate_service, update_service, deactivate_service, get_service_stats
)
from werkzeug.security import generate_password_hash
from bot.data.for_sale_storage import (
    get_all_cars, get_car, save_car, update_car, delete_car, save_uploaded_image,
    UPLOADS_DIR as FOR_SALE_UPLOADS_DIR
)
from bot.data.car_config_data import CARS, BODYKITS, WHEELS, SUSPENSIONS, ENGINES

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'admin_templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = os.getenv('ADMIN_SECRET_KEY', 'jdm-admin-secret-key-2024')


# ==================== Page Routes ====================

@app.route('/')
def admin_home():
    """Service login page"""
    return render_template('admin_login.html')


@app.route('/register')
def register_page():
    """Service registration page"""
    return render_template('admin_register.html')


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


@app.route('/services')
def admin_services():
    """Service management page"""
    return render_template('admin_services.html')


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


@app.route('/profile')
def service_profile():
    """Service profile management page"""
    if not session.get('is_admin'):
        return redirect('/')
    return render_template('admin_profile.html')


# ==================== API Routes - Auth ====================

@app.route('/api/service/login', methods=['POST'])
def service_login():
    """Service authentication via username and password"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400

    service = authenticate_service(username, password)
    if not service:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    session['is_admin'] = True
    session['service_id'] = service['id']
    session['service_name'] = service['name']
    session['service_username'] = service['username']

    return jsonify({
        'success': True,
        'service': {
            'id': service['id'],
            'name': service['name'],
            'username': service['username'],
            'telegram_username': service.get('telegram_username', ''),
            'phone': service.get('phone', ''),
            'specialties': service.get('specialties', []),
        },
        'message': 'Authenticated'
    })


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    session.pop('is_admin', None)
    session.pop('service_id', None)
    session.pop('service_name', None)
    return jsonify({'success': True})


@app.route('/api/admin/check', methods=['GET'])
def admin_check():
    """Check if admin is authenticated"""
    return jsonify({
        'is_admin': session.get('is_admin', False),
        'service_id': session.get('service_id'),
        'service_name': session.get('service_name'),
        'service_username': session.get('service_username'),
    })


# ==================== API Routes - Service Profile ====================

@app.route('/api/service/profile', methods=['GET'])
def api_get_service_profile():
    """Get current service's profile"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    service = get_service(session.get('service_id'))
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    # Return without password_hash
    safe_service = {k: v for k, v in service.items() if k != 'password_hash'}
    return jsonify(safe_service)


@app.route('/api/service/profile', methods=['PUT'])
def api_update_service_profile():
    """Update current service's profile"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    service_id = session.get('service_id')
    service = get_service(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    # Only allow updating certain fields
    allowed_fields = {'name', 'telegram_username', 'phone', 'specialties'}
    safe_data = {k: v for k, v in data.items() if k in allowed_fields}

    # Handle password separately (needs hashing)
    if 'password' in data and data['password']:
        if len(data['password']) < 4:
            return jsonify({'error': 'Password must be at least 4 characters'}), 400
        safe_data['password_hash'] = generate_password_hash(data['password'])

    # Handle specialties - convert string to list if needed
    if 'specialties' in safe_data and isinstance(safe_data['specialties'], str):
        safe_data['specialties'] = [s.strip() for s in safe_data['specialties'].split(',') if s.strip()]

    updated = update_service(service_id, safe_data)
    if not updated:
        return jsonify({'error': 'Failed to update profile'}), 500

    # Update session service name if it was changed
    if 'name' in safe_data:
        session['service_name'] = safe_data['name']

    # Return without password_hash
    safe_updated = {k: v for k, v in updated.items() if k != 'password_hash'}
    return jsonify(safe_updated)


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
    """Update order status — only by the service that claimed it"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    new_status = data.get('status')

    if new_status not in ['new', 'in_progress', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400

    service_id = session.get('service_id')
    service_name = session.get('service_name')

    # Check that this service has claimed the order
    order = get_order(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if order.get('claimed_by') != service_id:
        return jsonify({'error': 'You can only change status for orders you have claimed'}), 403

    updated = update_order_status(order_id, new_status, service_id, service_name)
    if not updated:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(updated)


@app.route('/api/orders/<order_id>/claim', methods=['POST'])
def api_claim_order(order_id):
    """Claim an order for the current service"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    service_id = session.get('service_id')
    service_name = session.get('service_name')

    if not service_id:
        return jsonify({'error': 'Service authentication required'}), 403

    updated = claim_order(order_id, service_id, service_name)
    if not updated:
        return jsonify({'error': 'Order not found or already claimed'}), 404

    return jsonify(updated)


@app.route('/api/orders/<order_id>/release', methods=['POST'])
def api_release_order(order_id):
    """Release a claimed order"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    service_id = session.get('service_id')

    if not service_id:
        return jsonify({'error': 'Service authentication required'}), 403

    updated = release_order(order_id, service_id)
    if not updated:
        return jsonify({'error': 'Order not found or not authorized to release'}), 404

    return jsonify(updated)


# ==================== API Routes - Statistics ====================

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """Get order statistics — each service sees only their own stats"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    service_id = session.get('service_id')
    orders = get_all_orders()

    if service_id:
        # Service sees only their own orders
        service_orders = [o for o in orders if o.get('claimed_by') == service_id]
        stats = {
            'total': len(service_orders),
            'new': sum(1 for o in service_orders if o.get('status') == 'new'),
            'in_progress': sum(1 for o in service_orders if o.get('status') == 'in_progress'),
            'completed': sum(1 for o in service_orders if o.get('status') == 'completed'),
            'cancelled': sum(1 for o in service_orders if o.get('status') == 'cancelled'),
        }

        # Popular cars for this service
        car_count = {}
        for order in service_orders:
            car_name = order.get('car', {}).get('name', 'N/A')
            car_count[car_name] = car_count.get(car_name, 0) + 1
        popular_cars = sorted(car_count.items(), key=lambda x: x[1], reverse=True)[:5]

        # Conversion rate for this service
        conversion = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0

        result = {
            **stats,
            'popular_cars': [{'name': name, 'count': count} for name, count in popular_cars],
            'conversion_rate': round(conversion, 1),
        }
    else:
        # Fallback: no service_id in session — show empty stats
        result = {
            'total': 0, 'new': 0, 'in_progress': 0,
            'completed': 0, 'cancelled': 0,
            'popular_cars': [], 'conversion_rate': 0,
        }

    return jsonify(result)


# ==================== API Routes - Services ====================

@app.route('/api/services', methods=['GET'])
def api_get_services():
    """Get all services (admin only) or current service info"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    active_only = request.args.get('active_only') != 'false'
    services = get_all_services(active_only=active_only)
    return jsonify(services)


@app.route('/api/services/register', methods=['POST'])
def api_register_service():
    """Register a new service"""
    data = request.json

    if not data or not data.get('name') or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing required fields: name, username, password'}), 400

    if len(data.get('password', '')) < 4:
        return jsonify({'error': 'Password must be at least 4 characters'}), 400

    service_data = {
        'name': data.get('name'),
        'username': data.get('username'),
        'password': data.get('password'),
        'telegram_username': data.get('telegram_username', ''),
        'phone': data.get('phone', ''),
        'specialties': data.get('specialties', []),
    }

    service = register_service(service_data)
    if not service:
        return jsonify({'error': 'Username already taken or invalid'}), 409

    # Return service without password_hash
    safe_service = {k: v for k, v in service.items() if k != 'password_hash'}
    return jsonify(safe_service), 201


@app.route('/api/services/<service_id>', methods=['GET'])
def api_get_service(service_id):
    """Get specific service details"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    service = get_service(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    return jsonify(service)


@app.route('/api/services/<service_id>', methods=['PUT'])
def api_update_service(service_id):
    """Update service information"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    # Only allow updating certain fields (prevent username/password overwrite via this route)
    allowed_fields = {'name', 'phone', 'specialties', 'is_active', 'telegram_username'}
    safe_data = {k: v for k, v in data.items() if k in allowed_fields}

    updated = update_service(service_id, safe_data)
    if not updated:
        return jsonify({'error': 'Service not found'}), 404

    # Return without password_hash
    safe_updated = {k: v for k, v in updated.items() if k != 'password_hash'}
    return jsonify(safe_updated)


@app.route('/api/services/<service_id>/deactivate', methods=['POST'])
def api_deactivate_service(service_id):
    """Deactivate a service"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    updated = deactivate_service(service_id)
    if not updated:
        return jsonify({'error': 'Service not found'}), 404

    return jsonify(updated)


@app.route('/api/services/stats', methods=['GET'])
def api_get_services_stats():
    """Get statistics for all services"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    service_id = session.get('service_id')
    if service_id:
        stats = get_service_stats(service_id)
    else:
        stats = get_service_stats()

    return jsonify(stats)


@app.route('/api/services/<service_id>/orders', methods=['GET'])
def api_get_service_orders(service_id):
    """Get orders for a specific service"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    status = request.args.get('status')
    orders = get_all_orders(status=status)

    # Filter orders for this service
    service_orders = [o for o in orders if o.get('claimed_by') == service_id]

    return jsonify(service_orders)


# ==================== API Routes - For Sale Cars ====================

@app.route('/api/for-sale', methods=['GET'])
def api_get_for_sale_cars():
    """Get for-sale cars — each service sees only their own listings"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    available_only = request.args.get('available_only') == 'true'
    service_id = session.get('service_id')
    cars = get_all_cars(available_only=available_only, service_id=service_id)
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

    service_id = session.get('service_id')
    saved = save_car(car_data, service_id=service_id)
    return jsonify(saved), 201


@app.route('/api/for-sale/<car_id>', methods=['PUT'])
def api_update_for_sale_car(car_id):
    """Update a for-sale car — only by the service that created it"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    service_id = session.get('service_id')
    if car.get('created_by_service_id') and car['created_by_service_id'] != service_id:
        return jsonify({'error': 'You can only edit cars you created'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    updated = update_car(car_id, data)
    if not updated:
        return jsonify({'error': 'Car not found'}), 404

    return jsonify(updated)


@app.route('/api/for-sale/<car_id>', methods=['DELETE'])
def api_delete_for_sale_car(car_id):
    """Delete a for-sale car — only by the service that created it"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    service_id = session.get('service_id')
    if car.get('created_by_service_id') and car['created_by_service_id'] != service_id:
        return jsonify({'error': 'You can only delete cars you created'}), 403

    deleted = delete_car(car_id)
    if not deleted:
        return jsonify({'error': 'Car not found'}), 404

    return jsonify({'success': True})


@app.route('/api/for-sale/<car_id>/images', methods=['POST'])
def api_upload_for_sale_images(car_id):
    """Upload images for a for-sale car — only by the service that created it"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    service_id = session.get('service_id')
    if car.get('created_by_service_id') and car['created_by_service_id'] != service_id:
        return jsonify({'error': 'You can only add images to cars you created'}), 403

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
    """Delete a specific image from a for-sale car — only by the service that created it"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    car = get_car(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    service_id = session.get('service_id')
    if car.get('created_by_service_id') and car['created_by_service_id'] != service_id:
        return jsonify({'error': 'You can only delete images from cars you created'}), 403

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
    susp_list = [{'id': k, **v} for k, v in SUSPENSIONS.items()]
    return jsonify(susp_list)


@app.route('/api/config/engines/<car_id>', methods=['GET'])
def api_get_engines(car_id):
    """Get engines for specific car"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    engines = ENGINES.get(car_id, [])
    return jsonify(engines)


@app.route('/api/config/engines', methods=['GET'])
def api_get_all_engines():
    """Get all engines from all cars (flattened list)"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    all_engines = []
    seen_ids = set()
    for car_engines in ENGINES.values():
        for e in car_engines:
            if e['id'] not in seen_ids:
                all_engines.append(e)
                seen_ids.add(e['id'])
    return jsonify(all_engines)


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
    print(f"🔐 Service username/password authentication")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
