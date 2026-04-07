"""Order storage system using JSON file"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'db')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')


def _ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_orders():
    """Load all orders from JSON file"""
    _ensure_data_dir()
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_orders(orders):
    """Save all orders to JSON file"""
    _ensure_data_dir()
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def save_order(order_data):
    """
    Save a new order and return the order.

    Args:
        order_data: dict with keys: user_id, username, car, engine, suspension, bodykit, wheels, notes, contacts

    Returns:
        dict: The saved order with added id, timestamp, and status
    """
    orders = _load_orders()

    # Generate order ID
    order_num = len(orders) + 1
    order_id = f"ORD-{order_num:04d}"

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    order = {
        'id': order_id,
        'user_id': order_data.get('user_id'),
        'username': order_data.get('username', 'Unknown'),
        'car': order_data.get('car', {}),
        'engine': order_data.get('engine', {}),
        'suspension': order_data.get('suspension', {}),
        'bodykit': order_data.get('bodykit', {}),
        'wheels': order_data.get('wheels', {}),
        'notes': order_data.get('notes', ''),
        'contacts': order_data.get('contacts', ''),
        'status': 'new',  # new, in_progress, completed, cancelled
        'claimed_by': None,  # service ID that claimed this order
        'claimed_at': None,
        'status_history': [
            {'status': 'new', 'by': 'system', 'by_name': 'System', 'at': now}
        ],
        'created_at': now,
        'updated_at': now,
    }
    
    orders.append(order)
    _save_orders(orders)
    
    return order


def get_all_orders(status=None):
    """
    Get all orders, optionally filtered by status.
    
    Args:
        status: Optional status filter ('new', 'in_progress', 'completed', 'cancelled')
    
    Returns:
        list: List of orders
    """
    orders = _load_orders()
    if status:
        orders = [o for o in orders if o.get('status') == status]
    # Return newest first
    return list(reversed(orders))


def get_order(order_id):
    """
    Get a specific order by ID.
    
    Args:
        order_id: Order ID string (e.g. "ORD-0001")
    
    Returns:
        dict or None: The order if found
    """
    orders = _load_orders()
    return next((o for o in orders if o['id'] == order_id), None)


def update_order_status(order_id, new_status, service_id=None, service_name=None):
    """
    Update order status.

    Args:
        order_id: Order ID string
        new_status: New status ('new', 'in_progress', 'completed', 'cancelled')
        service_id: Optional service ID making the change
        service_name: Optional service name for display

    Returns:
        dict or None: Updated order or None if not found
    """
    orders = _load_orders()
    order = next((o for o in orders if o['id'] == order_id), None)

    if not order:
        return None

    order['status'] = new_status
    order['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add to status history
    if 'status_history' not in order:
        order['status_history'] = []
    
    order['status_history'].append({
        'status': new_status,
        'by': service_id or 'system',
        'by_name': service_name or 'System',
        'at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    _save_orders(orders)

    return order


def claim_order(order_id, service_id, service_name):
    """
    Claim an order for a service.

    Args:
        order_id: Order ID string
        service_id: Service ID claiming the order
        service_name: Service name for display

    Returns:
        dict or None: Updated order or None if not found/already claimed
    """
    orders = _load_orders()
    order = next((o for o in orders if o['id'] == order_id), None)

    if not order:
        return None
    
    if order.get('claimed_by'):
        return None  # Already claimed

    order['claimed_by'] = service_id
    order['claimed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add to status history
    if 'status_history' not in order:
        order['status_history'] = []
    
    order['status_history'].append({
        'status': 'claimed',
        'by': service_id,
        'by_name': service_name,
        'at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    _save_orders(orders)

    return order


def release_order(order_id, service_id):
    """
    Release a claimed order.

    Args:
        order_id: Order ID string
        service_id: Service ID releasing the order (must be the one who claimed it)

    Returns:
        dict or None: Updated order or None if not found/not authorized
    """
    orders = _load_orders()
    order = next((o for o in orders if o['id'] == order_id), None)

    if not order:
        return None
    
    if order.get('claimed_by') != service_id:
        return None  # Not authorized to release

    order['claimed_by'] = None
    order['claimed_at'] = None
    order['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    _save_orders(orders)

    return order


def get_order_stats():
    """
    Get order statistics.
    
    Returns:
        dict: Stats with counts per status
    """
    orders = _load_orders()
    stats = {
        'total': len(orders),
        'new': sum(1 for o in orders if o.get('status') == 'new'),
        'in_progress': sum(1 for o in orders if o.get('status') == 'in_progress'),
        'completed': sum(1 for o in orders if o.get('status') == 'completed'),
        'cancelled': sum(1 for o in orders if o.get('status') == 'cancelled'),
    }
    return stats
