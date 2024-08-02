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

document.getElementById('logout-button').addEventListener('click', logout);
