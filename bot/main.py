"""Main bot application - Client order tracking only"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from bot.data.storage import get_order
from bot.data.users_storage import register_user, authenticate_user, get_user_by_username
from bot.data.services_storage import get_service

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    MAIN_MENU,
    AUTH_USERNAME,
    AUTH_PASSWORD,
    REG_USERNAME,
    REG_PASSWORD,
    REG_TELEGRAM,
    REG_PHONE,
    REG_EMAIL,
    ORDER_DETAIL,
) = range(9)

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

def _main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 My Orders", callback_data="my_orders")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ])


async def _edit(update: Update, text: str, **kwargs):
    """Edit message or reply"""
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, **kwargs)
        except Exception:
            if update.callback_query.message:
                await update.callback_query.message.reply_text(text, **kwargs)
    elif update.effective_message:
        await update.effective_message.reply_text(text, **kwargs)


def _get_user_from_session(context):
    """Get user info from session or return None"""
    return context.user_data.get('auth_user')


async def _require_auth(update, context):
    """Check if user is authenticated, redirect to login if not"""
    user = _get_user_from_session(context)
    if user:
        return True
    text = (
        "🔐 <b>Authentication required</b>\n\n"
        "Please log in or register to continue.\n\n"
        "Choose an option:"
    )
    kb = [
        [InlineKeyboardButton("🔑 Login", callback_data="auth_login")],
        [InlineKeyboardButton("📝 Register", callback_data="auth_register")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return False


# ==================== Commands ====================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /start command"""
    user = _get_user_from_session(context)
    if user:
        return await show_main_menu(update, context)
    else:
        text = (
            f"👋 Hello, {update.effective_user.first_name}!\n\n"
            f"🏎️ <b>JDM Config Bot</b>\n\n"
            f"Track your car order status and see which service is working on it.\n\n"
            f"Please log in or register to continue:"
        )
        kb = [
            [InlineKeyboardButton("🔑 Login", callback_data="auth_login")],
            [InlineKeyboardButton("📝 Register", callback_data="auth_register")],
            [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        ]
        await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
        return MAIN_MENU


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel current operation"""
    await update.message.reply_text("❌ Cancelled.")
    context.user_data.clear()
    return await cmd_start(update, context)


# ==================== Main Menu ====================

async def show_main_menu(update, context) -> int:
    """Show main menu for authenticated user"""
    user = _get_user_from_session(context)
    if not user:
        return await cmd_start(update, context)

    from bot.data.storage import get_all_orders
    all_orders = get_all_orders()
    my_orders = [o for o in all_orders if o.get('user_id') == user['id']]

    text = (
        f"👋 Hello, <b>{user['username']}</b>!\n\n"
        f"📊 You have <b>{len(my_orders)}</b> order(s).\n\n"
        f"Choose an action:"
    )
    await _edit(update, text, parse_mode='HTML', reply_markup=_main_menu_keyboard())
    return MAIN_MENU


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle main menu callbacks"""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "about":
        await _edit(update,
            "ℹ️ <b>About the Service</b>\n\n"
            "We help order cars from the 90s and 00s with custom configuration:\n\n"
            "• Engine selection and tuning\n"
            "• Suspension setup\n"
            "• Bodykit installation\n"
            "• Wheel selection\n\n"
            "All work is performed by professional technicians experienced with JDM vehicles.\n\n"
            "🌐 <b>Web client:</b> use our website to configure and order cars.\n"
            "🤖 <b>This bot:</b> track your order status and see which service is working on it.",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]])
        )
        return MAIN_MENU

    elif data == "my_orders":
        return await show_my_orders(update, context)

    elif data == "back_to_main":
        return await show_main_menu(update, context)

    return MAIN_MENU


# ==================== Authentication ====================

