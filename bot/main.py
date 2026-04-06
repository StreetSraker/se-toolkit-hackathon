"""Main bot application - single ConversationHandler architecture"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from bot.data.car_config_data import CARS, ENGINES, SUSPENSIONS, BODYKITS, WHEELS
from bot.data.storage import save_order, get_all_orders, get_order, update_order_status, get_order_stats
from bot.data.for_sale_storage import get_all_cars, get_car

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    MAIN_MENU,
    # Config states
    SELECT_CAR, SELECT_ENGINE, SELECT_SUSPENSION, SELECT_BODYKIT, SELECT_WHEEL, CONFIG_SUMMARY,
    # Custom input states
    CUSTOM_ENGINE, CUSTOM_SUSPENSION, CUSTOM_BODYKIT, CUSTOM_WHEELS,
    # Order states
    ORDER_REVIEW, ORDER_CONFIRMED,
    # Admin states
    ADMIN_AUTH, ADMIN_MENU, ADMIN_ORDER_LIST, ADMIN_ORDER_DETAIL,
    # Marketplace states
    MARKETPLACE_LIST, MARKETPLACE_DETAIL, MARKETPLACE_INQUIRY,
) = range(20)

# Admin settings
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'service2024')

# Status display
STATUS_NAMES = {
    'new': '🆕 New',
    'in_progress': '🔧 In Progress',
    'completed': '✅ Completed',
    'cancelled': '❌ Cancelled',
}
STATUS_EMOJI = {
    'new': '🆕',
    'in_progress': '🔧',
    'completed': '✅',
    'cancelled': '❌',
}


# ==================== Helpers ====================

def get_image_path(image_url):
    """Convert web image URL/path to local file path"""
    if not image_url:
        return None
    # Convert /static/images/... to actual file path
    if image_url.startswith('/static/'):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_dir, image_url.lstrip('/'))
    return None


async def send_car_image(update, context, image_url, caption, parse_mode='HTML'):
    """Send a car image if available, fallback to text"""
    image_path = get_image_path(image_url)
    if image_path and os.path.exists(image_path):
        try:
            if update.callback_query:
                # Send photo with caption - users can tap to view full-screen and zoom/pan
                await update.callback_query.message.reply_photo(
                    photo=open(image_path, 'rb'),
                    caption=caption,
                    parse_mode=parse_mode
                )
                # Edit original to show "image sent"
                await update.callback_query.edit_message_text("📸 Image sent above ⬆️\n💡 Tap the image to view full-screen, zoom and pan")
                return True
            elif update.effective_message:
                await update.effective_message.reply_photo(
                    photo=open(image_path, 'rb'),
                    caption=caption,
                    parse_mode=parse_mode
                )
                return True
        except Exception as e:
            logger.error(f"Error sending image: {e}")
    return False


def _main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚗 Configurator", callback_data="menu_config")],
        [InlineKeyboardButton("🏪 Marketplace", callback_data="menu_marketplace")],
        [InlineKeyboardButton("📋 My Orders", callback_data="menu_orders")],
        [InlineKeyboardButton("🔧 Service Panel", callback_data="menu_admin")],
        [InlineKeyboardButton("ℹ️ About", callback_data="menu_about")],
    ])


async def show_main_menu(update: Update) -> int:
    """Show main menu screen"""
    text = (
        f"👋 Hello, {update.effective_user.first_name}!\n\n"
        f"🏎️ <b>JDM Config Bot</b> — a service for ordering cars from the 90s and 00s with custom configuration\n\n"
        f"Choose an action:"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode='HTML', reply_markup=_main_menu_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=_main_menu_keyboard())
    return MAIN_MENU


async def _edit(update: Update, text: str, **kwargs):
    """Edit message or reply"""
    if update.callback_query:
        await update.callback_query.edit_message_text(text, **kwargs)
    elif update.effective_message:
        await update.effective_message.reply_text(text, **kwargs)


# ==================== Main Menu ====================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await show_main_menu(update)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_about":
        await query.edit_message_text(
            "ℹ️ <b>About the Service</b>\n\n"
            "We help order cars from the 90s and 00s with custom configuration:\n\n"
            "• Engine selection and tuning\n"
            "• Suspension setup\n"
            "• Bodykit installation\n"
            "• Wheel selection\n\n"
            "All work is performed by professional technicians experienced with JDM vehicles."
            "\n\n📞 Contact the manager: @manager_username",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]])
        )
        return MAIN_MENU

    elif data == "menu_config":
        return await start_config(update, context)

    elif data == "menu_orders":
        return await start_orders(update, context)

    elif data == "menu_admin":
        return await start_admin(update, context)

    elif data == "menu_marketplace":
        return await start_marketplace(update, context)

    elif data == "mp_list":
        return await show_marketplace_list(update, context)

    elif data == "mp_photos":
        return await show_car_photos(update, context)

    elif data == "mp_next_photo":
        return await show_next_photo(update, context)

    elif data == "mp_inquire":
        return await start_inquiry(update, context)

    elif data.startswith("mp_car_"):
        return await show_car_detail(update, context)

    elif data == "back_to_main":
        return await show_main_menu(update)

    return MAIN_MENU


# ==================== Config Flow ====================

async def start_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['config'] = {}
    keyboard = [[InlineKeyboardButton(f"{c['name']} ({c['years']})", callback_data=f"car_{c['id']}")] for c in CARS]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
    
    # Try to send a general configurator image, or just show text
    config_image = "/static/images/cars/supra.svg"  # Default hero image
    sent = await send_car_image(update, context, config_image, 
                                "🚗 <b>Car Configurator</b>\n\nSelect a car:",
                                parse_mode='HTML')
    if not sent:
        await update.callback_query.edit_message_text(
            "🚗 <b>Car Configurator</b>\n\nSelect a car:",
            parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
        )
    return SELECT_CAR


async def select_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    car_id = query.data.replace("car_", "")
    car = next((c for c in CARS if c['id'] == car_id), None)
    if not car:
        return SELECT_CAR
    context.user_data['config']['car'] = car
    engines = ENGINES.get(car_id, [])
    keyboard = [[InlineKeyboardButton(e['name'], callback_data=f"engine_{e['id']}")] for e in engines]
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="engine_custom")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_car")])
    await query.edit_message_text(
        f"🚗 <b>{car['name']}</b>\nYears: {car['years']}\n{car['description']}\n\n⚙️ Select an engine:",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_ENGINE


async def select_engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    engine_id = query.data.replace("engine_", "")
    if engine_id == "custom":
        await query.edit_message_text(
            "⚙️ <b>Custom Engine</b>\n\n"
            "Enter your desired engine/configuration.\n"
            "For example: '2JZ with Garrett GT3582R, 800 hp' or 'HKS 3.4L Kit'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_ENGINE
    if engine_id == "engine_custom":
        await query.edit_message_text(
            "⚙️ <b>Custom Engine</b>\n\n"
            "Enter your desired engine/configuration.\n"
            "For example: '2JZ with Garrett GT3582R, 800 hp' or 'HKS 3.4L Kit'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_ENGINE
    car_id = context.user_data['config']['car']['id']
    engine = next((e for e in ENGINES.get(car_id, []) if e['id'] == engine_id), None)
    if not engine:
        return SELECT_ENGINE
    context.user_data['config']['engine'] = engine
    keyboard = [[InlineKeyboardButton(s['name'], callback_data=f"susp_{sid}")] for sid, s in SUSPENSIONS.items()]
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="susp_custom")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_engine")])
    await query.edit_message_text(
        f"⚙️ <b>{engine['name']}</b>\nPower: {engine['power']}\n{engine['description']}\n\n🔧 Select suspension:",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_SUSPENSION


async def select_suspension(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    sid = query.data.replace("susp_", "")
    if sid == "custom":
        await query.edit_message_text(
            "🔧 <b>Custom Suspension</b>\n\n"
            "Enter your desired suspension configuration.\n"
            "For example: 'BC Racing BR Series, -40mm, camber -2.0'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_SUSPENSION
    if sid == "susp_custom":
        await query.edit_message_text(
            "🔧 <b>Custom Suspension</b>\n\n"
            "Enter your desired suspension configuration.\n"
            "For example: 'BC Racing BR Series, -40mm, camber -2.0'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_SUSPENSION
    susp = SUSPENSIONS.get(sid)
    if not susp:
        return SELECT_SUSPENSION
    context.user_data['config']['suspension'] = {'id': sid, **susp}
    keyboard = [[InlineKeyboardButton(bk['name'], callback_data=f"bodykit_{bk['id']}")] for bk in BODYKITS]
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="bodykit_custom")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_susp")])
    await query.edit_message_text(
        f"🔧 <b>{susp['name']}</b>\n{susp['description']}\n"
        f"Ride height: {susp['ride_height']} | Camber: {susp['camber']}\n\n🎨 Select a bodykit:",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_BODYKIT


async def select_bodykit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    bk_id = query.data.replace("bodykit_", "")
    if bk_id == "custom":
        await query.edit_message_text(
            "🎨 <b>Custom Bodykit</b>\n\n"
            "Enter your desired bodykit or brand.\n"
            "For example: 'VARIS Geo widebody, carbon hood' or 'Rocket Bunny v2'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_BODYKIT
    if bk_id == "bodykit_custom":
        await query.edit_message_text(
            "🎨 <b>Custom Bodykit</b>\n\n"
            "Enter your desired bodykit or brand.\n"
            "For example: 'VARIS Geo widebody, carbon hood' or 'Rocket Bunny v2'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_BODYKIT
    bk = next((b for b in BODYKITS if b['id'] == bk_id), None)
    if not bk:
        return SELECT_BODYKIT
    context.user_data['config']['bodykit'] = bk
    keyboard = []
    for i in range(0, len(WHEELS), 2):
        row = [InlineKeyboardButton(WHEELS[i]['name'], callback_data=f"wheel_{WHEELS[i]['id']}")]
        if i + 1 < len(WHEELS):
            row.append(InlineKeyboardButton(WHEELS[i+1]['name'], callback_data=f"wheel_{WHEELS[i+1]['id']}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="wheel_custom")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_bodykit")])
    components = "\n".join([f"• {c}" for c in bk['components']])
    await query.edit_message_text(
        f"🎨 <b>{bk['name']}</b>\n{bk['description']}\nStyle: {bk['style']}\n\n"
        f"Components:\n{components}\n\n🛞 Select wheels:",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_WHEEL


async def select_wheel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    w_id = query.data.replace("wheel_", "")
    if w_id == "custom":
        await query.edit_message_text(
            "🛞 <b>Custom Wheels</b>\n\n"
            "Enter your desired wheels (brand, model, size).\n"
            "For example: 'Volk TE37 18x9.5 +22' or 'BBS RS 18inch gold'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_WHEELS
    if w_id == "wheel_custom":
        await query.edit_message_text(
            "🛞 <b>Custom Wheels</b>\n\n"
            "Enter your desired wheels (brand, model, size).\n"
            "For example: 'Volk TE37 18x9.5 +22' or 'BBS RS 18inch gold'\n\n"
            "Or press /cancel to cancel.",
            parse_mode='HTML'
        )
        return CUSTOM_WHEELS
    wheel = next((w for w in WHEELS if w['id'] == w_id), None)
    if not wheel:
        return SELECT_WHEEL
    context.user_data['config']['wheels'] = wheel
    cfg = context.user_data['config']
    text = (
        f"✅ <b>Configuration complete!</b>\n\n"
        f"🚗 {cfg['car']['name']} ({cfg['car']['years']})\n"
        f"⚙️ {cfg['engine']['name']} — {cfg['engine']['power']}\n"
        f"🔧 {cfg['suspension']['name']}\n"
        f"🎨 {cfg['bodykit']['name']}\n"
        f"🛞 {cfg['wheels']['name']}\n"
    )
    keyboard = [
        [InlineKeyboardButton("📦 Place Order", callback_data="place_order")],
        [InlineKeyboardButton("🔄 Start Over", callback_data="restart_config")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
    ]
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIG_SUMMARY


async def config_summary_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == "place_order":
        return await start_orders(update, context)
    elif query.data == "restart_config":
        return await start_config(update, context)
    return CONFIG_SUMMARY


# ==================== Custom Input Handlers ====================

async def handle_custom_engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("❌ Please enter your desired engine.")
        return CUSTOM_ENGINE

    context.user_data['config']['engine'] = {
        'id': 'custom',
        'name': f'Custom: {text}',
        'power': 'Custom',
        'description': text
    }

    keyboard = [[InlineKeyboardButton(s['name'], callback_data=f"susp_{sid}")] for sid, s in SUSPENSIONS.items()]
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="susp_custom")])
    await update.message.reply_text(
        f"✅ <b>Engine saved:</b> {text}\n\n"
        f"🔧 <b>Now select suspension:</b>",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_SUSPENSION


async def handle_custom_suspension(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("❌ Please enter your desired suspension.")
        return CUSTOM_SUSPENSION

    context.user_data['config']['suspension'] = {
        'id': 'custom',
        'name': f'Custom: {text}',
        'description': text,
        'ride_height': 'Custom',
        'dampening': 'Custom',
        'spring_rate': 'Custom',
        'camber': 'Custom',
        'use_case': 'Custom configuration'
    }

    keyboard = [[InlineKeyboardButton(bk['name'], callback_data=f"bodykit_{bk['id']}")] for bk in BODYKITS]
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="bodykit_custom")])
    await update.message.reply_text(
        f"✅ <b>Suspension saved:</b> {text}\n\n"
        f"🎨 <b>Now select bodykit:</b>",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_BODYKIT


async def handle_custom_bodykit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("❌ Please enter your desired bodykit.")
        return CUSTOM_BODYKIT

    context.user_data['config']['bodykit'] = {
        'id': 'custom',
        'name': f'Custom: {text}',
        'description': text,
        'components': ['Custom parts'],
        'style': 'Custom',
        'price_range': 'Negotiable'
    }

    keyboard = []
    for i in range(0, len(WHEELS), 2):
        row = [InlineKeyboardButton(WHEELS[i]['name'], callback_data=f"wheel_{WHEELS[i]['id']}")]
        if i + 1 < len(WHEELS):
            row.append(InlineKeyboardButton(WHEELS[i+1]['name'], callback_data=f"wheel_{WHEELS[i+1]['id']}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("✏️ Other (custom)", callback_data="wheel_custom")])
    await update.message.reply_text(
        f"✅ <b>Bodykit saved:</b> {text}\n\n"
        f"🛞 <b>Now select wheels:</b>",
        parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECT_WHEEL


async def handle_custom_wheels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("❌ Please enter your desired wheels.")
        return CUSTOM_WHEELS

    context.user_data['config']['wheels'] = {
        'id': 'custom',
        'name': f'Custom: {text}',
        'description': text,
        'sizes': 'Custom',
        'weight': 'Custom',
        'style': 'Custom',
        'price_range': 'Negotiable'
    }

    cfg = context.user_data['config']
    text_summary = (
        f"✅ <b>Wheels saved:</b> {text}\n\n"
        f"✅ <b>Configuration complete!</b>\n\n"
        f"🚗 {cfg['car']['name']} ({cfg['car']['years']})\n"
        f"⚙️ {cfg['engine']['name']}\n"
        f"🔧 {cfg['suspension']['name']}\n"
        f"🎨 {cfg['bodykit']['name']}\n"
        f"🛞 {cfg['wheels']['name']}\n"
    )
    keyboard = [
        [InlineKeyboardButton("📦 Place Order", callback_data="place_order")],
        [InlineKeyboardButton("🔄 Start Over", callback_data="restart_config")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
    ]
    await update.message.reply_text(text_summary, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIG_SUMMARY


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel custom input and go back"""
    await update.message.reply_text("❌ Input cancelled. Choose from the list or press /start to return to the main menu.")
    return MAIN_MENU


