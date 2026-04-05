// Admin Statistics Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
    loadStatsDashboard();
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

async function loadStatsDashboard() {
    const container = document.getElementById('statsDashboard');
    
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        displayStats(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
        container.innerHTML = '<p class="loading">Ошибка при загрузке статистики</p>';
    }
}

function displayStats(stats) {
    const container = document.getElementById('statsDashboard');
    
    const conversionRate = stats.conversion_rate || 0;
    
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">${stats.total}</div>
                <div class="stat-label">Всего заказов</div>
            </div>
            <div class="stat-card stat-new">
                <div class="stat-number">${stats.new}</div>
                <div class="stat-label">🆕 Новые</div>
            </div>
            <div class="stat-card stat-progress">
                <div class="stat-number">${stats.in_progress}</div>
                <div class="stat-label">🔧 В работе</div>
            </div>
            <div class="stat-card stat-completed">
                <div class="stat-number">${stats.completed}</div>
                <div class="stat-label">✅ Выполнены</div>
            </div>
            <div class="stat-card stat-cancelled">
                <div class="stat-number">${stats.cancelled}</div>
                <div class="stat-label">❌ Отменены</div>
            </div>
        </div>
        
        <div style="margin-top: 40px;">
            <h2 style="color: #ff6b6b; margin-bottom: 20px;">🏆 Популярные автомобили</h2>
            <ul class="popular-cars-list">
                ${stats.popular_cars.map((car, index) => `
                    <li>
                        <span class="car-name">${index + 1}. ${car.name}</span>
                        <span class="car-count">${car.count} шт.</span>
                    </li>
                `).join('')}
            </ul>
        </div>
        
        <div class="conversion-info">
            <h3>📈 Конверсия</h3>
            <div class="conversion-rate">${stats.completed}/${stats.total} (${conversionRate}%)</div>
            <p style="margin-top: 10px; color: #a0a0a0;">
                Процент выполненных заказов от общего количества
            </p>
        </div>
    `;
}
