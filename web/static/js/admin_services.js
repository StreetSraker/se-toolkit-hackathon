// Admin Services Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
    loadServices();
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

async function loadServices() {
    const container = document.getElementById('servicesList');

    try {
        const response = await fetch('/api/services?active_only=false');
        const services = await response.json();

        if (services.length === 0) {
            container.innerHTML = '<p class="loading">📋 No registered services yet</p>';
            return;
        }

        displayServices(services);
    } catch (error) {
        console.error('Error loading services:', error);
        container.innerHTML = '<p class="loading">Error loading services</p>';
    }
}

function displayServices(services) {
    const container = document.getElementById('servicesList');

    container.innerHTML = services.map(service => {
        const statusBadge = service.is_active
            ? '<span class="status-badge status-active">✅ Active</span>'
            : '<span class="status-badge status-inactive">❌ Inactive</span>';

        const specialties = service.specialties && service.specialties.length > 0
            ? `<div class="service-specialties">
                ${service.specialties.map(s => `<span class="specialty-tag">${s}</span>`).join('')}
               </div>`
            : '';

        return `
            <div class="service-card" onclick="showServiceDetail('${service.id}')">
                <div class="service-header">
                    <h3>${service.name}</h3>
                    ${statusBadge}
                </div>
                <div class="service-info">
                    <p><strong>ID:</strong> ${service.id}</p>
                    <p><strong>Username:</strong> ${service.username || 'N/A'}</p>
                    ${service.telegram_username ? `<p><strong>Telegram:</strong> ${service.telegram_username}</p>` : ''}
                    ${service.phone ? `<p><strong>Phone:</strong> ${service.phone}</p>` : ''}
                    <p><strong>Registered:</strong> ${service.registered_at}</p>
                </div>
                ${specialties}
            </div>
        `;
    }).join('');
}

async function showServiceDetail(serviceId) {
    try {
        const [serviceRes, statsRes] = await Promise.all([
            fetch(`/api/services/${serviceId}`),
            fetch('/api/services/stats')
        ]);

        const service = await serviceRes.json();
        const allStats = await statsRes.json();

        // Find stats for this service
        const stats = Array.isArray(allStats)
            ? allStats.find(s => s.service_id === serviceId)
            : allStats;

        const modal = document.getElementById('serviceModal');
        const detail = document.getElementById('serviceDetail');

        detail.innerHTML = `
            <h2>🔧 Service: ${service.name}</h2>
            <p style="color: #808080;">ID: ${service.id} | Username: ${service.username} | Registered: ${service.registered_at}</p>

            <div style="margin: 20px 0; padding: 15px; background: linear-gradient(145deg, #2a3a3e, #1f2f2e); border-radius: 8px;">
                <p><strong>Status:</strong> ${service.is_active ? '✅ Active' : '❌ Inactive'}</p>
                ${service.telegram_username ? `<p><strong>Telegram:</strong> ${service.telegram_username}</p>` : ''}
                ${service.phone ? `<p><strong>Phone:</strong> ${service.phone}</p>` : ''}
                ${service.specialties && service.specialties.length > 0 ? `
                    <p style="margin-top: 10px;"><strong>Specialties:</strong></p>
                    <div style="margin-top: 5px;">
                        ${service.specialties.map(s => `<span class="specialty-tag">${s}</span>`).join('')}
                    </div>
                ` : ''}
            </div>

            ${stats ? `
                <h3 style="margin-top: 30px;">📊 Order Statistics</h3>
                <div class="stats-grid" style="margin-top: 15px;">
                    <div class="stat-card">
                        <div class="stat-value">${stats.total}</div>
                        <div class="stat-label">Total Orders</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.new}</div>
                        <div class="stat-label">🆕 New</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.in_progress}</div>
                        <div class="stat-label">🔧 In Progress</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.completed}</div>
                        <div class="stat-label">✅ Completed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.cancelled}</div>
                        <div class="stat-label">❌ Cancelled</div>
                    </div>
                </div>
            ` : ''}

            <div style="margin-top: 30px; display: flex; gap: 10px; flex-wrap: wrap;">
                ${service.is_active
                    ? `<button class="btn btn-secondary" onclick="deactivateService('${service.id}')">❌ Deactivate Service</button>`
                    : `<button class="btn btn-primary" onclick="activateService('${service.id}')">✅ Activate Service</button>`
                }
            </div>
        `;

        modal.classList.add('show');
    } catch (error) {
        console.error('Error loading service detail:', error);
        alert('❌ Error loading service details');
    }
}

async function deactivateService(serviceId) {
    if (!confirm('⚠️ Are you sure you want to deactivate this service? They will still be able to manage their claimed orders.')) {
        return;
    }

    try {
        const response = await fetch(`/api/services/${serviceId}/deactivate`, {
            method: 'POST'
        });

        if (response.ok) {
            alert('✅ Service deactivated');
            closeModal();
            loadServices();
        } else {
            alert('❌ Error deactivating service');
        }
    } catch (error) {
        console.error('Error deactivating service:', error);
        alert('❌ Error deactivating service');
    }
}

async function activateService(serviceId) {
    try {
        const response = await fetch(`/api/services/${serviceId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ is_active: true })
        });

        if (response.ok) {
            alert('✅ Service activated');
            closeModal();
            loadServices();
        } else {
            alert('❌ Error activating service');
        }
    } catch (error) {
        console.error('Error activating service:', error);
        alert('❌ Error activating service');
    }
}

function closeModal() {
    document.getElementById('serviceModal').classList.remove('show');
}

window.onclick = function(event) {
    const modal = document.getElementById('serviceModal');
    if (event.target === modal) {
        closeModal();
    }
}
