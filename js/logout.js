/**
 * Logs out the current user and redirects to the login page.
 * @param {Event} [event] - Optional event whose default action is prevented.
 */
async function logout(event) {
    if (event) event.preventDefault();

    if (window.SessionCache) {
        window.SessionCache.clearAll();
    }

    // 1. Sign out of Supabase session
    const { error } = await supabaseClient.auth.signOut();

    if (error) {
        console.error("Error logging out:", error.message);
        alert("Failed to log out. Please try again.");
        return;
    }

    // 2. Redirect back to login page
    console.log("Successfully logged out.");
    window.location.href = 'login.html';
}