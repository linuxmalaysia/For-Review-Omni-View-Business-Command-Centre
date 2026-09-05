const resetURL = new URL(
    "./reset_password.html",
    window.location.href
).href;

document.getElementById('forgotPasswordForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email')?.value.trim();

    if (!email) {
        alert('Please enter your email address.');
        return;
    }

    const { error } = await supabaseClient.auth.resetPasswordForEmail(email, {
        redirectTo: resetURL,
    });

    if (error) {
        alert('Error sending reset link: ' + error.message);
    } else {
        alert('A password reset link has been sent to your email address.');
    }
});
