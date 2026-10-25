# Smart Energy Microgrid & Demand Forecasting Engine

## Overview
An energy-demand forecasting prototype that predicts demand for upcoming timestamps and recommends an energy source mode based on predicted demand and time of day.

## Features
- Hourly demand forecasting through a published QuickML endpoint.
- Renewable Storage Mode when predicted demand exceeds 160 kW or the hour is between 18:00 and 22:00 inclusive.
- Main Grid Mode otherwise.
- Critical Overload Alert when predicted demand is at least 200 kW.
- Dashboard displaying predictions, energy modes, and overload alerts.

## Technology Stack
- Python, Pandas, NumPy, Requests
- Node.js, Express
- HTML, CSS, JavaScript
- Zoho QuickML and Zoho Catalyst (deployment pending)

## Local Setup
1. Install Python and Node.js.
2. Install Python dependencies: `pip install pandas numpy requests`.
3. Install Node.js dependencies: `npm install`.
4. Configure the required QuickML environment variables before running predictions.
5. Generate predictions and dashboard data using the project scripts.
6. Start the dashboard with `node server.js`.

## Environment Variables
- `QUICKML_ENDPOINT_URL`
- `QUICKML_AUTHORIZATION`
- `QUICKML_ENDPOINT_KEY`
- `CATALYST_ORG`
- `QUICKML_ENVIRONMENT`

Never commit access tokens, refresh tokens, client secrets, or endpoint keys.

## Current Status
Local dashboard prototype implemented. QuickML integration is being validated. Zoho Catalyst deployment and final submission checks are pending.
