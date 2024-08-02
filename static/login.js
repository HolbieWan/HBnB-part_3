document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.msg}`);
                return;
            }

            const data = await response.json();
            const token = data.access_token;
            const userId = data.user_id;  // Make sure this is being returned by the server

            // Store the token and user ID in cookies
            document.cookie = `jwt_token=${token}; path=/; secure; SameSite=Strict`;
            document.cookie = `user_id=${userId}; path=/; secure; SameSite=Strict`;  // Set user_id in cookie

            // Redirect to the home page
            window.location.href = '/';

        } catch (error) {
            console.error('Error logging in:', error);
            alert('An error occurred. Please try again.');
        }
    });
});
