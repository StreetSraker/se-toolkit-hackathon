# JDM Car Configurator - Deployment Guide 🚗

Complete guide for deploying the Telegram bot and web applications.

---

## 📋 Prerequisites

### Required Software
- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git** (for cloning the repository)

### Required Accounts
- **Telegram account** (to create a bot via @BotFather)
- **Server/VM** running Ubuntu 24.04 (or any Linux distribution with Docker support)

---

## 🚀 Quick Start (Docker Deployment)

### Step 1: Install Docker (Ubuntu 24.04)

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

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

### Step 3: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit the .env file
nano .env
```

**Required configurations in `.env`:**

```bash
# Telegram Bot Token (REQUIRED)
# Get this from @BotFather on Telegram
BOT_TOKEN=your_actual_bot_token_here

# Admin Password (change for production!)
ADMIN_PASSWORD=service2024

# Secret Keys (use strong random strings in production)
SECRET_KEY=jdm-config-secret-key-2024
ADMIN_SECRET_KEY=jdm-admin-secret-key-2024

# Debug Mode (set to False in production)
FLASK_DEBUG=False

# Ports (default values)
PORT=5000
ADMIN_PORT=5001
```

### Step 4: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot (e.g., "JDM Configurator")
   - Choose a username (must end in 'bot', e.g., "jdm_config_bot")
4. Copy the **bot token** provided
5. Paste it into your `.env` file as `BOT_TOKEN`

### Step 5: Deploy with Docker Compose

```bash
# Build and start all services
./deploy.sh

# OR using docker compose directly
docker compose up -d --build
```

### Step 6: Verify Deployment

```bash
# Check if all containers are running
docker compose ps

# View logs from all services
docker compose logs -f

# Or view specific service logs
docker compose logs -f bot
docker compose logs -f client
docker compose logs -f admin
```

---

## 🌐 Accessing the Services

### After successful deployment:

| Service | Local Access | External Access |
|---------|-------------|-----------------|
| **Client Website** | http://localhost:5000 | http://YOUR_SERVER_IP:5000 |
| **Admin Panel** | http://localhost:5001 | http://YOUR_SERVER_IP:5001 |
| **Telegram Bot** | Automatic (polling) | Automatic (polling) |

### Get your server IP:

```bash
# On Linux
ip addr show | grep "inet " | grep -v 127.0.0.1

# Or use curl to get public IP
curl ifconfig.me
```

---

## 🔧 Managing Services

### Start Services

```bash
# Start all services
docker compose up -d

# Or use the deployment script
./deploy.sh
```

### Stop Services

```bash
# Stop all services
docker compose down

# Or use the stop script
./stop_all.sh
```

### Restart Services

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart bot
docker compose restart client
docker compose restart admin
```

### View Logs

```bash
# View all logs
docker compose logs -f

# View specific service
docker compose logs -f bot
docker compose logs -f client
docker compose logs -f admin

# Or use the logs script
./logs.sh all
./logs.sh bot
./logs.sh client
./logs.sh admin
```

### Update Services

```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose up -d --build
```

---

## 📊 Service Architecture

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
│  │      (orders.json storage)         │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Services:

1. **jdm-bot** (Telegram Bot)
   - Polls Telegram API for messages
   - No exposed ports (uses outbound connections)
   - Handles bot commands and conversations

2. **jdm-client** (Client Website)
   - Port 5000
   - Public-facing car configurator
   - REST API for car data and order creation

3. **jdm-admin** (Admin Panel)
   - Port 5001
   - Password-protected service center
   - Order management and statistics

### Data Persistence:

All services share a Docker volume (`bot_data`) that stores:
- `orders.json` - All order data
- Configuration data (read-only from code)

---

## 🔐 Security Considerations

### For Production Deployment:

1. **Change Admin Password:**
   ```bash
   # In .env file
   ADMIN_PASSWORD=your_strong_password_here
   ```

2. **Use Strong Secret Keys:**
   ```bash
   # Generate random secret key
   python3 -c "import secrets; print(secrets.token_hex(32))"
   
   # Update in .env
   SECRET_KEY=<generated_key>
   ADMIN_SECRET_KEY=<generated_key>
   ```

