// Admin Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
});

async function checkAdminAuth() {
    try {
        const response = await fetch('/api/admin/check');
        const data = await response.json();
        
        if (data.is_admin) {
            window.location.href = '/dashboard';
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
            window.location.href = '/dashboard';
        } else {
            errorMsg.textContent = '❌ Incorrect password';
            errorMsg.classList.remove('hidden');
        }
    } catch (error) {
        errorMsg.textContent = '❌ Login error';
        errorMsg.classList.remove('hidden');
    }
}