# ==================== Order Flow ====================

async def start_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    config = context.user_data.get('config', {})
    user_id = update.effective_user.id
    all_orders_list = get_all_orders()
    my_orders = [o for o in all_orders_list if o.get('user_id') == user_id]

    if my_orders:
        text = f"📋 <b>Your Orders ({len(my_orders)})</b>\n\n"
        for o in my_orders[:10]:
            car = o.get('car', {}).get('name', 'N/A')
            st = o.get('status', 'new')
            text += f"{STATUS_EMOJI.get(st, '📋')} <code>{o['id']}</code> — {car}\n"
            text += f"   Status: {STATUS_NAMES.get(st, st)} | {o.get('created_at', '')}\n\n"
    else:
        text = "📋 <b>You have no orders yet</b>\n\n"

    if config:
        keyboard = [
            [InlineKeyboardButton("📦 Place Order", callback_data="confirm_order")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
        ]
    else:
        text += "First, configure a car through the Configurator."
        keyboard = [
            [InlineKeyboardButton("🚗 Configurator", callback_data="menu_config")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
        ]
    await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return ORDER_REVIEW


async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    cfg = context.user_data.get('config', {})
    if not cfg:
        await query.edit_message_text("❌ No configuration. Configure a car through the Configurator.")
        return MAIN_MENU

    order_data = {
        'user_id': query.from_user.id,
        'username': query.from_user.username or query.from_user.first_name,
        'car': cfg.get('car', {}), 'engine': cfg.get('engine', {}),
        'suspension': cfg.get('suspension', {}), 'bodykit': cfg.get('bodykit', {}),
        'wheels': cfg.get('wheels', {}), 'notes': '',
    }
    saved = save_order(order_data)
    text = (
        f"✅ <b>Order #{saved['id']} placed!</b>\n\n"
        f"🚗 {cfg['car']['name']} ({cfg['car']['years']})\n"
        f"⚙️ {cfg['engine']['name']} — {cfg['engine']['power']}\n"
        f"🔧 {cfg['suspension']['name']}\n"
        f"🎨 {cfg['bodykit']['name']}\n"
        f"🛞 {cfg['wheels']['name']}\n\n"
        f"Status: 🆕 New\n"
        f"A manager will contact you soon. Thank you! 🚗"
    )
    keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]]
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data.pop('config', None)
    return ORDER_CONFIRMED


