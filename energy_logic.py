
from datetime import datetime


def get_energy_status(timestamp, predicted_demand_kw):
    # Convert timestamp into a datetime object
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)

    hour = timestamp.hour
    demand = float(predicted_demand_kw)

    # Switching rule
    if demand > 160 or 18 <= hour <= 22:
        power_mode = "Renewable Storage Mode"
    else:
        power_mode = "Main Grid Mode"

    # Independent overload alert
    critical_overload = demand >= 200

    return {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "predicted_demand_kw": demand,
        "power_mode": power_mode,
        "critical_overload_alert": critical_overload,
    }
