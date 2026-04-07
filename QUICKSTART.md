# Quick Start Guide - JDM Configurator 🚗

Get your Telegram bot and websites running in 5 minutes!

---

## 🚀 Deploy in 3 Steps

### Step 1: Install Docker (if not installed)

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Configure Bot Token

```bash
# Copy environment file
cp .env.example .env

# Edit and add your bot token
nano .env
```

**Get your bot token:**
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy the token to `.env` file: `BOT_TOKEN=your_token_here`

### Step 3: Deploy

```bash
./deploy.sh
```

**Done!** ✅

---

## 🌐 Access Your Services

| Service | URL | Description |
|---------|-----|-------------|
| 🚗 Client Website | `http://YOUR_IP:5000` | Car configurator for customers |
| 🔧 Admin Panel | `http://YOUR_IP:5001` | Order management (Password: `service2024`) |
| 🤖 Telegram Bot | Search on Telegram | Bot interface |

**Find your IP:**
```bash
curl ifconfig.me
```

---

## 📋 Common Commands

### Manage Services

```bash
# Start all services
./deploy.sh

# Stop all services
./stop_all.sh

# View logs
./logs.sh all

# View bot logs only
./logs.sh bot

# Restart a service
docker compose restart bot
```

### Check Status

```bash
# See running containers
docker compose ps

# Check logs
docker compose logs -f
```

---

## 🔧 Troubleshooting

### Bot not working?
```bash
# Check logs
docker compose logs bot

# Most common issue: Invalid token
# Fix: Get correct token from @BotFather and update .env
# Then restart: docker compose restart bot
```

### Websites not accessible?
```bash
# Check if containers are running
docker compose ps

# Check firewall
sudo ufw allow 5000/tcp
sudo ufw allow 5001/tcp
```

### Need to reset everything?
```bash
docker compose down -v
docker compose up -d --build
```

---

## 📱 What You Get

### Telegram Bot Features:
- ✅ Car configuration wizard
- ✅ Engine, suspension, bodykit, wheels selection
- ✅ Order placement
- ✅ Admin panel (password protected)
- ✅ Order status tracking

### Client Website Features:
- ✅ Beautiful car configurator UI
- ✅ Step-by-step configuration wizard
- ✅ View personal orders
- ✅ Mobile responsive

### Admin Panel Features:
- ✅ Password-protected access
- ✅ View all orders
- ✅ Change order status
- ✅ Statistics and analytics
- ✅ Popular cars tracking

---

## 🎯 Next Steps

1. **Test the bot:** Open Telegram, find your bot, send `/start`
2. **Test websites:** Open browser, go to the URLs above
3. **Change admin password:** Edit `.env` file, set strong password
4. **Share with users:** Give them bot username and website URL

---

## 📚 Need More Help?

See full documentation: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Enjoy your JDM Configurator! 🏎️**