# ==================== Marketplace Flow ====================

async def start_marketplace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show marketplace main menu"""
    return await show_marketplace_list(update, context)


async def show_marketplace_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show list of available cars for sale"""
    cars = get_all_cars(available_only=True)
    
    if not cars:
        text = (
            "🏪 <b>Marketplace</b>\n\n"
            "🔍 No cars available at the moment.\n\n"
            "Stay tuned for updates or build your own unique project in the Configurator!"
        )
        keyboard = [[InlineKeyboardButton("🚗 Configurator", callback_data="menu_config")]]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
        await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        return MARKETPLACE_LIST
    
    text = "🏪 <b>Marketplace</b>\n\n🚗 <b>Ready-Made Projects</b>\n\nPre-modified cars from our service:\n\n"
    
    keyboard = []
    for car in cars[:10]:  # Show up to 10 cars
        car_preview = f"💰 {car.get('price', 'Negotiable')}"
        btn_text = f"🚗 {car['name']} — {car_preview}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"mp_car_{car['id']}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])

    await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return MARKETPLACE_LIST


async def show_car_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show details of a specific car for sale"""
    query = update.callback_query
    await query.answer()
    
    car_id = query.data.replace("mp_car_", "")
    car = get_car(car_id)
    
    if not car:
        await query.edit_message_text("❌ Car not found")
        return await show_marketplace_list(update, context)
    
    context.user_data['marketplace_car'] = car
    
    # Build detail text
    text = f"🚗 <b>{car['name']}</b>\n\n"
    text += f"💰 <b>{car.get('price', 'Negotiable')}</b>\n\n"
    
    if car.get('description'):
        text += f"📝 {car['description']}\n\n"
    
    # Questionnaire
    q = car.get('questionnaire', {})
    if q:
        text += "📋 <b>Questionnaire</b>\n"
        if q.get('mileage'):
            text += f"• Mileage: {q['mileage']} km\n"
        if q.get('year'):
            text += f"• Year: {q['year']}\n"
        if q.get('condition'):
            cond_map = {'excellent': 'Excellent', 'good': 'Good', 'fair': 'Fair', 'project': 'Project'}
            text += f"• Condition: {cond_map.get(q['condition'], q['condition'])}\n"
        if q.get('location'):
            text += f"• Location: {q['location']}\n"
        if q.get('contact'):
            text += f"• Contact: {q['contact']}\n"
        text += "\n"
    
    # Modifications
    mods = []
    if car.get('engine', {}).get('id'):
        mods.append(f"⚙️ Engine: {car['engine'].get('name', car['engine']['id'])}")
    if car.get('suspension', {}).get('id'):
        mods.append(f"🔧 Suspension: {car['suspension'].get('name', car['suspension']['id'])}")
    if car.get('bodykit', {}).get('id'):
        mods.append(f"🎨 Bodykit: {car['bodykit'].get('name', car['bodykit']['id'])}")
    if car.get('wheels', {}).get('id'):
        mods.append(f"🛞 Wheels: {car['wheels'].get('name', car['wheels']['id'])}")

    if mods:
        text += "🛠️ <b>Modifications</b>\n" + "\n".join(mods) + "\n\n"

    if q.get('mods_list'):
        text += f"📦 <b>Modifications List</b>\n{q['mods_list']}\n\n"
    
    # Images info
    images = car.get('images', [])
    if images:
        text += f"📸 Photos: {len(images)}\n\n"

    text += "Choose an action:"

    keyboard = [
        [InlineKeyboardButton("💬 Request Details", callback_data="mp_inquire")],
        [InlineKeyboardButton("📸 View Photos", callback_data="mp_photos")],
        [InlineKeyboardButton("⬅️ Back to List", callback_data="mp_list")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
    ]

    # If car has images, send the first one
    if images:
        first_image = images[0]
        sent = await send_car_image(update, context, first_image, text, parse_mode='HTML')
        if not sent:
            await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    return MARKETPLACE_DETAIL


async def show_car_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show car photos"""
    query = update.callback_query
    await query.answer()

    car = context.user_data.get('marketplace_car', {})
    images = car.get('images', [])

    if not images:
        await query.answer("📷 This car has no photos", show_alert=True)
        return MARKETPLACE_DETAIL

    # Show first image with caption
    text = f"📸 <b>{car['name']}</b>\n\nPhoto: 1/{len(images)}\n💡 Tap the image to zoom and pan"
    context.user_data['marketplace_photo_idx'] = 0

    keyboard = []
    if len(images) > 1:
        keyboard.append([
            InlineKeyboardButton("⬅️ Previous", callback_data="mp_prev_photo"),
            InlineKeyboardButton("➡️ Next", callback_data="mp_next_photo")
        ])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Details", callback_data=f"mp_car_{car['id']}")])

    first_image = images[0]
    sent = await send_car_image(update, context, first_image, text, parse_mode='HTML')
    if not sent:
        try:
            await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    return MARKETPLACE_DETAIL


