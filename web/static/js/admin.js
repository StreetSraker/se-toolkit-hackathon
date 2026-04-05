// Admin Panel JavaScript

let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
});

async function checkAdminAuth() {
    try {
        const response = await fetch('/api/admin/check');
        const data = await response.json();
        
        if (data.is_admin) {
            document.getElementById('adminLogin').classList.add('hidden');
            document.getElementById('adminDashboard').classList.remove('hidden');
            loadAdminOrders();
            loadStats();
        }
    } catch (error) {
        console.error('Error checking admin auth:', error);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('loginError');
    
    try {
        const response = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('adminLogin').classList.add('hidden');
            document.getElementById('adminDashboard').classList.remove('hidden');
            loadAdminOrders();
            loadStats();
        } else {
            errorMsg.textContent = '❌ Неверный пароль';
            errorMsg.classList.remove('hidden');
        }
    } catch (error) {
        errorMsg.textContent = '❌ Ошибка при входе';
        errorMsg.classList.remove('hidden');
    }
}

async function handleLogout() {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        document.getElementById('adminDashboard').classList.add('hidden');
        document.getElementById('adminLogin').classList.remove('hidden');
        document.getElementById('password').value = '';
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
            container.innerHTML = '<p class="loading">📋 Заказов нет</p>';
            return;
        }
        
        displayAdminOrders(orders);
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="loading">Ошибка при загрузке заказов</p>';
    }
}

function displayAdminOrders(orders) {
    const container = document.getElementById('adminOrdersList');
    
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
    
    // Show only first 10 orders in list
    const displayOrders = orders.slice(0, 10);
    
    container.innerHTML = displayOrders.map(order => {
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
    
    if (orders.length > 10) {
        container.innerHTML += `<p style="text-align: center; color: #808080; margin-top: 20px;">...и ещё ${orders.length - 10} заказов</p>`;
    }
}

function filterOrders(status) {
    currentFilter = status;
    
    // Update active button
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
            alert('❌ Заказ не найден');
            return;
        }
        
        const statusNames = {
            'new': '🆕 Новый',
            'in_progress': '🔧 В работе',
            'completed': '✅ Выполнен',
            'cancelled': '❌ Отменён'
        };
        
        const modal = document.getElementById('orderModal');
        const detail = document.getElementById('orderDetail');
        
        detail.innerHTML = `
            <h2>📦 Заказ ${order.id} | ${statusNames[order.status] || order.status}</h2>
            <p style="color: #808080;">Создан: ${order.created_at}</p>
            
            <div style="margin: 20px 0; padding: 15px; background: linear-gradient(145deg, #2a3a3e, #1f2f2e); border-radius: 8px;">
                <p><strong>👤 Пользователь:</strong> ${order.username} (ID: ${order.user_id})</p>
            </div>
            
            <div class="summary-box">
                <div class="summary-item">
                    <strong>🚗 Авто:</strong>
                    <span>${order.car?.name || 'N/A'} (${order.car?.years || ''})</span>
                </div>
                <div class="summary-item">
                    <strong>⚙️ Двигатель:</strong>
                    <span>${order.engine?.name || 'N/A'} — ${order.engine?.power || ''}</span>
                </div>
                <div class="summary-item">
                    <strong>🔧 Подвеска:</strong>
                    <span>${order.suspension?.name || 'N/A'}</span>
                </div>
                <div class="summary-item">
                    <strong>🎨 Обвес:</strong>
                    <span>${order.bodykit?.name || 'N/A'}</span>
                </div>
                <div class="summary-item">
                    <strong>🛞 Диски:</strong>
                    <span>${order.wheels?.name || 'N/A'}</span>
                </div>
            </div>
            
            ${order.notes ? `<p style="margin-top: 20px;"><strong>📝 Заметки:</strong> ${order.notes}</p>` : ''}
            
            <div style="margin-top: 30px;">
                <h3 style="margin-bottom: 15px;">Изменить статус:</h3>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    ${order.status !== 'new' ? `<button class="btn btn-small btn-secondary" onclick="updateOrderStatus('${order.id}', 'new')">🆕 Новый</button>` : ''}
                    ${order.status !== 'in_progress' ? `<button class="btn btn-small btn-secondary" onclick="updateOrderStatus('${order.id}', 'in_progress')">🔧 В работе</button>` : ''}
                    ${order.status !== 'completed' ? `<button class="btn btn-small btn-primary" onclick="updateOrderStatus('${order.id}', 'completed')">✅ Выполнен</button>` : ''}
                    ${order.status !== 'cancelled' ? `<button class="btn btn-small" style="background: #f44336; color: white;" onclick="updateOrderStatus('${order.id}', 'cancelled')">❌ Отменён</button>` : ''}
                </div>
            </div>
        `;
        
        modal.classList.add('show');
    } catch (error) {
        console.error('Error loading order detail:', error);
        alert('❌ Ошибка при загрузке заказа');
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
                'new': '🆕 Новый',
                'in_progress': '🔧 В работе',
                'completed': '✅ Выполнен',
                'cancelled': '❌ Отменён'
            };
            
            alert(`✅ Статус ${orderId} → ${statusNames[newStatus]}`);
            closeModal();
            loadAdminOrders(currentFilter);
            loadStats();
        } else {
            alert('❌ Ошибка при обновлении статуса');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        alert('❌ Ошибка при обновлении статуса');
    }
}

function closeModal() {
    document.getElementById('orderModal').classList.remove('show');
}

async function loadStats() {
    try {
        const response = await fetch('/api/admin/stats');
        const stats = await response.json();
        
        document.getElementById('statTotal').textContent = stats.total;
        document.getElementById('statNew').textContent = stats.new;
        document.getElementById('statProgress').textContent = stats.in_progress;
        document.getElementById('statCompleted').textContent = stats.completed;
        document.getElementById('statCancelled').textContent = stats.cancelled;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('orderModal');
    if (event.target === modal) {
        closeModal();
    }
}