async def show_login_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show login form"""
    text = (
        "🔑 <b>Login</b>\n\n"
        "Enter your <b>username</b>:"
    )
    await _edit(update, text, parse_mode='HTML', reply_markup=ForceReply())
    return AUTH_USERNAME


async def handle_auth_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle username input for login"""
    username = update.message.text.strip()
    if not username:
        await update.message.reply_text("❌ Please enter a valid username.")
        return AUTH_USERNAME

    context.user_data['auth_temp_username'] = username
    await update.message.reply_text(
        "Enter your <b>password</b>:",
        parse_mode='HTML',
        reply_markup=ForceReply()
    )
    return AUTH_PASSWORD


async def handle_auth_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password input for login"""
    password = update.message.text.strip()
    username = context.user_data.get('auth_temp_username', '')

    user = authenticate_user(username, password)
    if not user:
        await update.message.reply_text(
            "❌ <b>Invalid username or password.</b>\n\n"
            "Try again or register a new account.\n\n"
            "Enter your <b>username</b>:",
            parse_mode='HTML',
            reply_markup=ForceReply()
        )
        return AUTH_USERNAME

    # Save to session
    context.user_data['auth_user'] = {
        'id': user['id'],
        'username': user['username'],
    }
    context.user_data.pop('auth_temp_username', None)

    await update.message.reply_text(
        f"✅ <b>Welcome, {user['username']}!</b>\n\n"
        f"You are now logged in.",
        parse_mode='HTML'
    )
    return await show_main_menu(update, context)


# ==================== Registration ====================

async def show_register_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show registration form"""
    text = (
        "📝 <b>Registration</b>\n\n"
        "Choose a <b>username</b>:"
    )
    await _edit(update, text, parse_mode='HTML', reply_markup=ForceReply())
    return REG_USERNAME


async def handle_reg_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle username input for registration"""
    username = update.message.text.strip()
    if not username or len(username) < 3:
        await update.message.reply_text("❌ Username must be at least 3 characters.\n\nEnter your <b>username</b>:", parse_mode='HTML', reply_markup=ForceReply())
        return REG_USERNAME

    # Check if already exists
    existing = get_user_by_username(username)
    if existing:
        await update.message.reply_text("❌ Username already taken.\n\nEnter a different <b>username</b>:", parse_mode='HTML', reply_markup=ForceReply())
        return REG_USERNAME

    context.user_data['reg_data'] = {'username': username.lower()}
    context.user_data['reg_step'] = 'password'
    await update.message.reply_text(
        "Choose a <b>password</b> (min 4 characters):",
        parse_mode='HTML',
        reply_markup=ForceReply()
    )
    return REG_PASSWORD


async def handle_reg_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password input for registration"""
    password = update.message.text.strip()
    if len(password) < 4:
        await update.message.reply_text("❌ Password must be at least 4 characters.\n\nEnter your <b>password</b>:", parse_mode='HTML', reply_markup=ForceReply())
        return REG_PASSWORD

    context.user_data['reg_data']['password'] = password
    context.user_data['reg_step'] = 'telegram'
    await update.message.reply_text(
        "Enter your <b>Telegram username</b> (optional, e.g. @john):\n\n"
        "Or send /skip to skip.",
        parse_mode='HTML',
        reply_markup=ForceReply()
    )
    return REG_TELEGRAM


async def handle_reg_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle telegram input for registration"""
    context.user_data['reg_data']['telegram'] = update.message.text.strip()
    context.user_data['reg_step'] = 'phone'
    await update.message.reply_text(
        "Enter your <b>phone number</b> (optional, e.g. +1234567890):\n\n"
        "Or send /skip to skip.",
        parse_mode='HTML',
        reply_markup=ForceReply()
    )
    return REG_PHONE


async def handle_reg_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone input for registration"""
    context.user_data['reg_data']['phone'] = update.message.text.strip()
    context.user_data['reg_step'] = 'email'
    await update.message.reply_text(
        "Enter your <b>email</b> (optional):\n\n"
        "Or send /skip to skip.",
        parse_mode='HTML',
        reply_markup=ForceReply()
    )
    return REG_EMAIL


