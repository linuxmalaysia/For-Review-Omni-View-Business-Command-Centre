/**
 * Loads the authenticated user's profile and updates available profile elements.
 *
 * Redirects unauthenticated users to `login.html` and stops when authentication
 * or profile retrieval fails. Uses a cached profile when available.
 */
async function loadUserData() {

    const {
        data: { user },
        error: authError
    } = await supabaseClient.auth.getUser();

    if (authError || !user) {
        console.error("No logged-in user:", authError);
        window.location.href = "login.html";
        return;
    }

    console.log("Logged in email:", user.email);

    let data = window.SessionCache ? window.SessionCache.get(`user_profile_${user.email}`) : null;

    if (!data) {
        const { data: profileData, error } = await supabaseClient
            .from("profiles")
            .select("username, phone, email")
            .eq("email", user.email)
            .maybeSingle();

        if (error) {
            console.error("Profile loading error:", error);
            return;
        }

        if (!profileData) {
            console.error("Profile not found.");
            return;
        }

        data = profileData;
        if (window.SessionCache) {
            window.SessionCache.set(`user_profile_${user.email}`, data);
        }
    }

    console.log("Profile:", data);


    // Profile page
    const userNameElement =
        document.getElementById("user_name");

    const profileNameElement =
        document.getElementById("profile_name");

    const profileEmailElement =
        document.getElementById("profile_email");

    const profilePhoneElement =
        document.getElementById("profile_phone");

    const welcomename=
        document.getElementById("welcome_name");


    if (userNameElement) {
        userNameElement.innerText =
            `Welcome, ${data.username}!`;
    }

    if (profileNameElement) {
        profileNameElement.innerText =
            data.username;
    }

    if (profileEmailElement) {
        profileEmailElement.innerText =
            data.email;
    }

    if (profilePhoneElement) {
        profilePhoneElement.innerText =
            data.phone;
    }

    if(welcomename){
        welcomename.innerText =
            data.username;
    }


    // Edit profile page
    const updateName =
        document.getElementById("update_name");

    const updatePhone =
        document.getElementById("update_phone");


    if (updateName) {
        updateName.value = data.username;
    }

    if (updatePhone) {
        updatePhone.value = data.phone;
    }
}


document.addEventListener("DOMContentLoaded", function () {
    loadUserData();
});