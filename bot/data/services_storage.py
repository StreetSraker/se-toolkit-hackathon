"""Service/Technician storage system using JSON file"""

import json
import os
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
SERVICES_FILE = os.path.join(DATA_DIR, 'services.json')


def _ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_services():
    """Load all services from JSON file"""
    _ensure_data_dir()
    if not os.path.exists(SERVICES_FILE):
        return []
    with open(SERVICES_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_services(services):
    """Save all services to JSON file"""
    _ensure_data_dir()
    with open(SERVICES_FILE, 'w', encoding='utf-8') as f:
        json.dump(services, f, ensure_ascii=False, indent=2)


def register_service(service_data):
    """
    Register a new service and return the service.

    Args:
        service_data: dict with keys: name, username, password, telegram_username, phone, specialties

    Returns:
        dict: The registered service with added id and timestamp, or None if username already exists
    """
    services = _load_services()

    # Check if username already taken
    username = service_data.get('username', '').strip().lower()
    if not username:
        return None  # Username is required
    if any(s.get('username', '').lower() == username for s in services):
        return None  # Username already taken

    # Hash the password
    password = service_data.get('password', '')
    if not password or len(password) < 4:
        return None  # Password too short
    password_hash = generate_password_hash(password)

    # Generate service ID
    service_num = len(services) + 1
    service_id = f"SVC-{service_num:04d}"

    service = {
        'id': service_id,
        'name': service_data.get('name', 'Unknown Service'),
        'username': username,
        'password_hash': password_hash,
        'telegram_username': service_data.get('telegram_username', ''),
        'phone': service_data.get('phone', ''),
        'specialties': service_data.get('specialties', []),
        'is_active': True,
        'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    services.append(service)
    _save_services(services)

    return service


def authenticate_service(username, password):
    """
    Authenticate a service by username and password.

    Args:
        username: Service username
        password: Service password (plain text)

    Returns:
        dict or None: The service if authenticated, None otherwise
    """
    services = _load_services()
    username = username.strip().lower()

    for service in services:
        if service.get('username', '').lower() == username:
            if not service.get('is_active', True):
                return None  # Service is deactivated
            if check_password_hash(service.get('password_hash', ''), password):
                return service
            return None  # Wrong password

    return None  # Username not found


def get_all_services(active_only=True):
    """
    Get all services.

    Args:
        active_only: If True, return only active services

    Returns:
        list: List of services
    """
    services = _load_services()
    if active_only:
        services = [s for s in services if s.get('is_active', True)]
    return services


def get_service(service_id):
    """
    Get a specific service by ID.

    Args:
        service_id: Service ID string (e.g. "SVC-0001")

    Returns:
        dict or None: The service if found
    """
    services = _load_services()
    return next((s for s in services if s['id'] == service_id), None)


def get_service_by_username(username):
    """
    Get a service by username.

    Args:
        username: Service username

    Returns:
        dict or None: The service if found
    """
    services = _load_services()
    return next((s for s in services if s.get('username', '').lower() == username.lower()), None)


def update_service(service_id, update_data):
    """
    Update service information.

    Args:
        service_id: Service ID string
        update_data: dict with fields to update

    Returns:
        dict or None: Updated service or None if not found
    """
    services = _load_services()
    service = next((s for s in services if s['id'] == service_id), None)

    if not service:
        return None

    service.update(update_data)
    _save_services(services)

    return service


def deactivate_service(service_id):
    """
    Deactivate a service (soft delete).

    Args:
        service_id: Service ID string

    Returns:
        dict or None: Updated service or None if not found
    """
    return update_service(service_id, {'is_active': False})


def get_service_stats(service_id=None):
    """
    Get statistics for a specific service or all services.

    Args:
        service_id: Optional service ID to filter

    Returns:
        dict or list: Stats per service
    """
    from bot.data.storage import get_all_orders

    orders = get_all_orders()

    if service_id:
        # Stats for specific service
        service_orders = [o for o in orders if o.get('claimed_by') == service_id]
        return {
            'total': len(service_orders),
            'new': sum(1 for o in service_orders if o.get('status') == 'new'),
            'in_progress': sum(1 for o in service_orders if o.get('status') == 'in_progress'),
            'completed': sum(1 for o in service_orders if o.get('status') == 'completed'),
            'cancelled': sum(1 for o in service_orders if o.get('status') == 'cancelled'),
            'unclaimed': sum(1 for o in service_orders if not o.get('claimed_by')),
        }
    else:
        # Stats for all services
        services = get_all_services(active_only=False)
        stats = []
        for service in services:
            svc_orders = [o for o in orders if o.get('claimed_by') == service['id']]
            stats.append({
                'service_id': service['id'],
                'name': service['name'],
                'telegram_username': service.get('telegram_username', ''),
                'is_active': service.get('is_active', True),
                'total': len(svc_orders),
                'new': sum(1 for o in svc_orders if o.get('status') == 'new'),
                'in_progress': sum(1 for o in svc_orders if o.get('status') == 'in_progress'),
                'completed': sum(1 for o in svc_orders if o.get('status') == 'completed'),
                'cancelled': sum(1 for o in svc_orders if o.get('status') == 'cancelled'),
            })
        return stats
