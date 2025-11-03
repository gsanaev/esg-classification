"""
eu_taxonomy.py

Generates or downloads EU Taxonomy ESG indicators and saves them to data/raw/eu_taxonomy_esg.csv.
Currently uses simulated data aligned with regions and years for consistency testing.
"""

import os
import pandas as pd
from pathlib import Path
import numpy as np


def generate_eu_taxonomy_data(destination: str = "data/raw") -> str:
    """
    Creates a synthetic EU Taxonomy ESG dataset for testing.
    Returns path to saved CSV.
    """
    os.makedirs(destination, exist_ok=True)
    output_path = Path(destination) / "eu_taxonomy_esg.csv"

    # Define regions and years consistent with other datasets
    regions = [
        "Europe", "North America", "Latin America", "Asia",
        "Africa", "Middle East", "Oceania"
    ]
    years = list(range(2015, 2025))

    records = []
    rng = np.random.default_rng(42)
    for region in regions:
        for year in years:
            green_investment = rng.uniform(10, 60)  # %
            emission_intensity = rng.uniform(50, 300)  # tons CO₂ per $M revenue
            records.append({
                "Region": region,
                "Year": year,
                "EU_GreenInvestment": round(green_investment, 2),
                "EU_EmissionIntensity": round(emission_intensity, 2),
            })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Saved EU Taxonomy ESG dataset to {output_path} ({len(df)} rows).")
    return str(output_path)


if __name__ == "__main__":
    path = generate_eu_taxonomy_data()
    print(f"EU Taxonomy data stored at: {path}")
