"""Pre-modified cars for sale storage - managed by admin panel with image uploads"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'db')
FOR_SALE_FILE = os.path.join(DATA_DIR, 'for_sale_cars.json')

# Store images inside the shared bot_data volume so they survive container rebuilds
UPLOADS_DIR = os.path.join(DATA_DIR, 'for_sale_images')


def _ensure_dirs():
    """Create data and upload directories if they don't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)


def _load_cars():
    """Load for-sale cars from JSON file"""
    _ensure_dirs()
    if not os.path.exists(FOR_SALE_FILE):
        return []
    with open(FOR_SALE_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_cars(cars):
    """Save all for-sale cars to JSON file"""
    _ensure_dirs()
    with open(FOR_SALE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)


def save_car(car_data, service_id=None):
    """
    Save a new pre-modified car for sale.

    Args:
        car_data: dict with keys: name, base_car_id, description, price,
                  questionnaire (mileage, year, condition, mods_list, etc.),
                  engine, suspension, bodykit, wheels, is_available
        service_id: ID of the service creating this car

    Returns:
        dict: The saved car with added id, timestamps
    """
    cars = _load_cars()

    # Generate car ID
    car_num = len(cars) + 1
    car_id = f"SALE-{car_num:04d}"

    car = {
        'id': car_id,
        'name': car_data.get('name', ''),
        'base_car_id': car_data.get('base_car_id', ''),
        'description': car_data.get('description', ''),
        'price': car_data.get('price', ''),
        'questionnaire': car_data.get('questionnaire', {}),
        'engine': car_data.get('engine', {}),
        'suspension': car_data.get('suspension', {}),
        'bodykit': car_data.get('bodykit', {}),
        'wheels': car_data.get('wheels', {}),
        'images': car_data.get('images', []),
        'is_available': car_data.get('is_available', True),
        'created_by_service_id': service_id,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    cars.append(car)
    _save_cars(cars)

    return car


def get_all_cars(available_only=False, service_id=None):
    """
    Get all pre-modified cars for sale.

    Args:
        available_only: If True, return only available cars
        service_id: If provided, return only cars created by this service

    Returns:
        list: List of cars, newest first
    """
    cars = _load_cars()
    if available_only:
        cars = [c for c in cars if c.get('is_available', True)]
    if service_id:
        cars = [c for c in cars if c.get('created_by_service_id') == service_id]
    return list(reversed(cars))


def get_car(car_id):
    """
    Get a specific car by ID.

    Args:
        car_id: Car ID string

    Returns:
        dict or None: The car if found
    """
    cars = _load_cars()
    return next((c for c in cars if c['id'] == car_id), None)


def update_car(car_id, update_data):
    """
    Update a pre-modified car.

    Args:
        car_id: Car ID string
        update_data: dict with fields to update

    Returns:
        dict or None: Updated car or None if not found
    """
    cars = _load_cars()
    car = next((c for c in cars if c['id'] == car_id), None)

    if not car:
        return None

    for key, value in update_data.items():
        if key not in ('id', 'created_at'):
            car[key] = value

    car['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _save_cars(cars)

    return car


def delete_car(car_id):
    """
    Delete a pre-modified car.

    Args:
        car_id: Car ID string

    Returns:
        bool: True if deleted, False if not found
    """
    cars = _load_cars()
    car = next((c for c in cars if c['id'] == car_id), None)

    if not car:
        return False

    cars = [c for c in cars if c['id'] != car_id]
    _save_cars(cars)

    # Optionally delete uploaded images
    for image_path in car.get('images', []):
        if image_path:
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), image_path.lstrip('/'))
            if os.path.exists(full_path):
                os.remove(full_path)

    return True


ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}


def save_uploaded_image(file, car_id, image_index):
    """
    Save an uploaded image file for a car.

    Args:
        file: Werkzeug FileStorage object
        car_id: Car ID for filename
        image_index: Index number for this image

    Returns:
        str: The saved image path (relative to static), or empty string on error
    """
    if not file or not file.filename:
        return ''

    _ensure_dirs()

    # Sanitize filename
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return ''

    safe_filename = f"car_{car_id}_img{image_index}{ext}"
    filepath = os.path.join(UPLOADS_DIR, safe_filename)

    file.save(filepath)

    return f"/for-sale-images/{safe_filename}"
