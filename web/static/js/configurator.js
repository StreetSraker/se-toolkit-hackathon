// Car Configurator JavaScript

let currentStep = 1;
let configData = {
    car: null,
    engine: null,
    suspension: null,
    bodykit: null,
    wheels: null
};

// Load data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCars();
});

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
    const engines = await (await fetch(`/api/engines/${configData.car.id}`)).json();
    configData.engine = engines.find(e => e.id === engineId);
    
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
        <p><strong>Мощность:</strong> ${configData.engine.power}</p>
        <p>${configData.engine.description}</p>
    `;
    
    container.innerHTML = Object.entries(suspensions).map(([id, susp]) => `
        <div class="option-card" onclick="selectSuspension('${id}')">
            <h3>${susp.name}</h3>
            <p>${susp.description}</p>
            <div class="option-details">
                <p><strong>Клиренс:</strong> ${susp.ride_height}</p>
                <p><strong>Амортизация:</strong> ${susp.dampening}</p>
                <p><strong>Пружины:</strong> ${susp.spring_rate}</p>
                <p><strong>Развал:</strong> ${susp.camber}</p>
                <p><strong>Применение:</strong> ${susp.use_case}</p>
            </div>
        </div>
    `).join('');
}

function selectSuspension(suspId) {
    fetch('/api/suspensions')
        .then(r => r.json())
        .then(suspensions => {
            configData.suspension = { id: suspId, ...suspensions[suspId] };
            loadBodykits();
        });
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
        <p><strong>Клиренс:</strong> ${configData.suspension.ride_height}</p>
    `;
    
    container.innerHTML = bodykits.map(bk => `
        <div class="option-card" onclick="selectBodykit('${bk.id}')">
            <h3>${bk.name}</h3>
            <p>${bk.description}</p>
            <p><strong>Стиль:</strong> ${bk.style}</p>
            <ul class="option-components">
                ${bk.components.slice(0, 4).map(c => `<li>${c}</li>`).join('')}
                ${bk.components.length > 4 ? `<li>...и ещё ${bk.components.length - 4}</li>` : ''}
            </ul>
        </div>
    `).join('');
}

function selectBodykit(bkId) {
    fetch('/api/bodykits')
        .then(r => r.json())
        .then(bodykits => {
            configData.bodykit = bodykits.find(b => b.id === bkId);
            loadWheels();
        });
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
        <p><strong>Стиль:</strong> ${configData.bodykit.style}</p>
    `;
    
    container.innerHTML = wheels.map(wheel => `
        <div class="option-card" onclick="selectWheel('${wheel.id}')">
            <h3>${wheel.name}</h3>
            <p>${wheel.description}</p>
            <div class="option-details">
                <p><strong>Размеры:</strong> ${wheel.sizes}</p>
                <p><strong>Вес:</strong> ${wheel.weight}</p>
                <p><strong>Стиль:</strong> ${wheel.style}</p>
            </div>
        </div>
    `).join('');
}

function selectWheel(wheelId) {
    fetch('/api/wheels')
        .then(r => r.json())
        .then(wheels => {
            configData.wheels = wheels.find(w => w.id === wheelId);
            showSummary();
            nextStep();
        });
}

function showSummary() {
    const summary = document.getElementById('configSummary');
    summary.innerHTML = `
        <div class="summary-item">
            <strong>🚗 Авто:</strong>
            <span>${configData.car.name} (${configData.car.years})</span>
        </div>
        <div class="summary-item">
            <strong>⚙️ Двигатель:</strong>
            <span>${configData.engine.name} — ${configData.engine.power}</span>
        </div>
        <div class="summary-item">
            <strong>🔧 Подвеска:</strong>
            <span>${configData.suspension.name}</span>
        </div>
        <div class="summary-item">
            <strong>🎨 Обвес:</strong>
            <span>${configData.bodykit.name}</span>
        </div>
        <div class="summary-item">
            <strong>🛞 Диски:</strong>
            <span>${configData.wheels.name}</span>
        </div>
    `;
}

async function submitOrder() {
    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(configData)
        });
        
        if (response.ok) {
            const order = await response.json();
            alert(`✅ Заказ #${order.id} оформлен!\n\nСкоро свяжется менеджер. Спасибо! 🚗`);
            window.location.href = '/orders';
        } else {
            alert('❌ Ошибка при оформлении заказа');
        }
    } catch (error) {
        console.error('Error submitting order:', error);
        alert('❌ Ошибка при оформлении заказа');
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
    if (currentStep > 1 && currentStep < 6) {
        prevBtn.classList.remove('hidden');
    } else {
        prevBtn.classList.add('hidden');
    }
}
