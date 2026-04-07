// Service Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
});

async function checkAuth() {
    // Only redirect if we're on the login page
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        try {
            const response = await fetch('/api/admin/check');
            const data = await response.json();

            if (data.is_admin && window.location.pathname === '/') {
                window.location.href = '/dashboard';
            }
        } catch (error) {
            console.error('Error checking auth:', error);
        }
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('loginError');
    errorMsg.classList.add('hidden');

    try {
        const response = await fetch('/api/service/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = '/dashboard';
        } else {
            errorMsg.textContent = '❌ ' + (data.message || 'Invalid username or password');
            errorMsg.classList.remove('hidden');
        }
    } catch (error) {
        errorMsg.textContent = '❌ Login error. Please try again.';
        errorMsg.classList.remove('hidden');
    }
}

async function handleLogout() {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (error) {
        console.error('Error logging out:', error);
        window.location.href = '/';
    }
}
