import os
import requests


def download_oecd_data(dataset_code: str = "AIR_GHG", destination: str = "data/raw", replace: bool = False) -> str:
    """
    Downloads ESG-related data from the OECD API and saves it as a CSV file.
    
    Args:
        dataset_code (str): OECD dataset code (e.g., 'AIR_GHG' for greenhouse gas emissions).
        destination (str): Directory where the CSV file will be saved.
        replace (bool): If False, existing files won't be overwritten. If True, existing file will be replaced.
    
    Returns:
        str: The path to the saved CSV file.
    """
    os.makedirs(destination, exist_ok=True)
    output_path = os.path.join(destination, "oecd_esg.csv")

    if os.path.exists(output_path) and not replace:
        print(f"File already exists, skipping download (replace=False): {output_path}")
        return output_path

    url = f"https://stats.oecd.org/SDMX-JSON/data/{dataset_code}/all?contentType=csv"
    print(f"Downloading OECD dataset: {dataset_code}")
    print(f"API URL: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch data. HTTP {response.status_code}: {response.text[:200]}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Dataset saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    # Example: CO₂ emissions per capita (AIR_GHG)
    dataset_path = download_oecd_data("AIR_GHG")
    print(f"OECD ESG data stored at: {dataset_path}")
