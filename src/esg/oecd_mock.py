# src/esg/oecd_mock.py
import os
import pandas as pd
import numpy as np
from pathlib import Path

def generate_mock_oecd(destination: str = "data/raw"):
    os.makedirs(destination, exist_ok=True)
    output = Path(destination) / "oecd_esg.csv"

    regions = [
        "Europe", "North America", "Latin America", "Asia",
        "Africa", "Middle East", "Oceania"
    ]
    years = list(range(2015, 2025))
    rng = np.random.default_rng(1)
    rows = []
    for r in regions:
        for y in years:
            rows.append({
                "Region": r,
                "Year": y,
                "OECD_CO2pc": rng.uniform(5000, 120000),
                "OECD_SocSpendGDP": rng.uniform(5000, 20000)
            })
    pd.DataFrame(rows).to_csv(output, index=False)
    print(f"Mock OECD ESG dataset saved to {output}")

if __name__ == "__main__":
    generate_mock_oecd()
