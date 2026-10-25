
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import requests

QUICKML_ENDPOINT_URL = os.getenv("QUICKML_ENDPOINT_URL", "")


def predict(input_df: pd.DataFrame):
    required = [
        "timestamp",
        "ambient_temp_c",
        "humidity_pct",
        "solar_irradiance_wm2",
    ]

    missing = [c for c in required if c not in input_df.columns]
    if missing:
        raise ValueError(f"Missing input columns: {missing}")

    if not QUICKML_ENDPOINT_URL:
        raise RuntimeError("Set QUICKML_ENDPOINT_URL first.")

    header_names = {
        "Authorization": "QUICKML_AUTHORIZATION",
        "X-QuickML-Endpoint-Key": "QUICKML_ENDPOINT_KEY",
        "Catalyst-Org": "CATALYST_ORG",
        "Environment": "QUICKML_ENVIRONMENT",
    }

    headers = {"Content-Type": "application/json"}

    for header, env_name in header_names.items():
        value = os.getenv(env_name)
        if not value:
            raise RuntimeError(f"Missing environment variable: {env_name}")
        headers[header] = value

    def predict_one(item):
        index, timestamp = item
        payload = {"data": {"timestamp": str(timestamp)}}

        response = requests.post(
            QUICKML_ENDPOINT_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()

        result = response.json().get("result")

        if isinstance(result, dict):
            key = str(timestamp)
            if key in result:
                value = result[key]
            elif len(result) == 1:
                value = next(iter(result.values()))
            else:
                raise ValueError(f"Unexpected result: {result}")

        elif isinstance(result, list) and len(result) == 1:
            value = result[0]

        else:
            raise ValueError(f"Unexpected result: {result}")

        return index, float(value)

    predictions = [None] * len(input_df)
    items = list(enumerate(input_df["timestamp"]))

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(predict_one, item)
            for item in items
        ]

        for completed, future in enumerate(as_completed(futures), 1):
            index, value = future.result()
            predictions[index] = value

            if completed % 25 == 0 or completed == len(items):
                print(f"Completed {completed}/{len(items)} predictions")

    predictions = np.asarray(predictions, dtype=float)

    if not np.isfinite(predictions).all():
        raise ValueError("QuickML returned invalid predictions.")

    return predictions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    preds = predict(df)

    pd.DataFrame({
        "timestamp": df["timestamp"],
        "target_demand_kw": preds,
    }).to_csv(args.output, index=False)

    print(f"Saved {len(preds)} predictions to {args.output}")