async def show_next_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show next car photo"""
    query = update.callback_query
    await query.answer()

    car = context.user_data.get('marketplace_car', {})
    images = car.get('images', [])

    if not images:
        return MARKETPLACE_DETAIL

    # Get current photo index from user data
    current_idx = context.user_data.get('marketplace_photo_idx', 0)
    next_idx = (current_idx + 1) % len(images)
    context.user_data['marketplace_photo_idx'] = next_idx

    text = f"📸 <b>{car['name']}</b>\n\nPhoto: {next_idx + 1}/{len(images)}\n💡 Tap the image to zoom and pan"

    keyboard = []
    if len(images) > 1:
        keyboard.append([
            InlineKeyboardButton("⬅️ Previous", callback_data="mp_prev_photo"),
            InlineKeyboardButton("➡️ Next", callback_data="mp_next_photo")
        ])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Details", callback_data=f"mp_car_{car['id']}")])

    next_image = images[next_idx]
    sent = await send_car_image(update, context, next_image, text, parse_mode='HTML')
    if not sent:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return MARKETPLACE_DETAIL


async def show_prev_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show previous car photo"""
    query = update.callback_query
    await query.answer()

    car = context.user_data.get('marketplace_car', {})
    images = car.get('images', [])

    if not images:
        return MARKETPLACE_DETAIL

    # Get current photo index from user data
    current_idx = context.user_data.get('marketplace_photo_idx', 0)
    prev_idx = (current_idx - 1) % len(images)
    context.user_data['marketplace_photo_idx'] = prev_idx

    text = f"📸 <b>{car['name']}</b>\n\nPhoto: {prev_idx + 1}/{len(images)}\n💡 Tap the image to zoom and pan"

    keyboard = []
    if len(images) > 1:
        keyboard.append([
            InlineKeyboardButton("⬅️ Previous", callback_data="mp_prev_photo"),
            InlineKeyboardButton("➡️ Next", callback_data="mp_next_photo")
        ])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Details", callback_data=f"mp_car_{car['id']}")])

    prev_image = images[prev_idx]
    sent = await send_car_image(update, context, prev_image, text, parse_mode='HTML')
    if not sent:
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return MARKETPLACE_DETAIL


