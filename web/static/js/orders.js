// Orders Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadOrders();
});

async function checkAuth() {
    try {
        const response = await fetch('/api/auth/check');
        const data = await response.json();

        if (!data.is_authenticated) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error checking auth:', error);
    }
}

async function loadOrders() {
    const container = document.getElementById('ordersList');

    try {
        const response = await fetch('/api/orders');
        if (response.status === 403) {
            window.location.href = '/login';
            return;
        }
        const orders = await response.json();

        if (orders.length === 0) {
            container.innerHTML = `
                <div class="info-box">
                    <h3 data-i18n="orders.noOrders">📋 You have no orders yet</h3>
                    <p data-i18n="orders.createFirst">First configure a car through the Configurator.</p>
                    <a href="/configurator" class="btn btn-primary" style="margin-top: 20px;" data-i18n="configurator.configurator">🚗 Configurator</a>
                </div>
            `;
            return;
        }

        displayOrders(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="loading">' + (i18n ? i18n.t('orders.errorLoading') : 'Error loading orders') + '</p>';
    }
}

function displayOrders(orders) {
    const container = document.getElementById('ordersList');

    const statusNames = {
        'new': i18n ? i18n.t('status.new') : '🆕 New',
        'in_progress': i18n ? i18n.t('status.inProgress') : '🔧 In Progress',
        'completed': i18n ? i18n.t('status.completed') : '✅ Completed',
        'cancelled': i18n ? i18n.t('status.cancelled') : '❌ Cancelled'
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
        const contacts = order.contacts || '';

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
                    <div><strong>⚙️ Engine:</strong> ${order.engine?.name || 'N/A'}</div>
                    <div><strong>🔧 Suspension:</strong> ${order.suspension?.name || 'N/A'}</div>
                    <div><strong>🎨 Bodykit:</strong> ${order.bodykit?.name || 'N/A'}</div>
                    <div><strong>🛞 Wheels:</strong> ${order.wheels?.name || 'N/A'}</div>
                    ${contacts ? `<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #3a3a4e;"><strong>📞 Contact:</strong> ${contacts}</div>` : ''}
                </div>
                <div class="order-date">
                    Created: ${order.created_at}
                </div>
            </div>
        `;
    }).join('');
}
