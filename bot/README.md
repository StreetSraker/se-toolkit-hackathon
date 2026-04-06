# JDM Car Configurator Bot 🚗

Telegram bot for configuring and ordering classic JDM cars from the 90s and 00s with custom specifications.

## Features

- **Car Selection**: Choose from 10 legendary JDM cars (Supra, Skyline, RX-7, NSX, Silvia, etc.)
- **Engine Configuration**: Select engine setups from stock to high-performance builds
- **Suspension Setup**: 5 different suspension configurations (Street, Sport, Drift, Track, Stance)
- **Bodykit Selection**: 4 bodykit options (Rocket Bunny, VARIS, N1, Pandem)
- **Wheel Options**: 11 iconic JDM wheel choices (TE37, CE28, RPF1, etc.)
- **Order System**: Complete order flow with configuration summary

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your bot token from [@BotFather](https://t.me/BotFather)

3. **Run the bot**:
   ```bash
   python -m bot.main
   ```

## Bot Commands

- `/start` - Start the bot and see main menu
- `/config` - Launch car configurator
- `/order` - Place an order with current configuration
- `/admin` - Service center panel (requires admin ID setup)
- `/cancel` - Cancel current operation
- `/help` - Show help information

## Admin Panel Access

Anyone can access the admin panel with a password:

1. Click "🔧 Service Panel" in the main menu or use `/admin`
2. Enter the password (default: `service2024`)
3. Change the password in `.env` file or `bot/handlers/admin.py`:
   ```python
   ADMIN_PASSWORD = "your_secure_password"
   ```

## Admin Panel Features

- View all orders with filtering by status
- Detailed order view with full configuration
- Change order status (New → In Progress → Completed/Cancelled)
- Order statistics and popular car analytics

## Project Structure

```
bot/
├── main.py                    # Main bot entry point
├── data/
│   └── car_config_data.py    # Car, engine, suspension, bodykit, wheels data
└── handlers/
    ├── car_config.py         # Car configuration conversation handler
    └── order.py              # Order processing handler
```

## Configuration Flow

1. **Select Car** → Choose from 10 classic JDM vehicles
2. **Select Engine** → Pick engine setup (4 options per car)
3. **Select Suspension** → 5 suspension presets
4. **Select Bodykit** → 4 bodykit styles
5. **Select Wheels** → 11 wheel options
6. **Review & Order** → Summary and order placement

## Tech Stack

- Python 3.8+
- python-telegram-bot v20.7
- python-dotenv for environment variables

## Environment Variables

- `BOT_TOKEN` - Your Telegram bot token from BotFather

## Development

To add more cars, engines, or other options, edit `bot/data/car_config_data.py`.

## License

MIT