async def start_inquiry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start inquiry about a car"""
    query = update.callback_query
    await query.answer()
    
    car = context.user_data.get('marketplace_car', {})
    
    text = (
        f"💬 <b>Inquiry about {car.get('name', 'the car')}</b>\n\n"
        f"Write your question or request additional information:\n\n"
        f"For example:\n"
        f"• Interested in engine condition\n"
        f"• Can I see it in person?\n"
        f"• Is the price negotiable?\n\n"
        f"Or press /cancel to cancel."
    )

    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data=f"mp_car_{car.get('id', '')}")]]
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return MARKETPLACE_INQUIRY


async def handle_inquiry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle inquiry message"""
    inquiry_text = update.message.text if update.message else ""
    
    car = context.user_data.get('marketplace_car', {})
    user = update.effective_user
    
    # Send inquiry to admin (you can customize this)
    notification = (
        f"🔔 <b>New car inquiry</b>\n\n"
        f"🚗 Car: {car.get('name', 'N/A')}\n"
        f"👤 From: {user.first_name} (@{user.username or user.id})\n\n"
        f"💬 Message:\n{inquiry_text}"
    )
    
    # Here you could forward to admin chat or log it
    logger.info(f"Marketplace inquiry: {notification}")
    
    await update.message.reply_text(
        "✅ <b>Inquiry sent!</b>\n\n"
        "We received your question and will get back to you shortly.\n\n"
        "For urgent inquiries, contact us directly: @manager_username",
        parse_mode='HTML'
    )
    
    return await show_marketplace_list(update, context)


