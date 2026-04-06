"""Custom preset builds storage - managed by admin panel with image upload"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PRESETS_FILE = os.path.join(DATA_DIR, 'custom_presets.json')
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'cars', 'uploads')


def _ensure_dirs():
    """Create data and upload directories if they don't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)


def _load_presets():
    """Load custom presets from JSON file"""
    _ensure_dirs()
    if not os.path.exists(PRESETS_FILE):
        return []
    with open(PRESETS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_presets(presets):
    """Save all custom presets to JSON file"""
    _ensure_dirs()
    with open(PRESETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)


def save_preset(preset_data):
    """
    Save a new custom preset.

    Args:
        preset_data: dict with keys: name, car_id, tag, tag_color, hp, description,
                     engine, suspension, bodykit, wheels, price_estimate, image_path

    Returns:
        dict: The saved preset with added id, timestamps
    """
    presets = _load_presets()

    # Generate preset ID
    preset_num = len(presets) + 1
    preset_id = f"CUSTOM-{preset_num:04d}"

    preset = {
        'id': preset_id,
        'name': preset_data.get('name', ''),
        'car_id': preset_data.get('car_id', ''),
        'tag': preset_data.get('tag', 'Custom'),
        'tag_color': preset_data.get('tag_color', '#888888'),
        'hp': preset_data.get('hp', '—'),
        'description': preset_data.get('description', ''),
        'engine': preset_data.get('engine', {}),
        'suspension': preset_data.get('suspension', {}),
        'bodykit': preset_data.get('bodykit', {}),
        'wheels': preset_data.get('wheels', {}),
        'price_estimate': preset_data.get('price_estimate', 'Negotiable'),
        'image_path': preset_data.get('image_path', ''),
        'is_custom': True,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    presets.append(preset)
    _save_presets(presets)

    return preset


def get_all_presets():
    """
    Get all custom presets.

    Returns:
        list: List of custom presets
    """
    presets = _load_presets()
    return list(reversed(presets))


def get_preset(preset_id):
    """
    Get a specific preset by ID.

    Args:
        preset_id: Preset ID string

    Returns:
        dict or None: The preset if found
    """
    presets = _load_presets()
    return next((p for p in presets if p['id'] == preset_id), None)


def update_preset(preset_id, update_data):
    """
    Update a custom preset.

    Args:
        preset_id: Preset ID string
        update_data: dict with fields to update

    Returns:
        dict or None: Updated preset or None if not found
    """
    presets = _load_presets()
    preset = next((p for p in presets if p['id'] == preset_id), None)

    if not preset:
        return None

    for key, value in update_data.items():
        if key not in ('id', 'created_at'):
            preset[key] = value

    preset['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _save_presets(presets)

    return preset


def delete_preset(preset_id):
    """
    Delete a custom preset.

    Args:
        preset_id: Preset ID string

    Returns:
        bool: True if deleted, False if not found
    """
    presets = _load_presets()
    preset = next((p for p in presets if p['id'] == preset_id), None)

    if not preset:
        return False

    presets = [p for p in presets if p['id'] != preset_id]
    _save_presets(presets)

    # Optionally delete the uploaded image
    image_path = preset.get('image_path', '')
    if image_path:
        full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), image_path.lstrip('/'))
        if os.path.exists(full_path):
            os.remove(full_path)

    return True


def save_uploaded_image(file, preset_id):
    """
    Save an uploaded image file.

    Args:
        file: Werkzeug FileStorage object
        preset_id: Preset ID for filename

    Returns:
        str: The saved image path (relative to static), or empty string on error
    """
    if not file or not file.filename:
        return ''

    _ensure_dirs()

    # Sanitize filename
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif'):
        return ''

    safe_filename = f"custom_{preset_id}{ext}"
    filepath = os.path.join(UPLOADS_DIR, safe_filename)

    file.save(filepath)

    return f"/static/images/cars/uploads/{safe_filename}"
