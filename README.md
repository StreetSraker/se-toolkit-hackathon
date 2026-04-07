# JDM Car Configurator 🚗

A Telegram bot and web platform for ordering and configuring classic 90s/00s JDM cars with custom modifications.

---

## Demo

### Client Website - Car Configurator
![Car Configurator](Images/demo/configurator_demo.png)

### Client Website - Marketplace
![Marketplace](Images/demo/marketplace_demo.png)

### Admin Panel - Order Management
![Admin Panel](Images/demo/admin_demo.png)

### Telegram Bot
![Telegram Bot](Images/demo/bot_demo.png)

---

## Product Context

### End Users

- **Car Enthusiasts** — Fans of classic JDM cars (90s/00s era) who want to order and customize vehicles
- **Car Service Centers** — Technicians and shops that fulfill custom car build orders

### Problem

Enthusiasts of classic JDM cars lack a streamlined platform to:
- Browse available 90s/00s JDM models
- Configure custom builds (engine swaps, suspensions, bodykits, wheels)
- Place orders with service centers
- Track order progress

Service centers lack a centralized system to:
- Receive and manage custom build orders
- Claim jobs and communicate with clients
- Track statistics and workload

### Solution

A multi-platform system with:
- **Telegram Bot** — Quick access to order tracking and notifications
- **Client Website** — Interactive car configurator with step-by-step customization
- **Admin Panel** — Service center dashboard for order management and analytics

---

## Features

### Implemented ✅

#### Client Website (Port 5000)
- User registration and authentication
- Interactive car configurator with 10 JDM models:
  - Toyota Supra A80, Nissan Skyline R34 GT-R, Mazda RX-7 FD, Honda NSX
  - Nissan Silvia S15, Toyota Chaser JZX100, Honda Civic Type R EK9
  - Mitsubishi Lancer Evolution VI, Subaru Impreza WRX STI GC8, Toyota AE86
- Customization options:
  - **Engines** — 6 options per car (stock, built, stroker, swaps, custom)
  - **Suspensions** — 7 setups (stock, street, sport, drift, track, stance, custom)
  - **Bodykits** — 6 styles (stock, Rocket Bunny, VARIS, N1/Origin, Pandem, custom)
  - **Wheels** — 13 options (Rays Volk, Work, SSR, Advan, Enkei, BBS, OZ, etc.)
- 8 pre-configured preset builds (Drift, Track, Stance, Street, Rally, Touge)
- Order placement and tracking
- Marketplace for pre-modified cars for sale
- User profile management
- Mobile responsive design
- Internationalization (English & Russian)

#### Admin Panel (Port 5001)
- Service center registration and authentication
- Order management (view, claim, release, update status)
- Per-service data isolation
- Statistics and analytics (order counts, popular cars, conversion rates)
- Service management (register, edit, deactivate services)
- Marketplace management (add/edit/remove cars for sale, image uploads)
- Service profile management

#### Telegram Bot
- User registration and authentication
- Order listing with status tracking
- Order detail view with full configuration
- Assigned service contact information
- Status history timeline

#### Infrastructure
- Docker containerization (3 services)
- Shared persistent storage (JSON-based database)
- Deployment scripts
- Health checks for all services

### Not Yet Implemented 🚧

- Real-time order status notifications (push to Telegram)
- Payment processing integration
- Image upload for custom builds
- Advanced search and filtering in marketplace
- Order comments/messaging between client and service
- Email notifications
- Multi-language support in Telegram bot
- Admin role-based access control
- Export orders to PDF
- Car image gallery for configurator (SVG placeholders used)

---

## Usage

### For Car Enthusiasts

1. **Via Website:**
   - Open `http://YOUR_SERVER_IP:5000`
   - Register an account
   - Browse available JDM cars
   - Use the configurator to customize your build
   - Place an order and track its progress

2. **Via Telegram:**
   - Find the bot by its username
   - Send `/start` to begin
   - Register with username and password
   - View your orders and their status

