// Orders Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    loadOrders();
});

async function loadOrders() {
    const container = document.getElementById('ordersList');
    
    try {
        const response = await fetch('/api/orders');
        const orders = await response.json();
        
        if (orders.length === 0) {
            container.innerHTML = `
                <div class="info-box">
                    <h3>📋 У вас пока нет заказов</h3>
                    <p>Сначала настройте автомобиль через Конфигуратор.</p>
                    <a href="/configurator" class="btn btn-primary" style="margin-top: 20px;">🚗 Конфигуратор</a>
                </div>
            `;
            return;
        }
        
        displayOrders(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="loading">Ошибка при загрузке заказов</p>';
    }
}

function displayOrders(orders) {
    const container = document.getElementById('ordersList');
    
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
        const status = order.status || 'new';
        const statusName = statusNames[status] || status;
        const statusClass = statusClasses[status] || 'status-new';
        
        return `
            <div class="order-card">
                <div class="order-header">
                    <div>
                        <span class="order-id">${order.id}</span>
                        <span style="color: #a0a0a0; margin-left: 10px;">— ${carName}</span>
                    </div>
                    <span class="order-status ${statusClass}">${statusName}</span>
                </div>
                <div class="order-details">
                    <div><strong>⚙️ Двигатель:</strong> ${order.engine?.name || 'N/A'}</div>
                    <div><strong>🔧 Подвеска:</strong> ${order.suspension?.name || 'N/A'}</div>
                    <div><strong>🎨 Обвес:</strong> ${order.bodykit?.name || 'N/A'}</div>
                    <div><strong>🛞 Диски:</strong> ${order.wheels?.name || 'N/A'}</div>
                </div>
                <div class="order-date">
                    Создан: ${order.created_at}
                </div>
            </div>
        `;
    }).join('');
}
