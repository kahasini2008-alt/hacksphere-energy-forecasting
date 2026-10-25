
const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

const dataPath = path.join(__dirname, "dashboard_data.csv");

// Serve the frontend files from the public folder
app.use(express.static(path.join(__dirname, "public")));

// API endpoint for forecast data
app.get("/api/forecast", (req, res) => {
    fs.readFile(dataPath, "utf8", (error, csv) => {
        if (error) {
            return res.status(500).json({
                error: "Could not read dashboard forecast data."
            });
        }

        const lines = csv.trim().split(/\r?\n/);
        const headers = lines[0].split(",");

        const records = lines.slice(1).filter(Boolean).map(line => {
            const values = line.split(",");

            return {
                timestamp: values[0],
                predicted_demand_kw: Number(values[1]),
                power_mode: values[2],
                critical_overload_alert: values[3].toLowerCase() === "true"
            };
        });

        res.json(records);
    });
});

app.listen(PORT, () => {
    console.log(`EnergyGrid server running at http://localhost:${PORT}`);
});
