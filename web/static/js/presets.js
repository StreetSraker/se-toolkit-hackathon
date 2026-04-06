// Preset Builds JavaScript

let allPresets = [];
let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', function() {
    loadPresets();
    setupFilters();
});

async function loadPresets() {
    try {
        const response = await fetch('/api/presets');
        allPresets = await response.json();
        displayPresets(allPresets);
    } catch (error) {
        console.error('Error loading presets:', error);
        document.getElementById('presetsGrid').innerHTML = '<p class="loading">Error loading builds</p>';
    }
}

function setupFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;

            if (currentFilter === 'all') {
                displayPresets(allPresets);
            } else {
                displayPresets(allPresets.filter(p => p.tag === currentFilter));
            }
        });
    });
}

function displayPresets(presets) {
    const container = document.getElementById('presetsGrid');

    if (presets.length === 0) {
        container.innerHTML = '<p class="loading">No builds in this category</p>';
        return;
    }

    container.innerHTML = presets.map(preset => `
        <div class="option-card option-card-car" onclick="showPresetDetail('${preset.id}')">
            <div class="option-card-image" style="height: 200px; border-radius: 8px; margin-bottom: 15px; overflow: hidden; background: #2a2a3e; display: flex; align-items: center; justify-content: center; position: relative;">
                <img src="${preset.image}" alt="${preset.name}" style="width: 100%; height: 100%; object-fit: cover;">
                <div class="preset-tag" style="position: absolute; top: 10px; right: 10px; background: ${preset.tag_color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">
                    ${preset.tag}
                </div>
                <div class="preset-hp" style="position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.7); color: #64748b; padding: 4px 10px; border-radius: 8px; font-size: 0.9rem; font-weight: bold;">
                    ${preset.hp}
                </div>
            </div>
            <h3>${preset.name}</h3>
            <p>${preset.description}</p>
            <div class="preset-price" style="margin-top: 10px; color: #64748b; font-size: 1.1rem; font-weight: bold;">
                ${preset.price_estimate}
            </div>
        </div>
    `).join('');
}

async function showPresetDetail(presetId) {
    const preset = allPresets.find(p => p.id === presetId);
    if (!preset) return;

    const car = preset.car || {};
    const engine = preset.engine || {};
    const suspension = preset.suspension || {};
    const bodykit = preset.bodykit || {};
    const wheels = preset.wheels || {};

    const content = `
        <div class="preset-detail">
            <div class="preset-detail-header">
                <div class="preset-tag" style="display: inline-block; background: ${preset.tag_color}; color: white; padding: 6px 16px; border-radius: 16px; font-size: 0.9rem; font-weight: bold; margin-bottom: 10px;">
                    ${preset.tag}
                </div>
                <h2>${preset.name}</h2>
                <p style="color: #a0a0a0; font-size: 1.1rem;">${preset.description}</p>
            </div>

            <div class="preset-specs">
                <h3>⚙️ Engine</h3>
                <div class="spec-item">
                    <strong>${engine.name || 'N/A'}</strong>
                    <span>${engine.power || ''}</span>
                    <p>${engine.description || ''}</p>
                </div>

                <h3>🔧 Suspension</h3>
                <div class="spec-item">
                    <strong>${suspension.name || 'N/A'}</strong>
                    <p>${suspension.description || ''}</p>
                    <div class="spec-details">
                        <span>Clearance: ${suspension.ride_height || '—'}</span>
                        <span>Dampening: ${suspension.dampening || '—'}</span>
                        <span>Springs: ${suspension.spring_rate || '—'}</span>
                        <span>Camber: ${suspension.camber || '—'}</span>
                    </div>
                </div>

                <h3>🎨 Bodykit</h3>
                <div class="spec-item">
                    <strong>${bodykit.name || 'N/A'}</strong>
                    <p>${bodykit.description || ''}</p>
                    <p><strong>Style:</strong> ${bodykit.style || '—'}</p>
                    ${bodykit.components && bodykit.components.length > 0 ? `
                        <ul class="option-components">
                            ${bodykit.components.map(c => `<li>${c}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>

                <h3>🛞 Wheels</h3>
                <div class="spec-item">
                    <strong>${wheels.name || 'N/A'}</strong>
                    <p>${wheels.description || ''}</p>
                    <div class="spec-details">
                        <span>Sizes: ${wheels.sizes || '—'}</span>
                        <span>Weight: ${wheels.weight || '—'}</span>
                        <span>Style: ${wheels.style || '—'}</span>
                    </div>
                </div>
            </div>

            <div class="preset-detail-footer">
                <div class="preset-price-large" style="color: #64748b; font-size: 1.5rem; font-weight: bold;">
                    ${preset.price_estimate}
                </div>
                <div class="action-buttons">
                    <button class="btn btn-primary" onclick="orderPreset('${preset.id}')">📦 Order this build</button>
                    <button class="btn btn-secondary" onclick="customizePreset('${preset.id}')">🔧 Customize</button>
                </div>
            </div>
        </div>
    `;

    document.getElementById('modalContent').innerHTML = content;
    document.getElementById('presetModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('presetModal').classList.add('hidden');
}

// Close modal on backdrop click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('presetModal');
    if (e.target === modal) {
        closeModal();
    }
});

async function orderPreset(presetId) {
    const preset = allPresets.find(p => p.id === presetId);
    if (!preset) return;

    const orderData = {
        car: preset.car || {},
        engine: preset.engine || {},
        suspension: preset.suspension || {},
        bodykit: preset.bodykit || {},
        wheels: preset.wheels || {},
        notes: `Pre-built: ${preset.name}`
    };

    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });

        if (response.ok) {
            const order = await response.json();
            closeModal();
            alert(`✅ Order #${order.id} placed!\n\nBuild: ${preset.name}\nA manager will contact you soon. Thank you! 🚗`);
            window.location.href = '/orders';
        } else {
            alert('❌ Error placing order');
        }
    } catch (error) {
        console.error('Error ordering preset:', error);
        alert('❌ Error placing order');
    }
}

function customizePreset(presetId) {
    // Navigate to configurator with preset data pre-filled
    const preset = allPresets.find(p => p.id === presetId);
    if (!preset) return;

    // Store preset in sessionStorage for the configurator to pick up
    sessionStorage.setItem('presetConfig', JSON.stringify({
        car: preset.car,
        engine: preset.engine,
        suspension: preset.suspension,
        bodykit: preset.bodykit,
        wheels: preset.wheels
    }));

    window.location.href = '/configurator';
}
