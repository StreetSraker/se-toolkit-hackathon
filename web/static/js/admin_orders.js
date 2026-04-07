// Admin Orders Management JavaScript

let currentFilter = 'all';
let currentServiceId = null;
let currentServiceName = null;

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

        // Check if logged in as a service
        currentServiceId = data.service_id;
        currentServiceName = data.service_name;

        if (currentServiceId) {
            // Show service info banner
            const serviceInfo = document.getElementById('serviceInfo');
            const serviceNameEl = document.getElementById('serviceName');
            const myOrdersBtn = document.getElementById('myOrdersBtn');
            
            if (serviceInfo) serviceInfo.style.display = 'flex';
            if (serviceNameEl) serviceNameEl.textContent = currentServiceName;
            if (myOrdersBtn) myOrdersBtn.style.display = 'inline-block';
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
        let url = '/api/orders';
        if (status === 'my' && currentServiceId) {
            // Load only orders claimed by this service
            url = `/api/services/${currentServiceId}/orders`;
        } else if (status !== 'all') {
            url = `/api/orders?status=${status}`;
        }
        
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
        const contacts = order.contacts || '';
        const claimedBy = order.claimed_by;
        const isClaimedByMe = claimedBy === currentServiceId;
        const isUnclaimed = !claimedBy;

        return `
            <div class="order-card" onclick="showOrderDetail('${order.id}')" style="cursor: pointer;">
                <div class="order-header">
                    <div>
                        <span class="order-id">${order.id}</span>
                        <span style="color: #a0a0a0; margin-left: 10px;">— ${carName}</span>
                        <span style="color: #58a6ff; margin-left: 10px;">| 👤 ${username}</span>
                        ${contacts ? `<span style="color: #4ecdc4; margin-left: 10px;">| 📞 ${contacts}</span>` : ''}
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        ${isUnclaimed
                            ? '<span class="claim-badge unclaimed">📋 Unclaimed</span>'
                            : isClaimedByMe
                                ? '<span class="claim-badge claimed-by-me">🔧 My Order</span>'
                                : '<span class="claim-badge claimed-by-other">🔧 Claimed</span>'
                        }
                        <span class="order-status ${statusClass}">${statusName}</span>
                    </div>
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

        const isClaimedByMe = order.claimed_by === currentServiceId;
        const isUnclaimed = !order.claimed_by;

        const modal = document.getElementById('orderModal');
        const detail = document.getElementById('orderDetail');

        detail.innerHTML = `
            <h2>📦 Order ${order.id} | ${statusNames[order.status] || order.status}</h2>
            <p style="color: #9ca3af;">Created: ${order.created_at}</p>

            <div style="margin: 20px 0; padding: 15px; background: linear-gradient(145deg, #2a3a3e, #1f2f2e); border-radius: 8px;">
                <p><strong>👤 User:</strong> <span style="color: #58a6ff;">${order.username}</span> (ID: ${order.user_id})</p>
                ${order.contacts ? `<p style="margin-top: 10px;"><strong>📞 Contact:</strong> ${order.contacts}</p>` : '<p style="margin-top: 10px; color: #f44336;"><strong>⚠️ No contact info provided</strong></p>'}
                <p style="margin-top: 10px;">
                    <strong>📋 Status:</strong>
                    ${isUnclaimed
                        ? '<span class="claim-badge unclaimed">📋 Unclaimed</span>'
                        : isClaimedByMe
                            ? '<span class="claim-badge claimed-by-me">🔧 Claimed by You</span>'
                            : `<span class="claim-badge claimed-by-other">🔧 Claimed by another service</span>`
                    }
                </p>
            </div>

            ${!isClaimedByMe && isUnclaimed && currentServiceId ? `
                <div style="margin: 15px 0;">
                    <button class="btn btn-primary" onclick="claimOrder('${order.id}')">📦 Claim This Order</button>
                </div>
            ` : ''}
            ${isClaimedByMe ? `
                <div style="margin: 15px 0;">
                    <button class="btn btn-secondary" onclick="releaseOrder('${order.id}')">↩️ Release Order</button>
                </div>
            ` : ''}

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

            ${order.status_history && order.status_history.length > 0 ? `
                <div style="margin-top: 25px;">
                    <h3 style="margin-bottom: 15px;">📜 Status History</h3>
                    <div style="background: #1c1c1c; padding: 15px; border-radius: 8px;">
                        ${order.status_history.map(h => `
                            <div style="margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #3a3a4e;">
                                <strong>${h.status}</strong> by ${h.by_name} at ${h.at}
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            ${isClaimedByMe ? `
                <div style="margin-top: 30px;">
                    <h3 style="margin-bottom: 15px;">Change status:</h3>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        ${order.status !== 'new' ? `<button class="btn btn-small btn-secondary" onclick="updateOrderStatus('${order.id}', 'new')">🆕 New</button>` : ''}
                        ${order.status !== 'in_progress' ? `<button class="btn btn-small btn-secondary" onclick="updateOrderStatus('${order.id}', 'in_progress')">🔧 In Progress</button>` : ''}
                        ${order.status !== 'completed' ? `<button class="btn btn-small btn-primary" onclick="updateOrderStatus('${order.id}', 'completed')">✅ Completed</button>` : ''}
                        ${order.status !== 'cancelled' ? `<button class="btn btn-small" style="background: #f44336; color: white;" onclick="updateOrderStatus('${order.id}', 'cancelled')">❌ Cancelled</button>` : ''}
                    </div>
                </div>
            ` : `
                <div style="margin-top: 30px; padding: 15px; background: rgba(244,67,54,0.1); border-radius: 8px; color: #f44336;">
                    ⚠️ You can only change status for orders you have claimed.
                </div>
            `}
        `;

        modal.classList.add('show');
    } catch (error) {
        console.error('Error loading order detail:', error);
        alert('❌ Error loading order');
    }
}

async function claimOrder(orderId) {
    if (!confirm('📦 Claim this order for your service?')) {
        return;
    }

    try {
        const response = await fetch(`/api/orders/${orderId}/claim`, {
            method: 'POST'
        });

        if (response.ok) {
            alert('✅ Order claimed successfully!');
            closeModal();
            loadAdminOrders(currentFilter);
        } else {
            const error = await response.json();
            alert('❌ Error: ' + (error.error || 'Failed to claim order'));
        }
    } catch (error) {
        console.error('Error claiming order:', error);
        alert('❌ Error claiming order');
    }
}

async function releaseOrder(orderId) {
    if (!confirm('↩️ Release this order back to the unclaimed pool?')) {
        return;
    }

    try {
        const response = await fetch(`/api/orders/${orderId}/release`, {
            method: 'POST'
        });

        if (response.ok) {
            alert('✅ Order released successfully!');
            closeModal();
            loadAdminOrders(currentFilter);
        } else {
            const error = await response.json();
            alert('❌ Error: ' + (error.error || 'Failed to release order'));
        }
    } catch (error) {
        console.error('Error releasing order:', error);
        alert('❌ Error releasing order');
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
