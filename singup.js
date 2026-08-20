const roleSelection = document.getElementById("roleSelection");

const seekerRole = document.getElementById("seekerRole");
const supporterRole = document.getElementById("supporterRole");

const seekerForm = document.getElementById("seekerForm");
const supporterForm = document.getElementById("supporterForm");

const backFromSeeker = document.getElementById("backFromSeeker");
const backFromSupporter = document.getElementById("backFromSupporter");


/* =========================
   ROLE SELECTION
========================= */

seekerRole.addEventListener("click", function () {

    roleSelection.classList.add("hidden");
    seekerForm.classList.remove("hidden");

});


supporterRole.addEventListener("click", function () {

    roleSelection.classList.add("hidden");
    supporterForm.classList.remove("hidden");

});


/* =========================
   BACK BUTTONS
========================= */

backFromSeeker.addEventListener("click", function () {

    seekerForm.classList.add("hidden");
    roleSelection.classList.remove("hidden");

});


backFromSupporter.addEventListener("click", function () {

    supporterForm.classList.add("hidden");
    roleSelection.classList.remove("hidden");

});


/* =========================
   SUPPORT SEEKER SIGNUP
========================= */

seekerForm.addEventListener("submit", function (e) {

    e.preventDefault();

    const user = {

        name: document.getElementById("seekerName").value.trim(),

        email: document.getElementById("seekerEmail").value.trim(),

        password: document.getElementById("seekerPassword").value,

        age: document.getElementById("seekerAge").value,

        location: document.getElementById("seekerLocation").value.trim(),

        interests: document.getElementById("seekerInterests").value.trim(),

        role: "Support Seeker"

    };


    /* SAVE USER */

    localStorage.setItem(
        "interconnectUser",
        JSON.stringify(user)
    );


    alert("Support seeker account created successfully!");


    /* GO TO DASHBOARD */

    window.location.href = "dashboard.html";

});


/* =========================
   SUPPORTER SIGNUP
========================= */

supporterForm.addEventListener("submit", function (e) {

    e.preventDefault();


    const availability =
        document.querySelector(
            'input[name="availability"]:checked'
        ).value;


    const user = {

        name: document.getElementById("supporterName").value.trim(),

        email: document.getElementById("supporterEmail").value.trim(),

        password: document.getElementById("supporterPassword").value,

        qualification:
            document.getElementById("qualification").value.trim(),

        college:
            document.getElementById("college").value.trim(),

        location:
            document.getElementById("supporterLocation").value.trim(),

        bio:
            document.getElementById("bio").value.trim(),

        availability: availability,

        role: "Supporter"

    };


    /* SAVE USER */

    localStorage.setItem(
        "interconnectUser",
        JSON.stringify(user)
    );


    alert("Supporter account submitted for verification!");


    /* GO TO DASHBOARD */

    window.location.href = "dashboard.html";

});