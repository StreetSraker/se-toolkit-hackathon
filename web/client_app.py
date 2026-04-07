"""Flask web application - JDM Car Configurator (CLIENT SIDE ONLY)"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from datetime import datetime

# Add parent directory to path to import bot modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.data.car_config_data import CARS, ENGINES, SUSPENSIONS, BODYKITS, WHEELS, PRESET_BUILDS
from bot.data.storage import save_order, get_all_orders, get_order
from bot.data.for_sale_storage import get_all_cars, get_car, UPLOADS_DIR as FOR_SALE_UPLOADS_DIR
from bot.data.users_storage import register_user, authenticate_user, get_user, get_user_by_username, update_user
from werkzeug.security import generate_password_hash

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = os.getenv('SECRET_KEY', 'jdm-config-secret-key-2024')


# ==================== Page Routes ====================

@app.route('/')
def index():
    """Main page — redirect to login if not authenticated"""
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('index.html')


@app.route('/login')
def login_page():
    """User login page"""
    if session.get('user_id'):
        return redirect('/')
    return render_template('login.html')


@app.route('/register')
def register_page():
    """User registration page"""
    if session.get('user_id'):
        return redirect('/')
    return render_template('register.html')


@app.route('/configurator')
def configurator():
    """Car configurator page"""
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('configurator.html')


@app.route('/orders')
def orders_page():
    """User orders page — only shows current user's orders"""
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('orders.html')


@app.route('/marketplace')
def marketplace():
    """Pre-modified cars for sale marketplace"""
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('marketplace.html')


@app.route('/marketplace/<car_id>')
def marketplace_car(car_id):
    """View specific car for sale"""
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('marketplace_car.html', car_id=car_id)


@app.route('/profile')
def profile():
    """User profile page"""
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('profile.html')


# ==================== API Routes - Auth ====================

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """Register a new client user"""
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Username and password required'}), 400

    if len(data.get('password', '')) < 4:
        return jsonify({'success': False, 'message': 'Password must be at least 4 characters'}), 400

    user_data = {
        'username': data.get('username', '').strip(),
        'password': data.get('password', ''),
        'telegram': data.get('telegram', ''),
        'phone': data.get('phone', ''),
        'email': data.get('email', ''),
    }

    user = register_user(user_data)
    if not user:
        # Check if username already taken
        existing = get_user_by_username(user_data['username'])
        if existing:
            return jsonify({'success': False, 'message': 'Username already taken'}), 409
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    # Auto-login after registration
    session['user_id'] = user['id']
    session['username'] = user['username']

    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'telegram': user.get('telegram', ''),
            'phone': user.get('phone', ''),
            'email': user.get('email', ''),
        },
        'message': 'Registered successfully'
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """User login"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400

    user = authenticate_user(username, password)
    if not user:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    session['user_id'] = user['id']
    session['username'] = user['username']

    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'telegram': user.get('telegram', ''),
            'phone': user.get('phone', ''),
            'email': user.get('email', ''),
        },
        'message': 'Logged in successfully'
    })


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """User logout"""
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({'success': True})


@app.route('/api/auth/check', methods=['GET'])
def api_auth_check():
    """Check if user is authenticated"""
    return jsonify({
        'is_authenticated': bool(session.get('user_id')),
        'user_id': session.get('user_id'),
        'username': session.get('username'),
    })


# ==================== API Routes - Profile ====================

@app.route('/api/profile', methods=['GET'])
def api_get_profile():
    """Get current user's profile"""
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 403

    user = get_user(session.get('user_id'))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Return without password_hash
    safe_user = {k: v for k, v in user.items() if k != 'password_hash'}
    return jsonify(safe_user)


@app.route('/api/profile', methods=['PUT'])
def api_update_profile():
    """Update current user's profile"""
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    user_id = session.get('user_id')
    user = get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Only allow updating certain fields
    allowed_fields = {'telegram', 'phone', 'email', 'username'}
    safe_data = {k: v for k, v in data.items() if k in allowed_fields}

    # Handle password separately (needs hashing)
    if 'password' in data and data['password']:
        if len(data['password']) < 4:
            return jsonify({'error': 'Password must be at least 4 characters'}), 400
        safe_data['password_hash'] = generate_password_hash(data['password'])

    # If username is being changed, check it's not already taken
    if 'username' in safe_data:
        safe_data['username'] = safe_data['username'].strip().lower()
        existing = get_user_by_username(safe_data['username'])
        if existing and existing['id'] != user_id:
            return jsonify({'error': 'Username already taken'}), 409

    updated = update_user(user_id, safe_data)
    if not updated:
        return jsonify({'error': 'Failed to update profile'}), 500

    # Update session username if it was changed
    if 'username' in safe_data:
        session['username'] = safe_data['username']

    # Return without password_hash
    safe_updated = {k: v for k, v in updated.items() if k != 'password_hash'}
    return jsonify(safe_updated)


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
    """Get current user's orders only"""
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 403

    user_id = session.get('user_id')
    all_orders = get_all_orders()
    user_orders = [o for o in all_orders if o.get('user_id') == user_id]
    return jsonify(user_orders)


@app.route('/api/orders', methods=['POST'])
def api_create_order():
    """Create a new order for the current user"""
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json

    if not data or not all(key in data for key in ['car', 'engine', 'suspension', 'bodykit', 'wheels']):
        return jsonify({'error': 'Missing required fields'}), 400

    order_data = {
        'user_id': session.get('user_id'),
        'username': session.get('username', 'Unknown'),
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
    print(f"🔐 User authentication enabled")

    app.run(debug=debug, host='0.0.0.0', port=port)
