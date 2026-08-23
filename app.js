const signupLink = document.getElementById("showSignup");
const signupOverlay = document.getElementById("signupOverlay");
const closeSignup = document.getElementById("closeSignup");

const roleSelection = document.getElementById("roleSelection");

const supportUser = document.getElementById("supportUser");
const supporterUser = document.getElementById("supporterUser");

const seekerSignupForm = document.getElementById("seekerSignupForm");
const supporterSignupForm = document.getElementById("supporterSignupForm");

const backToRoles = document.getElementById("backToRoles");
const backToRoles2 = document.getElementById("backToRoles2");


/* OPEN SIGNUP */

signupLink.addEventListener("click", function (event) {
    event.preventDefault();

    signupOverlay.classList.add("active");

    roleSelection.style.display = "block";
    seekerSignupForm.style.display = "none";
    supporterSignupForm.style.display = "none";
});


/* CLOSE SIGNUP */

closeSignup.addEventListener("click", function () {
    signupOverlay.classList.remove("active");
});


/* SUPPORT SEEKER */

supportUser.addEventListener("click", function () {

    roleSelection.style.display = "none";
    seekerSignupForm.style.display = "block";
    supporterSignupForm.style.display = "none";

});


/* SUPPORTER */

supporterUser.addEventListener("click", function () {

    roleSelection.style.display = "none";
    seekerSignupForm.style.display = "none";
    supporterSignupForm.style.display = "block";

});


/* BACK BUTTONS */

backToRoles.addEventListener("click", function () {

    seekerSignupForm.style.display = "none";
    supporterSignupForm.style.display = "none";
    roleSelection.style.display = "block";

});


backToRoles2.addEventListener("click", function () {

    seekerSignupForm.style.display = "none";
    supporterSignupForm.style.display = "none";
    roleSelection.style.display = "block";

});


/* CLOSE WHEN CLICKING OUTSIDE */

signupOverlay.addEventListener("click", function (event) {

    if (event.target === signupOverlay) {
        signupOverlay.classList.remove("active");
    }

});

/* =========================
   SUPPORT SEEKER SIGNUP
========================= */

document.getElementById("seekerForm").addEventListener("submit", async function (event) {

    event.preventDefault();

    const user = {
        name: document.getElementById("seekerName").value.trim(),
        email: document.getElementById("seekerEmail").value.trim(),
        password: document.getElementById("seekerPassword").value,
        age: document.getElementById("seekerAge").value,
        location: document.getElementById("seekerLocation").value.trim(),
        interests: document.getElementById("seekerInterests").value.trim(),
        role: "seeker"
    };

    try {

        const response = await fetch("https://interconnect-production-9022.up.railway.app/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(user)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        // Keep profile information locally for the dashboard
        localStorage.setItem(
            "interconnectUser",
            JSON.stringify({
                name: user.name,
                email: user.email,
                age: user.age,
                location: user.location,
                interests: user.interests,
                role: "seeker"
            })
        );

        alert("Support seeker account created successfully!");

        window.location.href = "dashboard.html";

    } catch (error) {

        console.error("Signup error:", error);

        alert(
            "Unable to connect to the server. Make sure the Flask backend is running."
        );
    }

});


/* =========================
   SUPPORTER SIGNUP
========================= */

document.getElementById("supporterForm").addEventListener("submit", async function (event) {

    event.preventDefault();

    const supporter = {
        name: document.getElementById("supporterName").value.trim(),
        email: document.getElementById("supporterEmail").value.trim(),
        password: document.getElementById("supporterPassword").value,
        qualification: document.getElementById("qualification").value.trim(),
        college: document.getElementById("college").value.trim(),
        location: document.getElementById("supporterLocation").value.trim(),
        bio: document.getElementById("supporterBio").value.trim(),
        role: "supporter"
    };

    try {

        const response = await fetch("https://interconnect-production-9022.up.railway.app/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(supporter)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message);
            return;
        }

        // Keep profile information locally for the dashboard
        localStorage.setItem(
            "interconnectUser",
            JSON.stringify({
                name: supporter.name,
                email: supporter.email,
                qualification: supporter.qualification,
                college: supporter.college,
                location: supporter.location,
                bio: supporter.bio,
                role: "supporter"
            })
        );

        alert(
            "Your supporter application has been submitted for verification."
        );

        window.location.href = "dashboard.html";

    } catch (error) {

        console.error("Signup error:", error);

        alert(
            "Unable to connect to the server. Make sure the Flask backend is running."
        );
    }

});
/* LOGIN */

document.getElementById("loginForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("https://interconnect-production-9022.up.railway.app/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const result = await response.json();

    if (result.success) {

        localStorage.setItem(
            "interconnectUser",
            JSON.stringify(result.user)
        );

        alert("Login successful!");

        window.location.href = "dashboard.html";

    } else {

        alert(result.message);
    }

});