### For Service Centers

1. Open `http://YOUR_SERVER_IP:5001`
2. Register as a service center
3. Browse available orders
4. Claim orders you want to fulfill
5. Update order status as work progresses
6. View statistics on your dashboard

### For Marketplace Sellers

1. Log in to the Admin Panel
2. Navigate to "For Sale" section
3. Add pre-modified cars with details and images
4. Manage listings (edit, remove)

---

## Deployment

### Prerequisites

- **OS:** Ubuntu 24.04 (or any Linux with Docker support)
- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git**
- **Telegram account** (to create a bot via @BotFather)

### Step-by-Step Instructions

#### 1. Install Docker

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

#### 3. Configure Environment Variables

```bash
cp .env.example .env
nano .env
```

Edit the `.env` file:

```bash
# Get this from @BotFather on Telegram
BOT_TOKEN=your_actual_bot_token_here

# Change for production!
ADMIN_PASSWORD=service2024

# Use strong random strings in production
SECRET_KEY=jdm-config-secret-key-2024
ADMIN_SECRET_KEY=jdm-admin-secret-key-2024

# Set to False in production
FLASK_DEBUG=False

PORT=5000
ADMIN_PORT=5001
```

#### 4. Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g., "JDM Configurator")
4. Choose a username (must end in `bot`, e.g., `jdm_config_bot`)
5. Copy the token and paste it into `.env`

#### 5. Deploy

```bash
# Build and start all services
./deploy.sh

# Or manually
docker compose up -d --build
```

#### 6. Verify Deployment

```bash
# Check all containers are running
docker compose ps

# View logs
docker compose logs -f
```

#### 7. Access Services

| Service | URL | Description |
|---------|-----|-------------|
| Client Website | `http://YOUR_IP:5000` | Car configurator for customers |
| Admin Panel | `http://YOUR_IP:5001` | Order management (Password: `service2024`) |
| Telegram Bot | Search on Telegram | Bot interface |

Get your server IP:
```bash
curl ifconfig.me
```

#### 8. Configure Firewall (if needed)

```bash
sudo ufw allow 5000/tcp
sudo ufw allow 5001/tcp
```

### Managing Services

```bash
# Stop all services
docker compose down

# Restart all services
docker compose restart

# Restart specific service
docker compose restart bot

# View logs
docker compose logs -f bot
./logs.sh all

# Update and rebuild
git pull
docker compose up -d --build

# Complete reset (removes data)
docker compose down -v
docker compose up -d --build
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Network                  │
│                                         │
│  ┌──────────────┐                       │
│  │  jdm-bot     │ ← Telegram Bot        │
│  │  (Polling)   │    Polls Telegram API │
│  └──────┬───────┘                       │
│         │                               │
│  ┌──────┴───────┐  ┌──────────────────┐ │
│  │ jdm-client   │  │  jdm-admin       │ │
│  │ Port 5000    │  │  Port 5001       │ │
│  │ (Public)     │  │  (Password)      │ │
│  └──────┬───────┘  └──────┬───────────┘ │
│         │                  │             │
│  ┌──────┴──────────────────┴──────────┐ │
│  │      Shared Volume: bot_data       │ │
│  │      (JSON storage)                │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Services

1. **jdm-bot** — Telegram bot (polling-based, no exposed port)
2. **jdm-client** — Client website (Port 5000)
3. **jdm-admin** — Admin panel (Port 5001)

### Data Storage

JSON-based persistent storage shared via Docker volume:
- `orders.json` — All order data
- `users.json` — Client user accounts
- `services.json` — Service center accounts
- `for_sale_cars.json` — Marketplace listings

---

## Tech Stack

- **Backend:** Python 3.11, Flask 3.0+, python-telegram-bot 21.0+
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Containerization:** Docker + Docker Compose
- **Storage:** JSON files (file-based database)
- **Internationalization:** English & Russian

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