async def inquiry_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle inquiry confirmation button"""
    query = update.callback_query
    await query.answer()
    
    car = context.user_data.get('marketplace_car', {})
    
    text = (
        f"💬 <b>Inquiry about {car.get('name', 'the car')}</b>\n\n"
        f"Write your question, and we will get back to you soon!"
    )

    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data=f"mp_car_{car.get('id', '')}")]]
    
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return MARKETPLACE_INQUIRY


# ==================== Admin Flow ====================

async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "🔐 <b>Service Panel Login</b>\n\nEnter password:"
    await _edit(update, text, parse_mode='HTML')
    return ADMIN_AUTH


async def handle_auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pwd = update.message.text if update.message else ""
    if pwd == ADMIN_PASSWORD:
        context.user_data['is_admin'] = True
        return await show_admin_menu(update)
    await update.message.reply_text("❌ Incorrect password. Try again:", parse_mode='HTML')
    return ADMIN_AUTH


async def show_admin_menu(update: Update) -> int:
    stats = get_order_stats()
    text = (
        f"🔧 <b>Service Panel</b>\n\n"
        f"📊 Total: {stats['total']} | 🆕 {stats['new']} | 🔧 {stats['in_progress']} | ✅ {stats['completed']} | ❌ {stats['cancelled']}"
    )
    kb = [
        [InlineKeyboardButton("📋 All Orders", callback_data="admin_all_orders")],
        [InlineKeyboardButton("🆕 New", callback_data="admin_new_orders")],
        [InlineKeyboardButton("🔧 In Progress", callback_data="admin_progress_orders")],
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
    ]
    await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_MENU


async def admin_menu_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    d = query.data

    if d in ("admin_all_orders", "admin_new_orders", "admin_progress_orders"):
        status = None
        if d == "admin_new_orders":
            status = 'new'
        elif d == "admin_progress_orders":
            status = 'in_progress'
        return await show_order_list(update, context, status)
    elif d == "admin_stats":
        return await show_admin_stats(update)
    elif d == "admin_back_menu":
        return await show_admin_menu(update)
    elif d == "admin_back_to_list":
        return await show_order_list(update, context)
    return ADMIN_MENU


async def show_order_list(update: Update, context: ContextTypes.DEFAULT_TYPE, status=None) -> int:
    orders = get_all_orders(status=status)
    if not orders:
        text = "📋 No orders."
        kb = [[InlineKeyboardButton("⬅️ Back", callback_data="admin_back_menu"), InlineKeyboardButton("🏠 Menu", callback_data="back_to_main")]]
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        return ADMIN_ORDER_LIST

    text = f"📋 <b>Orders ({len(orders)})</b>\n\n"
    for o in orders[:10]:
        car = o.get('car', {}).get('name', 'N/A')
        st = o.get('status', 'new')
        text += f"{STATUS_EMOJI.get(st,'📋')} <code>{o['id']}</code> — {car} | {o.get('username','?')} | {o.get('created_at','')}\n"
    if len(orders) > 10:
        text += f"\n...and {len(orders) - 10} more"

    kb = []
    for o in orders[:5]:
        car = o.get('car', {}).get('name', 'N/A')[:25]
        kb.append([InlineKeyboardButton(f"{STATUS_EMOJI.get(o.get('status','new'),'')} {o['id']} — {car}", callback_data=f"admin_order_{o['id']}")])
    kb.append([InlineKeyboardButton("⬅️ Back", callback_data="admin_back_menu")])
    kb.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")])
    if status:
        kb.insert(0, [InlineKeyboardButton("📋 All Orders", callback_data="admin_all_orders")])

    await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_ORDER_LIST


async def show_order_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, order_id) -> int:
    o = get_order(order_id)
    if not o:
        await update.callback_query.edit_message_text("❌ Order not found")
        return ADMIN_ORDER_LIST

    car = o.get('car', {})
    text = (
        f"📦 <b>Order {o['id']}</b> | {STATUS_NAMES.get(o.get('status','new'),'')}\n"
        f"Created: {o.get('created_at','')}\n\n"
        f"👤 {o.get('username','?')} (ID: {o.get('user_id','')})\n\n"
        f"🚗 {car.get('name','N/A')} ({car.get('years','')})\n"
        f"⚙️ {o.get('engine',{}).get('name','N/A')} — {o.get('engine',{}).get('power','')}\n"
        f"🔧 {o.get('suspension',{}).get('name','N/A')}\n"
        f"🎨 {o.get('bodykit',{}).get('name','N/A')}\n"
        f"🛞 {o.get('wheels',{}).get('name','N/A')}\n"
    )
    if o.get('notes'):
        text += f"\n📝 {o['notes']}\n"

    kb = []
    cur = o.get('status', 'new')
    for ns in ['new', 'in_progress', 'completed', 'cancelled']:
        if ns != cur:
            kb.append([InlineKeyboardButton(f"🔄 {STATUS_NAMES[ns]}", callback_data=f"admin_set_status_{o['id']}_{ns}")])
    kb.append([InlineKeyboardButton("⬅️ Back", callback_data="admin_back_to_list")])
    kb.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")])

    await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_ORDER_DETAIL


async def handle_order_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    d = query.data

    if d.startswith("admin_order_"):
        oid = d[len("admin_order_"):]
        return await show_order_detail(update, context, oid)

    if d.startswith("admin_set_status_"):
        data = d[len("admin_set_status_"):]
        parts = data.split('_')
        oid = parts[0]
        ns = '_'.join(parts[1:])
        o = update_order_status(oid, ns)
        if o:
            await query.edit_message_text(f"✅ Status {oid} → {STATUS_NAMES.get(ns, ns)}")
            return await show_order_detail(update, context, oid)
        await query.edit_message_text("❌ Order not found")
        return ADMIN_ORDER_LIST

    return ADMIN_ORDER_DETAIL


async def show_admin_stats(update: Update) -> int:
    stats = get_order_stats()
    orders = get_all_orders()
    cc = {}
    for o in orders:
        n = o.get('car', {}).get('name', 'N/A')
        cc[n] = cc.get(n, 0) + 1
    top = sorted(cc.items(), key=lambda x: x[1], reverse=True)[:5]
    top_text = "\n".join(f"   {i+1}. {n}: {c}" for i, (n, c) in enumerate(top)) or "   No data"
    conv = f"({stats['completed']/stats['total']*100:.1f}%)" if stats['total'] > 0 else "(no orders)"
    text = (
        f"📊 <b>Statistics</b>\n\n"
        f"Total: {stats['total']}\n"
        f"🆕 {stats['new']} | 🔧 {stats['in_progress']} | ✅ {stats['completed']} | ❌ {stats['cancelled']}\n\n"
        f"<b>Popular cars:</b>\n{top_text}\n\n"
        f"<b>Conversion:</b> {stats['completed']}/{stats['total']} {conv}"
    )
    kb = [
        [InlineKeyboardButton("⬅️ Back", callback_data="admin_back_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
    ]
    await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_MENU


# ==================== Back to Main ====================

async def back_to_main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    return await show_main_menu(update)


# ==================== Bot Setup ====================

def main():
    """Start the bot"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        if k.strip() == 'BOT_TOKEN':
                            token = v.strip()
                            break
    if not token:
        logger.error("BOT_TOKEN not found")
        return

    app = ApplicationBuilder().token(token).build()

    # Single ConversationHandler for everything
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(menu_handler, pattern='^menu_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            # Config
            SELECT_CAR: [
                CallbackQueryHandler(select_car, pattern='^car_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            SELECT_ENGINE: [
                CallbackQueryHandler(select_engine, pattern='^engine_'),
                CallbackQueryHandler(back_to_config_car, pattern='^back_to_config_car$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            SELECT_SUSPENSION: [
                CallbackQueryHandler(select_suspension, pattern='^susp_'),
                CallbackQueryHandler(back_to_config_engine, pattern='^back_to_config_engine$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            SELECT_BODYKIT: [
                CallbackQueryHandler(select_bodykit, pattern='^bodykit_'),
                CallbackQueryHandler(back_to_config_susp, pattern='^back_to_config_susp$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            SELECT_WHEEL: [
                CallbackQueryHandler(select_wheel, pattern='^wheel_'),
                CallbackQueryHandler(back_to_config_bodykit, pattern='^back_to_config_bodykit$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            CONFIG_SUMMARY: [
                CallbackQueryHandler(config_summary_action, pattern='^(place_order|restart_config)$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            # Custom input
            CUSTOM_ENGINE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_engine),
                CommandHandler("cancel", cmd_cancel),
                CallbackQueryHandler(back_to_config_engine, pattern='^back_to_config_engine$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            CUSTOM_SUSPENSION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_suspension),
                CommandHandler("cancel", cmd_cancel),
                CallbackQueryHandler(back_to_config_susp, pattern='^back_to_config_susp$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            CUSTOM_BODYKIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_bodykit),
                CommandHandler("cancel", cmd_cancel),
                CallbackQueryHandler(back_to_config_bodykit, pattern='^back_to_config_bodykit$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            CUSTOM_WHEELS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_wheels),
                CommandHandler("cancel", cmd_cancel),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            # Orders
            ORDER_REVIEW: [
                CallbackQueryHandler(confirm_order, pattern='^confirm_order$'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            ORDER_CONFIRMED: [
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            # Marketplace
            MARKETPLACE_LIST: [
                CallbackQueryHandler(show_car_detail, pattern='^mp_car_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            MARKETPLACE_DETAIL: [
                CallbackQueryHandler(show_car_photos, pattern='^mp_photos$'),
                CallbackQueryHandler(show_next_photo, pattern='^mp_next_photo$'),
                CallbackQueryHandler(show_prev_photo, pattern='^mp_prev_photo$'),
                CallbackQueryHandler(start_inquiry, pattern='^mp_inquire$'),
                CallbackQueryHandler(show_marketplace_list, pattern='^mp_list$'),
                CallbackQueryHandler(show_car_detail, pattern='^mp_car_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            MARKETPLACE_INQUIRY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_inquiry),
                CommandHandler("cancel", cmd_cancel),
                CallbackQueryHandler(show_car_detail, pattern='^mp_car_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            # Admin
            ADMIN_AUTH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_auth),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            ADMIN_MENU: [
                CallbackQueryHandler(admin_menu_cb, pattern='^admin_(all|new|progress|stats|back)_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            ADMIN_ORDER_LIST: [
                CallbackQueryHandler(handle_order_action, pattern='^admin_order_'),
                CallbackQueryHandler(admin_menu_cb, pattern='^admin_(all|new|progress|back)_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
            ADMIN_ORDER_DETAIL: [
                CallbackQueryHandler(handle_order_action, pattern='^admin_(order_|set_status_)'),
                CallbackQueryHandler(admin_menu_cb, pattern='^admin_back_'),
                CallbackQueryHandler(back_to_main_handler, pattern='^back_to_main$'),
            ],
        },
        fallbacks=[],
    )
    app.add_handler(conv)
    app.add_error_handler(lambda u, c: logger.error(f"Error: {c.error}"))

    logger.info("🤖 Bot started!")
    app.run_polling(drop_pending_updates=True)


# ==================== Back navigation helpers ====================

async def back_to_config_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['config'] = {}
    keyboard = [[InlineKeyboardButton(f"{c['name']} ({c['years']})", callback_data=f"car_{c['id']}")] for c in CARS]
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")])
    await update.callback_query.edit_message_text("🚗 Select a car:", parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_CAR


async def back_to_config_engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    car = context.user_data.get('config', {}).get('car')
    if not car:
        return await back_to_config_car(update, context)
    cid = car['id']
    engines = ENGINES.get(cid, [])
    keyboard = [[InlineKeyboardButton(e['name'], callback_data=f"engine_{e['id']}")] for e in engines]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_car")])
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")])
    await update.callback_query.edit_message_text(f"⚙️ Select an engine for {car['name']}:", parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_ENGINE


async def back_to_config_susp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(s['name'], callback_data=f"susp_{sid}")] for sid, s in SUSPENSIONS.items()]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_engine")])
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")])
    await update.callback_query.edit_message_text("🔧 Select suspension:", reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_SUSPENSION


async def back_to_config_bodykit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(bk['name'], callback_data=f"bodykit_{bk['id']}")] for bk in BODYKITS]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_config_susp")])
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")])
    await update.callback_query.edit_message_text("🎨 Select a bodykit:", reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_BODYKIT


if __name__ == '__main__':
    main()
