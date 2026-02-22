// ---------------- PAGE SWITCH ----------------

function showPage(id) {
    document.querySelectorAll(".page").forEach(p => p.classList.add("hidden"));
    const el = document.getElementById(id);
    if (el) el.classList.remove("hidden");
}

// ensure elements exist before binding
window.addEventListener("DOMContentLoaded", () => {
    const regForm = document.getElementById("registrationForm");
    if (regForm) {
        regForm.addEventListener("submit", async e => {
            e.preventDefault();
            try {
                const res = await fetch("/register/", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        name: document.getElementById("name").value,
                        age: document.getElementById("age").value,
                        bloodGroup: document.getElementById("bloodGroup").value,
                        phone: document.getElementById("phone").value,
                        language: document.getElementById("language").value
                    })
                });
                const data = await res.json();
                document.getElementById("qrcode").innerText = data.patient_id;
                document.querySelector("#qrContainer h3").innerText =
                    "Health ID: " + data.patient_id;
                document.getElementById("qrContainer").classList.remove("hidden");
            } catch (err) {
                console.error("registration failed", err);
                alert("Registration failed, please try again");
            }
        });
    }

    const loginForm = document.getElementById("patientLoginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async e => {
            e.preventDefault();
            try {
                const res = await fetch("/patient-login/", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        health_id: document.getElementById("loginHealthId").value,
                        phone: document.getElementById("loginPhone").value
                    })
                });
                const data = await res.json();
                if (data.status === "ok") {
                    showPage("patientDashboardPage");
                } else {
                    alert("Invalid login");
                }
            } catch (err) {
                console.error("login error", err);
                alert("Login error");
            }
        });
    }

    const docForm = document.getElementById("doctorLoginForm");
    if (docForm) {
        docForm.addEventListener("submit", e => {
            e.preventDefault();
            showPage("doctorDashboardPage");
        });
    }
});

async function addDoctorRecord() {
    const health_id = document.getElementById("doctorPatientSearch")?.value;
    if (!health_id) {
        alert("Enter a health ID first");
        return;
    }

    const payload = {
        health_id,
        date: prompt("Date (YYYY-MM-DD)"),
        description: prompt("Symptoms"),
        diagnosis: prompt("Diagnosis"),
        prescription: prompt("Prescription"),
        doctor: "Doctor" // replace with real user name
    };

    try {
        const res = await fetch("/add-record/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(res.statusText);
        alert("Record added");
    } catch (err) {
        console.error("add record failed", err);
        alert("Failed to add record");
    }
}

// fetch and display records for given health ID
async function loadPatientRecords(id) {
    try {
        const res = await fetch(`/records/${encodeURIComponent(id)}/`);
        if (!res.ok) throw new Error(res.statusText);
        const data = await res.json();
        let html = "";
        data.records.forEach(r => {
            html += `
            <div class="record-item">
                <p>${r.date}</p>
                <p>${r.description}</p>
                <p>${r.diagnosis}</p>
                <p>${r.prescription}</p>
                <p>${r.doctor}</p>
            </div>`;
        });
        const container = document.getElementById("patientRecords");
        if (container) container.innerHTML = html;
    } catch (err) {
        console.error("load records failed", err);
        alert("Could not load patient records");
    }
}

// doctor search patient by health_id
async function loadDoctorPatientLive() {
    const health_id = document.getElementById("doctorPatientSearch")?.value?.trim();
    if (!health_id) {
        alert("Enter a health ID to search");
        return;
    }

    try {
        const res = await fetch(`/search-patient/?health_id=${encodeURIComponent(health_id)}`);
        if (!res.ok) throw new Error(res.statusText);
        const data = await res.json();
        
        if (data.status === "ok") {
            const pt = data.patient;
            let infoHtml = `
            <div class="info-box">
                <p><strong>Name:</strong> ${pt.name || "N/A"}</p>
                <p><strong>Health ID:</strong> ${pt.health_id}</p>
                <p><strong>Age:</strong> ${pt.age || "N/A"}</p>
                <p><strong>Phone:</strong> ${pt.phone}</p>
                <p><strong>Blood Group:</strong> ${pt.blood_group || "N/A"}</p>
                <p><strong>Language:</strong> ${pt.language || "N/A"}</p>
            </div>`;
            document.getElementById("doctorPatientInfo").innerHTML = infoHtml;
            
            // load records for this patient
            await loadPatientRecords(health_id);
        } else {
            alert(data.error || "Patient not found");
        }
    } catch (err) {
        console.error("search failed", err);
        alert("Error searching for patient");
    }
}

// doctor add record to patient
async function addDoctorRecordLive() {
    const health_id = document.getElementById("doctorPatientSearch")?.value?.trim();
    if (!health_id) {
        alert("Search for a patient first");
        return;
    }

    const payload = {
        health_id,
        date: prompt("Date (YYYY-MM-DD)"),
        description: prompt("Symptoms"),
        diagnosis: prompt("Diagnosis"),
        prescription: prompt("Prescription"),
        doctor: prompt("Doctor Name", "Doctor")
    };

    // cancel if user hit cancel on any prompt
    if (!payload.date || !payload.description || !payload.diagnosis || !payload.prescription) {
        return;
    }

    try {
        const res = await fetch("/add-record/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(res.statusText);
        alert("Record added successfully");
        // reload records
        await loadPatientRecords(health_id);
    } catch (err) {
        console.error("add record failed", err);
        alert("Failed to add record");
    }

}
