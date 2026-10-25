
const demandElement = document.getElementById("demand");
const modeElement = document.getElementById("mode");
const alertElement = document.getElementById("alert");
const countElement = document.getElementById("record-count");
const messageElement = document.getElementById("message");
const tableBody = document.getElementById("forecast-body");

function renderDashboard(records) {
    if (!Array.isArray(records) || records.length === 0) {
        messageElement.textContent = "No forecast records available yet.";
        return;
    }

    const latest = records[0];

    demandElement.innerHTML =
        `${Number(latest.predicted_demand_kw).toFixed(2)} <small>kW</small>`;

    modeElement.textContent = latest.power_mode;

    const hasAlert = latest.critical_overload_alert === true ||
        String(latest.critical_overload_alert).toLowerCase() === "true";

    alertElement.textContent = hasAlert ? "CRITICAL" : "Normal";
    alertElement.style.color = hasAlert ? "#b42318" : "#16845b";

    countElement.textContent = `${records.length} records`;
    messageElement.textContent = "Forecast data loaded successfully.";

    tableBody.replaceChildren();

    records.forEach(record => {
        const row = document.createElement("tr");

        const values = [
            record.timestamp,
            `${Number(record.predicted_demand_kw).toFixed(2)} kW`,
            record.power_mode,
            (
                record.critical_overload_alert === true ||
                String(record.critical_overload_alert).toLowerCase() === "true"
            ) ? "Critical Alert" : "Normal"
        ];

       
values.forEach((value, index) => {
    const cell = document.createElement("td");

    if (index === 2 || index === 3) {
        const badge = document.createElement("span");
        badge.textContent = value;

        if (index === 2) {
            badge.className = "mode-tag";
        } else {
            badge.className = value === "Critical Alert"
                ? "alert-tag"
                : "normal-tag";
        }

        cell.appendChild(badge);
    } else {
        cell.textContent = value;
    }

    row.appendChild(cell);
});

        tableBody.appendChild(row);
    });
}

fetch("/api/forecast")
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to load forecast data");
        }
        return response.json();
    })
    .then(records => {
        renderDashboard(records);
    })
    .catch(error => {
        console.error(error);
        messageElement.textContent =
            "Could not load forecast data. Please try again.";
    });
