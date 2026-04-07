// Service Statistics Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadStatsDashboard();
});

async function checkAuth() {
    try {
        const response = await fetch('/api/admin/check');
        const data = await response.json();

        if (!data.is_admin) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error checking auth:', error);
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

async function loadStatsDashboard() {
    const container = document.getElementById('statsDashboard');

    try {
        const [statsRes, checkRes] = await Promise.all([
            fetch('/api/stats'),
            fetch('/api/admin/check')
        ]);

        if (!statsRes.ok) {
            window.location.href = '/';
            return;
        }

        const stats = await statsRes.json();
        const authData = await checkRes.json();

        displayStats(stats, authData);
    } catch (error) {
        console.error('Error loading stats:', error);
        container.innerHTML = '<p class="loading">Error loading statistics</p>';
    }
}

function displayStats(stats, authData) {
    const container = document.getElementById('statsDashboard');
    const conversionRate = stats.conversion_rate || 0;
    const serviceName = authData.service_name || 'Your Service';

    let html = `
        <h2 style="color: #c9d1d9; margin-bottom: 20px;">📊 ${serviceName} — Statistics</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">${stats.total}</div>
                <div class="stat-label">Total orders</div>
            </div>
            <div class="stat-card stat-new">
                <div class="stat-number">${stats.new}</div>
                <div class="stat-label">🆕 New</div>
            </div>
            <div class="stat-card stat-progress">
                <div class="stat-number">${stats.in_progress}</div>
                <div class="stat-label">🔧 In Progress</div>
            </div>
            <div class="stat-card stat-completed">
                <div class="stat-number">${stats.completed}</div>
                <div class="stat-label">✅ Completed</div>
            </div>
            <div class="stat-card stat-cancelled">
                <div class="stat-number">${stats.cancelled}</div>
                <div class="stat-label">❌ Cancelled</div>
            </div>
        </div>
    `;

    // Popular cars
    if (stats.popular_cars && stats.popular_cars.length > 0) {
        html += `
            <div style="margin-top: 40px;">
                <h2 style="color: #64748b; margin-bottom: 20px;">🏆 Popular Cars</h2>
                <ul class="popular-cars-list">
                    ${stats.popular_cars.map((car, index) => `
                        <li>
                            <span class="car-name">${index + 1}. ${car.name}</span>
                            <span class="car-count">${car.count} orders</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }

    // Conversion rate
    html += `
        <div class="conversion-info">
            <h3>📈 Conversion Rate</h3>
            <div class="conversion-rate">${stats.completed}/${stats.total} (${conversionRate}%)</div>
            <p style="margin-top: 10px; color: #a0a0a0;">
                Percentage of completed orders out of total
            </p>
        </div>
    `;

    container.innerHTML = html;
}
