# JDM Car Configurator - Web Application 🚗

Two separate web applications:
1. **Client Site** (port 5000) - For customers to configure cars and place orders
2. **Service Center Site** (port 5001) - For service staff to manage orders

---

## 🚗 Client Website (Port 5000)

**For:** Customers who want to configure and order JDM cars

**Features:**
- Car configurator wizard (6 steps)
- View personal orders
- About service info

**Access:**
- Local: http://localhost:5000
- From other devices: http://YOUR_IP:5000

**Run:**
```bash
run_client.bat
```

---

## 🔧 Service Center Website (Port 5001)

**For:** Service center staff to manage orders

**Features:**
- Password-protected login
- Dashboard with order overview
- Full order management (view details, change status)
- Statistics and analytics

**Access:**
- Local: http://localhost:5001
- From other devices: http://YOUR_IP:5001

**Run:**
```bash
run_admin.bat
```

**Default Password:** `service2024`

---

## 📁 Project Structure

```
web/
├── client_app.py             # Client Flask app (port 5000)
├── admin_app.py              # Admin Flask app (port 5001)
├── templates/                # Client HTML templates
│   ├── index.html
│   ├── configurator.html
│   └── orders.html
├── admin_templates/          # Admin HTML templates (separate)
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_orders.html
│   └── admin_stats.html
└── static/                   # Shared static files
    ├── css/
    │   └── style.css
    └── js/
        ├── main.js
        ├── configurator.js
        ├── orders.js
        ├── admin_auth.js
        ├── admin_dashboard.js
        ├── admin_orders.js
        └── admin_stats.js
```

---

## 🚀 Quick Start

### 1. Start Client Site
```bash
double-click: run_client.bat
```
Open browser: http://localhost:5000

### 2. Start Service Center Site
```bash
double-click: run_admin.bat
```
Open browser: http://localhost:5001

### 3. Open Firewall (for external access)
```bash
right-click run_admin.bat → Run as Administrator
```

---

## 🌐 Access from Other Devices

### Get your IP:
```cmd
ipconfig | findstr /i "IPv4"
```

Your IP: `192.168.0.118`

### From phone/tablet/other PC:
- Client: **http://192.168.0.118:5000**
- Service Center: **http://192.168.0.118:5001**

---

## 🔐 Security

- Client site: No authentication needed (public)
- Service Center: Password protected
- Both share the same orders database (orders.json)

---

## 🛣️ API Endpoints

### Client API (Port 5000)
- `GET /api/cars` - Get all cars
- `GET /api/engines/<car_id>` - Get engines
- `GET /api/suspensions` - Get suspensions
- `GET /api/bodykits` - Get bodykits
- `GET /api/wheels` - Get wheels
- `GET /api/orders` - Get all orders
- `POST /api/orders` - Create order

### Service Center API (Port 5001)
- `POST /api/admin/login` - Login
- `POST /api/admin/logout` - Logout
- `GET /api/admin/check` - Check auth
- `GET /api/orders` - Get all orders (auth required)
- `GET /api/orders/<id>` - Get order details
- `PUT /api/orders/<id>/status` - Update status
- `GET /api/stats` - Get statistics

---

## 💡 Key Differences

| Feature | Client Site | Service Center |
|---------|-------------|----------------|
| **Port** | 5000 | 5001 |
| **Access** | Public | Password protected |
| **Purpose** | Configure & order | Manage orders |
| **Users** | Customers | Staff |
| **Features** | Configurator, My Orders | Dashboard, All Orders, Stats |

---

## 📊 Shared Data

Both applications share:
- Same car database (`bot/data/car_config_data.py`)
- Same orders file (`bot/data/orders.json`)
- Same storage functions

Orders placed on client site appear immediately in service center!
