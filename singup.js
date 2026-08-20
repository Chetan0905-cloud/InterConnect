const roleSelection = document.getElementById("roleSelection");

const seekerRole = document.getElementById("seekerRole");
const supporterRole = document.getElementById("supporterRole");

const seekerForm = document.getElementById("seekerForm");
const supporterForm = document.getElementById("supporterForm");

const backFromSeeker = document.getElementById("backFromSeeker");
const backFromSupporter = document.getElementById("backFromSupporter");

seekerRole.addEventListener("click", function () {
    roleSelection.classList.add("hidden");
    seekerForm.classList.remove("hidden");
});

supporterRole.addEventListener("click", function () {
    roleSelection.classList.add("hidden");
    supporterForm.classList.remove("hidden");
});

backFromSeeker.addEventListener("click", function () {
    seekerForm.classList.add("hidden");
    roleSelection.classList.remove("hidden");
});

backFromSupporter.addEventListener("click", function () {
    supporterForm.classList.add("hidden");
    roleSelection.classList.remove("hidden");
});

seekerForm.addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Support seeker account created successfully!");
});

supporterForm.addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Supporter account submitted for verification!");
});