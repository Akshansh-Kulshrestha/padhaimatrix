function addExp() {
    let div = document.createElement("div");
    div.innerHTML = `<input name="company[]" placeholder="Company"><input name="role[]" placeholder="Role">`;
    document.getElementById("exp-container").appendChild(div);
}

function addEdu() {
    let div = document.createElement("div");
    div.innerHTML = `<input name="degree[]" placeholder="Degree"><input name="edu_institute[]" placeholder="Institute">`;
    document.getElementById("edu-container").appendChild(div);
}

function addQual() {
    let input = document.createElement("input");
    input.name = "qualification[]";
    input.placeholder = "Qualification";
    document.getElementById("qual-container").appendChild(input);
}

// PINCODE AUTO
document.getElementById("pincode").addEventListener("blur", function () {
    let pincode = this.value;

    if (pincode.length === 6) {
        fetch(`https://api.postalpincode.in/pincode/${pincode}`)
            .then(res => res.json())
            .then(data => {
                if (data[0].Status === "Success") {
                    document.getElementById("city").value = data[0].PostOffice[0].District;
                    document.getElementById("state").value = data[0].PostOffice[0].State;
                }
            });
    }
});

function addExperience() {
    let container = document.getElementById("experience-container");

    let div = document.createElement("div");
    div.classList.add("exp-block");

    div.innerHTML = `
        <label>Company</label>
        <input type="text" name="company[]">

        <label>Role</label>
        <input type="text" name="role[]">

        <label>Start Date</label>
        <input type="date" name="start_date[]">

        <label>End Date</label>
        <input type="date" name="end_date[]">
    `;

    container.appendChild(div);
}

function addEducation() {
    let container = document.getElementById("education-container");

    let div = document.createElement("div");
    div.classList.add("edu-block");

    div.innerHTML = `
        <label>Degree</label>
        <input type="text" name="degree[]">

        <label>Institute</label>
        <input type="text" name="edu_institute[]">

        <label>Year</label>
        <input type="text" name="year[]">
    `;

    container.appendChild(div);
}

let isFormDirty = false;

// Detect input changes
document.querySelectorAll("form input, form textarea").forEach(input => {
    input.addEventListener("change", () => {
        isFormDirty = true;
    });
});

// Warn before leaving
window.addEventListener("beforeunload", function (e) {
    if (isFormDirty) {
        e.preventDefault();
        e.returnValue = "";
    }
});

document.querySelector("form").addEventListener("submit", function () {
    isFormDirty = false;
});

function confirmLeave() {
    if (isFormDirty) {
        return confirm("You have unsaved changes. Are you sure you want to leave?");
    }
    return true;
}