async def handle_reg_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle email input for registration"""
    context.user_data['reg_data']['email'] = update.message.text.strip()
    return await complete_registration(update, context)


async def handle_reg_skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle skip in registration"""
    reg_step = context.user_data.get('reg_step', 'telegram')

    if reg_step == 'telegram':
        context.user_data['reg_data']['telegram'] = ''
        context.user_data['reg_step'] = 'phone'
        await update.message.reply_text(
            "Enter your <b>phone number</b> (optional):\n\nOr send /skip to skip.",
            parse_mode='HTML',
            reply_markup=ForceReply()
        )
        return REG_PHONE
    elif reg_step == 'phone':
        context.user_data['reg_data']['phone'] = ''
        context.user_data['reg_step'] = 'email'
        await update.message.reply_text(
            "Enter your <b>email</b> (optional):\n\nOr send /skip to skip.",
            parse_mode='HTML',
            reply_markup=ForceReply()
        )
        return REG_EMAIL
    elif state == REG_EMAIL:
        context.user_data['reg_data']['email'] = ''
        return await complete_registration(update, context)
    return REG_TELEGRAM


async def complete_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Complete user registration"""
    reg_data = context.user_data.get('reg_data', {})

    user = register_user(reg_data)
    if not user:
        await update.message.reply_text("❌ Registration failed. Username may already be taken.\n\nTry /start to log in instead.")
        context.user_data.pop('reg_data', None)
        return await cmd_start(update, context)

    # Auto-login
    context.user_data['auth_user'] = {
        'id': user['id'],
        'username': user['username'],
    }
    context.user_data.pop('reg_data', None)

    await update.message.reply_text(
        f"✅ <b>Registration successful!</b>\n\n"
        f"Welcome, <b>{user['username']}</b>!\n"
        f"Your user ID: <code>{user['id']}</code>\n\n"
        f"You can now track your orders.",
        parse_mode='HTML'
    )
    return await show_main_menu(update, context)


# ==================== My Orders ====================

async def show_my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show user's orders"""
    user = _get_user_from_session(context)
    if not user:
        return await _require_auth(update, context)

    from bot.data.storage import get_all_orders
    all_orders = get_all_orders()
    my_orders = [o for o in all_orders if o.get('user_id') == user['id']]

    if not my_orders:
        text = (
            "📋 <b>You have no orders yet.</b>\n\n"
            "Use our website to configure and order a car:\n"
            "🌐 Open the web client to get started."
        )
        kb = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]]
        await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
        return MAIN_MENU

    text = f"📋 <b>Your Orders ({len(my_orders)})</b>\n\n"
    kb = []
    for o in my_orders[:15]:
        car = o.get('car', {}).get('name', 'N/A')
        st = o.get('status', 'new')
        text += f"{STATUS_EMOJI.get(st, '📋')} <code>{o['id']}</code> — {car}\n"
        text += f"   Status: {STATUS_NAMES.get(st, st)}\n"

        # Show assigned service
        claimed_by = o.get('claimed_by')
        if claimed_by:
            svc = get_service(claimed_by)
            if svc:
                text += f"   Service: {svc['name']}\n"
        else:
            text += f"   Service: ⏳ Not assigned yet\n"

        text += f"   Date: {o.get('created_at', '')}\n\n"

        kb.append([InlineKeyboardButton(
            f"{STATUS_EMOJI.get(st, '📋')} {o['id']} — {car[:30]}",
            callback_data=f"order_{o['id']}"
        )])

    if len(my_orders) > 15:
        text += f"...and {len(my_orders) - 15} more\n\n"

    kb.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])

    await _edit(update, text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return MAIN_MENU


async def show_order_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, order_id) -> int:
    """Show detailed order info"""
    user = _get_user_from_session(context)
    if not user:
        return await _require_auth(update, context)

    o = get_order(order_id)
    if not o:
        await update.callback_query.edit_message_text("❌ Order not found.")
        return MAIN_MENU

    # Verify ownership
    if o.get('user_id') != user['id']:
        await update.callback_query.edit_message_text("❌ This order does not belong to you.")
        return MAIN_MENU

    car = o.get('car', {})
    text = (
        f"📦 <b>Order {o['id']}</b> | {STATUS_NAMES.get(o.get('status','new'),'')}\n"
        f"Created: {o.get('created_at','')}\n\n"
        f"🚗 {car.get('name','N/A')} ({car.get('years','')})\n"
        f"⚙️ {o.get('engine',{}).get('name','N/A')} — {o.get('engine',{}).get('power','')}\n"
        f"🔧 {o.get('suspension',{}).get('name','N/A')}\n"
        f"🎨 {o.get('bodykit',{}).get('name','N/A')}\n"
        f"🛞 {o.get('wheels',{}).get('name','N/A')}\n"
    )

    if o.get('contacts'):
        text += f"\n📞 Contact: {o['contacts']}\n"

    # Show assigned service info
    claimed_by = o.get('claimed_by')
    if claimed_by:
        svc = get_service(claimed_by)
        if svc:
            text += f"\n🔧 <b>Service:</b> {svc['name']}\n"
            if svc.get('telegram_username'):
                text += f"   Telegram: {svc['telegram_username']}\n"
            if svc.get('phone'):
                text += f"   Phone: {svc['phone']}\n"
            if svc.get('specialties'):
                text += f"   Specialties: {', '.join(svc['specialties'])}\n"
        text += f"\n📋 Claimed at: {o.get('claimed_at', 'N/A')}\n"
    else:
        text += "\n⏳ <b>Service:</b> Not assigned yet. A service will claim your order soon.\n"

    # Status history
    history = o.get('status_history', [])
    if history:
        text += "\n📜 <b>History:</b>\n"
        for h in history:
            text += f"  {STATUS_EMOJI.get(h['status'],'📋')} {h['status']} — {h.get('by_name','System')} at {h['at']}\n"

    kb = [
        [InlineKeyboardButton("⬅️ Back to Orders", callback_data="my_orders")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")],
    ]
    await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    return ORDER_DETAIL


# ==================== Entry Point ====================

def build_application():
    """Build and return the application with handlers"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set")

    app = ApplicationBuilder().token(token).build()

    # Main conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', cmd_start),
            CommandHandler('cancel', cmd_cancel),
            CallbackQueryHandler(menu_handler, pattern='^(my_orders|about|back_to_main)$'),
            CallbackQueryHandler(show_login_form, pattern='^auth_login$'),
            CallbackQueryHandler(show_register_form, pattern='^auth_register$'),
            CallbackQueryHandler(lambda u, c: show_order_detail(u, c, u.callback_query.data.replace('order_', '')), pattern='^order_'),
        ],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(menu_handler, pattern='^(my_orders|about|back_to_main)$'),
                CallbackQueryHandler(lambda u, c: show_order_detail(u, c, u.callback_query.data.replace('order_', '')), pattern='^order_'),
            ],
            AUTH_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_auth_username),
            ],
            AUTH_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_auth_password),
            ],
            REG_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reg_username),
            ],
            REG_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reg_password),
            ],
            REG_TELEGRAM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reg_telegram),
                CommandHandler("skip", handle_reg_skip),
            ],
            REG_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reg_phone),
                CommandHandler("skip", handle_reg_skip),
            ],
            REG_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reg_email),
                CommandHandler("skip", handle_reg_skip),
            ],
            ORDER_DETAIL: [
                CallbackQueryHandler(menu_handler, pattern='^(my_orders|back_to_main)$'),
            ],
        },
        fallbacks=[
            CommandHandler('start', cmd_start),
            CommandHandler('cancel', cmd_cancel),
        ],
    )

    app.add_handler(conv_handler)

    return app


def main():
    """Run the bot"""
    application = build_application()
    print("🤖 JDM Client Bot starting...")
    print("📋 Client order tracking only — login, view orders, see service info")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
