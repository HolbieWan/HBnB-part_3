document.addEventListener('DOMContentLoaded', function () {
    const navMenu = document.getElementById('nav-menu');
    const jwtToken = getCookie('jwt_token');

    if (jwtToken) {
        const logoutLink = document.createElement('li');
        logoutLink.classList.add('nav-item');
        logoutLink.innerHTML = '<a href="#" class="nav-link" id="logout-button">Logout</a>';
        navMenu.appendChild(logoutLink);

        document.getElementById('logout-button').addEventListener('click', async function () {
            await logout();
        });
    } else {
        const loginLink = document.createElement('li');
        loginLink.classList.add('nav-item');
        loginLink.innerHTML = '<a href="/login" class="nav-link">Login</a>';
        navMenu.appendChild(loginLink);
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getCookie('jwt_token')}`
            }
        });

        if (response.ok) {
            clearCookies();
            window.location.href = '/login';
        } else {
            console.error('Failed to log out');
        }
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

function clearCookies() {
    document.cookie = 'jwt_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; secure; SameSite=Strict';
    document.cookie = 'user_id=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; secure; SameSite=Strict';
}
