
import pandas as pd
from energy_logic import get_energy_status

INPUT_FILE = "predictions.csv"
OUTPUT_FILE = "dashboard_data.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    required = ["timestamp", "target_demand_kw"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    records = []

    for _, row in df.iterrows():
        status = get_energy_status(
            row["timestamp"],
            row["target_demand_kw"],
        )
        records.append(status)

    result = pd.DataFrame(records)
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"Created {OUTPUT_FILE}")
    print(f"Rows: {len(result)}")
    print("Columns:", list(result.columns))
    print(result.head())


if __name__ == "__main__":
    main()
