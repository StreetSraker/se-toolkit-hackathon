"""Client user accounts storage system using JSON file"""

import json
import os
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'db')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')


def _ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_users():
    """Load all users from JSON file"""
    _ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_users(users):
    """Save all users to JSON file"""
    _ensure_data_dir()
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def register_user(user_data):
    """
    Register a new client user.

    Args:
        user_data: dict with keys: username, password, telegram, phone, email

    Returns:
        dict: The registered user with added id and timestamp, or None if username exists
    """
    users = _load_users()

    username = user_data.get('username', '').strip().lower()
    if not username:
        return None
    if any(u.get('username', '').lower() == username for u in users):
        return None

    password = user_data.get('password', '')
    if not password or len(password) < 4:
        return None
    password_hash = generate_password_hash(password)

    user_num = len(users) + 1
    user_id = f"USR-{user_num:04d}"

    user = {
        'id': user_id,
        'username': username,
        'password_hash': password_hash,
        'telegram': user_data.get('telegram', ''),
        'phone': user_data.get('phone', ''),
        'email': user_data.get('email', ''),
        'is_active': True,
        'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    users.append(user)
    _save_users(users)

    return user


def authenticate_user(username, password):
    """
    Authenticate a user by username and password.

    Args:
        username: User username
        password: User password (plain text)

    Returns:
        dict or None: The user if authenticated, None otherwise
    """
    users = _load_users()
    username = username.strip().lower()

    for user in users:
        if user.get('username', '').lower() == username:
            if not user.get('is_active', True):
                return None
            if check_password_hash(user.get('password_hash', ''), password):
                return user
            return None

    return None


def get_user(user_id):
    """
    Get a specific user by ID.

    Args:
        user_id: User ID string (e.g. "USR-0001")

    Returns:
        dict or None: The user if found
    """
    users = _load_users()
    return next((u for u in users if u['id'] == user_id), None)


def get_user_by_username(username):
    """
    Get a user by username.

    Args:
        username: User username

    Returns:
        dict or None: The user if found
    """
    users = _load_users()
    return next((u for u in users if u.get('username', '').lower() == username.lower()), None)


def update_user(user_id, update_data):
    """
    Update user information.

    Args:
        user_id: User ID string
        update_data: dict with fields to update

    Returns:
        dict or None: Updated user or None if not found
    """
    users = _load_users()
    user = next((u for u in users if u['id'] == user_id), None)

    if not user:
        return None

    for key, value in update_data.items():
        if key != 'id':
            user[key] = value

    _save_users(users)

    return user


def get_user_orders(user_id):
    """
    Get all orders for a specific user.

    Args:
        user_id: User ID string

    Returns:
        list: List of orders for this user, newest first
    """
    from bot.data.storage import get_all_orders

    orders = get_all_orders()
    user_orders = [o for o in orders if o.get('user_id') == user_id]
    return user_orders
