// Car Configurator JavaScript

let currentStep = 1;
let configData = {
    car: null,
    engine: null,
    suspension: null,
    bodykit: null,
    wheels: null
};
let userProfile = null;

// Load data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadCars();
});

async function handleLogout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
        window.location.href = '/login';
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

async function loadUserProfile() {
    try {
        const response = await fetch('/api/auth/check');
        const data = await response.json();
        if (data.is_authenticated) {
            // Fetch full profile
            const profResp = await fetch('/api/profile');
            if (profResp.ok) {
                userProfile = await profResp.json();
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

async function loadCars() {
    try {
        const response = await fetch('/api/cars');
        const cars = await response.json();
        displayCars(cars);
    } catch (error) {
        console.error('Error loading cars:', error);
    }
}

function displayCars(cars) {
    const container = document.getElementById('carOptions');

    container.innerHTML = cars.map(car => `
        <div class="option-card option-card-car" onclick="selectCar('${car.id}')">
            <div class="option-card-image" style="height: 180px; border-radius: 8px; margin-bottom: 15px; overflow: hidden; background: #2a2a3e; display: flex; align-items: center; justify-content: center;">
                <img src="${car.image}" alt="${car.name}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <h3>${car.name}</h3>
            <div class="option-years">${car.years}</div>
            <p>${car.description}</p>
        </div>
    `).join('');
}

async function selectCar(carId) {
    configData.car = await (await fetch(`/api/cars`)).json().then(cars => cars.find(c => c.id === carId));

    // Load engines for this car
    const response = await fetch(`/api/engines/${carId}`);
    const engines = await response.json();

    displayEngines(engines);
    nextStep();
}

function displayEngines(engines) {
    const container = document.getElementById('engineOptions');
    const carInfo = document.getElementById('selectedCarInfo');

    carInfo.innerHTML = `
        <h3>${configData.car.name}</h3>
        <p>${configData.car.description}</p>
    `;

    container.innerHTML = engines.map(engine => `
        <div class="option-card" onclick="selectEngine('${engine.id}')">
            <h3>${engine.name}</h3>
            <div class="option-power">${engine.power}</div>
            <p>${engine.description}</p>
        </div>
    `).join('');
}

async function selectEngine(engineId) {
    if (engineId === 'custom') {
        const value = await showCustomInputPrompt('Custom Engine', "Enter your desired engine/configuration.\nFor example: '2JZ with Garrett GT3582R, 800 hp' or 'HKS 3.4L Kit'");
        if (!value) return; // cancelled
        configData.engine = {
            id: 'custom',
            name: `Custom: ${value}`,
            power: 'Custom',
            description: value
        };
    } else {
        const engines = await (await fetch(`/api/engines/${configData.car.id}`)).json();
        configData.engine = engines.find(e => e.id === engineId);
    }

    // Load suspensions
    const response = await fetch('/api/suspensions');
    const suspensions = await response.json();

    displaySuspensions(suspensions);
    nextStep();
}

function displaySuspensions(suspensions) {
    const container = document.getElementById('suspensionOptions');
    const engineInfo = document.getElementById('selectedEngineInfo');

    engineInfo.innerHTML = `
        <h3>${configData.engine.name}</h3>
        <p><strong>Power:</strong> ${configData.engine.power}</p>
        <p>${configData.engine.description}</p>
    `;

    container.innerHTML = Object.entries(suspensions).map(([id, susp]) => `
        <div class="option-card" onclick="selectSuspension('${id}')">
            <h3>${susp.name}</h3>
            <p>${susp.description}</p>
            <div class="option-details">
                <p><strong>Clearance:</strong> ${susp.ride_height}</p>
                <p><strong>Dampening:</strong> ${susp.dampening}</p>
                <p><strong>Springs:</strong> ${susp.spring_rate}</p>
                <p><strong>Camber:</strong> ${susp.camber}</p>
                <p><strong>Use case:</strong> ${susp.use_case}</p>
            </div>
        </div>
    `).join('');
}

function selectSuspension(suspId) {
    if (suspId === 'custom') {
        showCustomInputPrompt('Custom Suspension', "Enter your desired suspension configuration.\nFor example: 'BC Racing BR Series, -40mm, camber -2.0'")
            .then(value => {
                if (!value) return;
                configData.suspension = {
                    id: 'custom',
                    name: `Custom: ${value}`,
                    description: value,
                    ride_height: 'Custom',
                    dampening: 'Custom',
                    spring_rate: 'Custom',
                    camber: 'Custom',
                    use_case: 'Custom configuration'
                };
                loadBodykits();
            });
    } else {
        fetch('/api/suspensions')
            .then(r => r.json())
            .then(suspensions => {
                configData.suspension = { id: suspId, ...suspensions[suspId] };
                loadBodykits();
            });
    }
}

async function loadBodykits() {
    const response = await fetch('/api/bodykits');
    const bodykits = await response.json();

    displayBodykits(bodykits);
    nextStep();
}

function displayBodykits(bodykits) {
    const container = document.getElementById('bodykitOptions');
    const suspInfo = document.getElementById('selectedSuspensionInfo');

    suspInfo.innerHTML = `
        <h3>${configData.suspension.name}</h3>
        <p>${configData.suspension.description}</p>
        <p><strong>Clearance:</strong> ${configData.suspension.ride_height}</p>
    `;

    container.innerHTML = bodykits.map(bk => `
        <div class="option-card" onclick="selectBodykit('${bk.id}')">
            ${bk.image ? `
            <div class="option-card-image" style="height: 160px; border-radius: 8px; margin-bottom: 12px; overflow: hidden; background: #2a2a3e;">
                <img src="${bk.image}" alt="${bk.name}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>` : ''}
            <h3>${bk.name}</h3>
            <p>${bk.description}</p>
            <p><strong>Style:</strong> ${bk.style}</p>
            <ul class="option-components">
                ${bk.components.slice(0, 4).map(c => `<li>${c}</li>`).join('')}
                ${bk.components.length > 4 ? `<li>...and ${bk.components.length - 4} more</li>` : ''}
            </ul>
        </div>
    `).join('');
}

function selectBodykit(bkId) {
    if (bkId === 'custom') {
        showCustomInputPrompt('Custom Bodykit', "Enter your desired bodykit or brand.\nFor example: 'VARIS Geo widebody, carbon hood' or 'Rocket Bunny v2'")
            .then(value => {
                if (!value) return;
                configData.bodykit = {
                    id: 'custom',
                    name: `Custom: ${value}`,
                    description: value,
                    components: ['Custom parts'],
                    style: 'Custom',
                    price_range: 'Negotiable'
                };
                loadWheels();
            });
    } else {
        fetch('/api/bodykits')
            .then(r => r.json())
            .then(bodykits => {
                configData.bodykit = bodykits.find(b => b.id === bkId);
                loadWheels();
            });
    }
}

async function loadWheels() {
    const response = await fetch('/api/wheels');
    const wheels = await response.json();

    displayWheels(wheels);
    nextStep();
}

function displayWheels(wheels) {
    const container = document.getElementById('wheelOptions');
    const bodykitInfo = document.getElementById('selectedBodykitInfo');

    bodykitInfo.innerHTML = `
        <h3>${configData.bodykit.name}</h3>
        <p>${configData.bodykit.description}</p>
        <p><strong>Style:</strong> ${configData.bodykit.style}</p>
    `;

    container.innerHTML = wheels.map(wheel => `
        <div class="option-card" onclick="selectWheel('${wheel.id}')">
            ${wheel.image ? `
            <div class="option-card-image" style="height: 160px; border-radius: 8px; margin-bottom: 12px; overflow: hidden; background: #2a2a3e;">
                <img src="${wheel.image}" alt="${wheel.name}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>` : ''}
            <h3>${wheel.name}</h3>
            <p>${wheel.description}</p>
            <div class="option-details">
                <p><strong>Sizes:</strong> ${wheel.sizes}</p>
                <p><strong>Weight:</strong> ${wheel.weight}</p>
                <p><strong>Style:</strong> ${wheel.style}</p>
            </div>
        </div>
    `).join('');
}

function selectWheel(wheelId) {
    if (wheelId === 'custom') {
        showCustomInputPrompt('Custom Wheels', "Enter your desired wheels (brand, model, size).\nFor example: 'Volk TE37 18x9.5 +22' or 'BBS RS 18inch gold'")
            .then(value => {
                if (!value) return;
                configData.wheels = {
                    id: 'custom',
                    name: `Custom: ${value}`,
                    description: value,
                    sizes: 'Custom',
                    weight: 'Custom',
                    style: 'Custom',
                    price_range: 'Negotiable'
                };
                showSummary();
                nextStep();
            });
    } else {
        fetch('/api/wheels')
            .then(r => r.json())
            .then(wheels => {
                configData.wheels = wheels.find(w => w.id === wheelId);
                showSummary();
                nextStep();
            });
    }
}

function showSummary() {
    const summary = document.getElementById('configSummary');
    summary.innerHTML = `
        <div class="summary-item">
            <strong>🚗 Car:</strong>
            <span>${configData.car.name} (${configData.car.years})</span>
        </div>
        <div class="summary-item">
            <strong>⚙️ Engine:</strong>
            <span>${configData.engine.name} — ${configData.engine.power}</span>
        </div>
        <div class="summary-item">
            <strong>🔧 Suspension:</strong>
            <span>${configData.suspension.name}</span>
        </div>
        <div class="summary-item">
            <strong>🎨 Bodykit:</strong>
            <span>${configData.bodykit.name}</span>
        </div>
        <div class="summary-item">
            <strong>🛞 Wheels:</strong>
            <span>${configData.wheels.name}</span>
        </div>
    `;

    // Show profile contacts
    showProfileContacts();
}

function showProfileContacts() {
    const container = document.getElementById('profileContacts');
    if (!container) return;

    if (!userProfile || (!userProfile.telegram && !userProfile.phone && !userProfile.email)) {
        container.innerHTML = `
            <div class="summary-item">
                <strong>📞 Contacts:</strong>
                <span style="color: #f44336;">⚠️ No contacts in profile</span>
            </div>
        `;
    } else {
        const contacts = [];
        if (userProfile.telegram) contacts.push(`💬 ${userProfile.telegram}`);
        if (userProfile.phone) contacts.push(`📱 ${userProfile.phone}`);
        if (userProfile.email) contacts.push(`📧 ${userProfile.email}`);

        container.innerHTML = `
            <div class="summary-item">
                <strong>📞 Contacts (from profile):</strong>
                <span>${contacts.join(' &nbsp;|&nbsp; ')}</span>
            </div>
        `;
    }
}

function buildContactsString() {
    if (!userProfile) return '';

    const contacts = [];
    if (userProfile.telegram) contacts.push(`Telegram: ${userProfile.telegram}`);
    if (userProfile.phone) contacts.push(`Phone: ${userProfile.phone}`);
    if (userProfile.email) contacts.push(`Email: ${userProfile.email}`);

    return contacts.join(', ');
}

async function submitOrder() {
    const contacts = buildContactsString();

    try {
        const orderPayload = {
            ...configData,
            contacts: contacts
        };

        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderPayload)
        });

        if (response.ok) {
            const order = await response.json();
            let message = `✅ Order #${order.id} placed!\n\n`;
            if (order.contacts) {
                message += `📞 Contact: ${order.contacts}\n\n`;
            }
            message += `A manager will contact you soon. Thank you! 🚗`;
            alert(message);
            window.location.href = '/orders';
        } else {
            const error = await response.json();
            alert('❌ Error placing order: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error submitting order:', error);
        alert('❌ Error placing order');
    }
}

function restartConfig() {
    currentStep = 1;
    configData = {
        car: null,
        engine: null,
        suspension: null,
        bodykit: null,
        wheels: null
    };
    updateSteps();
    loadCars();
}

function nextStep() {
    if (currentStep < 6) {
        currentStep++;
        updateSteps();
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        updateSteps();
    }
}

function updateSteps() {
    // Hide all steps content
    document.querySelectorAll('.config-step-content').forEach(el => {
        el.classList.add('hidden');
    });

    // Show current step
    const currentStepEl = document.getElementById(`step${currentStep}`);
    if (currentStepEl) {
        currentStepEl.classList.remove('hidden');
    }

    // Update progress bar
    document.querySelectorAll('.progress-step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index + 1 === currentStep) {
            step.classList.add('active');
        } else if (index + 1 < currentStep) {
            step.classList.add('completed');
        }
    });

    // Update navigation buttons
    const prevBtn = document.getElementById('prevBtn');
    const navButtons = document.getElementById('navButtons');

    // Hide default nav buttons for step 6 (it has its own buttons)
    if (currentStep === 6) {
        navButtons.classList.add('hidden');
    } else if (currentStep > 1) {
        prevBtn.classList.remove('hidden');
        navButtons.classList.remove('hidden');
    } else {
        prevBtn.classList.add('hidden');
        navButtons.classList.add('hidden');
    }
}

// Custom Input Modal
function showCustomInputPrompt(title, description) {
    return new Promise((resolve) => {
        const modal = document.getElementById('customInputModal');
        const titleEl = document.getElementById('customInputTitle');
        const descEl = document.getElementById('customInputDescription');
        const inputEl = document.getElementById('customInputField');
        const confirmBtn = document.getElementById('customInputConfirm');
        const cancelBtn = document.getElementById('customInputCancel');

        titleEl.textContent = title;
        descEl.textContent = description;
        inputEl.value = '';

        modal.classList.add('show');
        inputEl.focus();

        function close(result) {
            modal.classList.remove('show');
            confirmBtn.removeEventListener('click', onConfirm);
            cancelBtn.removeEventListener('click', onCancel);
            inputEl.removeEventListener('keydown', onKey);
            resolve(result);
        }

        function onConfirm() {
            const val = inputEl.value.trim();
            if (val) close(val);
            else inputEl.classList.add('shake');
            setTimeout(() => inputEl.classList.remove('shake'), 500);
        }

        function onCancel() {
            close(null);
        }

        function onKey(e) {
            if (e.key === 'Enter') onConfirm();
            if (e.key === 'Escape') onCancel();
        }

        confirmBtn.addEventListener('click', onConfirm);
        cancelBtn.addEventListener('click', onCancel);
        inputEl.addEventListener('keydown', onKey);
    });
}
