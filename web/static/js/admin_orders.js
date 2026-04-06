// Admin Orders Management JavaScript

let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
    loadAdminOrders();
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

async function loadAdminOrders(status = 'all') {
    const container = document.getElementById('adminOrdersList');
    
    try {
        const url = status === 'all' ? '/api/orders' : `/api/orders?status=${status}`;
        const response = await fetch(url);
        const orders = await response.json();
        
        if (orders.length === 0) {
            container.innerHTML = '<p class="loading">📋 No orders</p>';
            return;
        }
        
        displayOrders(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="loading">Error loading orders</p>';
    }
}

function displayOrders(orders) {
    const container = document.getElementById('adminOrdersList');
    
    const statusNames = {
        'new': '🆕 New',
        'in_progress': '🔧 In Progress',
        'completed': '✅ Completed',
        'cancelled': '❌ Cancelled'
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
            <div class="order-card" onclick="showOrderDetail('${order.id}')" style="cursor: pointer;">
                <div class="order-header">
                    <div>
                        <span class="order-id">${order.id}</span>
                        <span style="color: #a0a0a0; margin-left: 10px;">— ${carName}</span>
                        <span style="color: #808080; margin-left: 10px;">| ${username}</span>
                    </div>
                    <span class="order-status ${statusClass}">${statusName}</span>
                </div>
                <div class="order-date">
                    ${order.created_at}
                </div>
            </div>
        `;
    }).join('');
}

function filterOrders(status) {
    currentFilter = status;
    
    document.querySelectorAll('.btn-filter').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    loadAdminOrders(status);
}

async function showOrderDetail(orderId) {
    try {
        const response = await fetch(`/api/orders/${orderId}`);
        const order = await response.json();
        
        if (!order) {
            alert('❌ Order not found');
            return;
        }

        const statusNames = {
            'new': '🆕 New',
            'in_progress': '🔧 In Progress',
            'completed': '✅ Completed',
            'cancelled': '❌ Cancelled'
        };
        
        const modal = document.getElementById('orderModal');
        const detail = document.getElementById('orderDetail');
        
        detail.innerHTML = `
            <h2>📦 Order ${order.id} | ${statusNames[order.status] || order.status}</h2>
            <p style="color: #808080;">Created: ${order.created_at}</p>

            <div style="margin: 20px 0; padding: 15px; background: linear-gradient(145deg, #2a3a3e, #1f2f2e); border-radius: 8px;">
                <p><strong>👤 User:</strong> ${order.username} (ID: ${order.user_id})</p>
            </div>

            <div class="summary-box">
                <div class="summary-item">
                    <strong>🚗 Car:</strong>
                    <span>${order.car?.name || 'N/A'} (${order.car?.years || ''})</span>
                </div>
                <div class="summary-item">
                    <strong>⚙️ Engine:</strong>
                    <span>${order.engine?.name || 'N/A'} — ${order.engine?.power || ''}</span>
                </div>
                <div class="summary-item">
                    <strong>🔧 Suspension:</strong>
                    <span>${order.suspension?.name || 'N/A'}</span>
                </div>
                <div class="summary-item">
                    <strong>🎨 Bodykit:</strong>
                    <span>${order.bodykit?.name || 'N/A'}</span>
                </div>
                <div class="summary-item">
                    <strong>🛞 Wheels:</strong>
                    <span>${order.wheels?.name || 'N/A'}</span>
                </div>
            </div>

            ${order.notes ? `<p style="margin-top: 20px;"><strong>📝 Notes:</strong> ${order.notes}</p>` : ''}

            <div style="margin-top: 30px;">
                <h3 style="margin-bottom: 15px;">Change status:</h3>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    ${order.status !== 'new' ? `<button class="btn btn-small btn-secondary" onclick="updateOrderStatus('${order.id}', 'new')">🆕 New</button>` : ''}
                    ${order.status !== 'in_progress' ? `<button class="btn btn-small btn-secondary" onclick="updateOrderStatus('${order.id}', 'in_progress')">🔧 In Progress</button>` : ''}
                    ${order.status !== 'completed' ? `<button class="btn btn-small btn-primary" onclick="updateOrderStatus('${order.id}', 'completed')">✅ Completed</button>` : ''}
                    ${order.status !== 'cancelled' ? `<button class="btn btn-small" style="background: #f44336; color: white;" onclick="updateOrderStatus('${order.id}', 'cancelled')">❌ Cancelled</button>` : ''}
                </div>
            </div>
        `;
        
        modal.classList.add('show');
    } catch (error) {
        console.error('Error loading order detail:', error);
        alert('❌ Error loading order');
    }
}

async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`/api/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            const statusNames = {
                'new': '🆕 New',
                'in_progress': '🔧 In Progress',
                'completed': '✅ Completed',
                'cancelled': '❌ Cancelled'
            };

            alert(`✅ Status ${orderId} → ${statusNames[newStatus]}`);
            closeModal();
            loadAdminOrders(currentFilter);
        } else {
            alert('❌ Error updating status');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        alert('❌ Error updating status');
    }
}

function closeModal() {
    document.getElementById('orderModal').classList.remove('show');
}

window.onclick = function(event) {
    const modal = document.getElementById('orderModal');
    if (event.target === modal) {
        closeModal();
    }
}