3. **Disable Debug Mode:**
   ```bash
   FLASK_DEBUG=False
   ```

4. **Use HTTPS (Recommended):**
   - Set up Nginx as reverse proxy
   - Use Let's Encrypt for SSL certificates
   
   Example Nginx configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Firewall Configuration:**
   ```bash
   # Allow only necessary ports
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP (if using reverse proxy)
   sudo ufw allow 443/tcp   # HTTPS (if using SSL)
   sudo ufw enable
   ```

---

## 🐛 Troubleshooting

### Bot not starting?

**Problem:** `InvalidToken` error in logs

**Solution:**
```bash
# Check bot logs
docker compose logs bot

# Verify BOT_TOKEN in .env
cat .env | grep BOT_TOKEN

# Make sure token is valid from @BotFather
# Restart bot after fixing token
docker compose restart bot
```

### Website not accessible?

**Problem:** Can't reach http://localhost:5000

**Solution:**
```bash
# Check if container is running
docker compose ps

# Check container logs
docker compose logs client

# Verify port is listening
docker port jdm-client

# Check firewall
sudo ufw status
sudo ufw allow 5000/tcp
sudo ufw allow 5001/tcp
```

### Orders not persisting?

**Problem:** Orders disappear after restart

**Solution:**
```bash
# Check if volume is mounted
docker inspect jdm-client | grep -A 5 Mounts

# Verify orders.json exists
docker exec jdm-client cat /app/bot/data/orders.json | head -20
```

### Need to reset everything?

```bash
# Stop and remove everything
docker compose down -v

# Rebuild from scratch
docker compose up -d --build
```

---

## 📝 Alternative: Manual Deployment (Without Docker)

If you prefer to run the services directly:

### Step 1: Install Python Dependencies

```bash
cd /root/se-toolkit-hackathon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your settings
```

### Step 3: Start Services

```bash
# Terminal 1 - Telegram Bot
python -m bot.main

# Terminal 2 - Client Website
python web/client_app.py

# Terminal 3 - Admin Website
python web/admin_app.py
```

### Step 4: Run as Background Services (systemd)

Create service files:

**`/etc/systemd/system/jdm-bot.service`:**
```ini
[Unit]
Description=JDM Configurator Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/se-toolkit-hackathon
Environment=PATH=/root/se-toolkit-hackathon/venv/bin
ExecStart=/root/se-toolkit-hackathon/venv/bin/python -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**`/etc/systemd/system/jdm-client.service`:**
```ini
[Unit]
Description=JDM Configurator Client Website
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/se-toolkit-hackathon
Environment=PATH=/root/se-toolkit-hackathon/venv/bin
ExecStart=/root/se-toolkit-hackathon/venv/bin/python web/client_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**`/etc/systemd/system/jdm-admin.service`:**
```ini
[Unit]
Description=JDM Configurator Admin Website
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/se-toolkit-hackathon
Environment=PATH=/root/se-toolkit-hackathon/venv/bin
ExecStart=/root/se-toolkit-hackathon/venv/bin/python web/admin_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable jdm-bot jdm-client jdm-admin
sudo systemctl start jdm-bot jdm-client jdm-admin

# Check status
sudo systemctl status jdm-bot
sudo systemctl status jdm-client
sudo systemctl status jdm-admin
```

---

## 📞 Support

If you encounter issues:

1. Check the logs: `docker compose logs -f`
2. Verify your `.env` configuration
3. Ensure all required ports are available
4. Check Docker is running: `docker --version`

---

## 🎯 Post-Deployment Checklist

- [ ] Bot token configured in `.env`
- [ ] All three containers running (`docker compose ps`)
- [ ] Client website accessible (http://YOUR_IP:5000)
- [ ] Admin panel accessible (http://YOUR_IP:5001)
- [ ] Bot responds to `/start` command on Telegram
- [ ] Can create order via website
- [ ] Can view order in admin panel
- [ ] Admin password changed from default
- [ ] Debug mode disabled (for production)
- [ ] Firewall configured to allow necessary ports

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Deployed successfully? Great! Now you can:**
- Share the bot username with users
- Share client website URL: http://YOUR_IP:5000
- Share admin panel URL with staff: http://YOUR_IP:5001
- Monitor orders in real-time across all platforms
