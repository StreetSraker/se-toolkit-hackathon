// Admin Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
    loadDashboard();
});

async function checkAdminAuth() {
    try {
        const response = await fetch('/api/admin/check');
        const data = await response.json();
        
        if (!data.is_admin) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error checking admin auth:', error);
    }
}

async function handleLogout() {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

async function loadDashboard() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.getElementById('statTotal').textContent = stats.total;
        document.getElementById('statNew').textContent = stats.new;
        document.getElementById('statProgress').textContent = stats.in_progress;
        document.getElementById('statCompleted').textContent = stats.completed;
        document.getElementById('statCancelled').textContent = stats.cancelled;
        
        // Load recent orders
        loadRecentOrders();
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadRecentOrders() {
    const container = document.getElementById('recentOrders');
    
    try {
        const response = await fetch('/api/orders');
        const orders = await response.json();
        
        if (orders.length === 0) {
            container.innerHTML = '<p class="loading">📋 Заказов нет</p>';
            return;
        }
        
        displayOrders(orders.slice(0, 5), container);
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="loading">Ошибка при загрузке заказов</p>';
    }
}

function displayOrders(orders, container) {
    const statusNames = {
        'new': '🆕 Новый',
        'in_progress': '🔧 В работе',
        'completed': '✅ Выполнен',
        'cancelled': '❌ Отменён'
    };
    
    const statusClasses = {
        'new': 'status-new',
        'in_progress': 'status-in_progress',
        'completed': 'status-completed',
        'cancelled': 'status-cancelled'
    };
    
    container.innerHTML = orders.map(order => {
        const carName = order.car?.name || 'N/A';
        const username = order.username || 'Unknown';
        const status = order.status || 'new';
        const statusName = statusNames[status] || status;
        const statusClass = statusClasses[status] || 'status-new';
        
        return `
            <div class="order-card" onclick="window.location.href='/orders'">
                <div class="order-header">
                    <div>
                        <span class="order-id">${order.id}</span>
                        <span style="color: #a0a0a0; margin-left: 10px;">— ${carName}</span>
                    </div>
                    <span class="order-status ${statusClass}">${statusName}</span>
                </div>
                <div class="order-details">
                    <div><strong>👤</strong> ${username}</div>
                    <div><strong>⚙️</strong> ${order.engine?.name || 'N/A'}</div>
                </div>
                <div class="order-date">
                    Создан: ${order.created_at}
                </div>
            </div>
        `;
    }).join('');
}
