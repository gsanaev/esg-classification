import pandas as pd
import time
import urllib.error

def safe_read_csv(url, max_retries=5, base_delay=5):
    """Download a CSV from OECD API with retry on 429/5xx errors."""
    for attempt in range(max_retries):
        try:
            return pd.read_csv(url)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = base_delay * (2 ** attempt)
                print(f"HTTP {e.code} from OECD — waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                raise
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            raise
    raise RuntimeError(f"Failed after {max_retries} attempts: {url}")

def download_oecd_ghg(start_year=2015, end_year=None):
    base_url = "https://sdmx.oecd.org/public/rest/data/"
    dataset = "OECD.ENV.EPI,DSD_AIR_GHG@DF_AIR_GHG,1.0"
    query = f"/.A.GHG._T.KG_CO2E_PS?startPeriod={start_year}"
    if end_year:
        query += f"&endPeriod={end_year}"
    url = f"{base_url}{dataset}{query}&dimensionAtObservation=AllDimensions&format=csv"
    print(f"Downloading GHG data: {url}\n")
    df = safe_read_csv(url)
    print(f"Columns returned by OECD GHG API: {list(df.columns)}")
    df = df.rename(columns={
        "REF_AREA": "CountryCode",
        "TIME_PERIOD": "Year",
        "OBS_VALUE": "GHG_Emissions_kgCO2eq_perCapita"
    })
    df["CountryName"] = df["CountryCode"]
    df = df[["CountryCode", "CountryName", "Year", "GHG_Emissions_kgCO2eq_perCapita"]]
    df.dropna(subset=["GHG_Emissions_kgCO2eq_perCapita"], inplace=True)
    return df

def download_oecd_social_expenditure(start_year=2015, end_year=None):
    base_url = "https://sdmx.oecd.org/public/rest/data/"
    dataset = "OECD.ELS.SPD,DSD_SOCX_AGG@DF_SOCX_AGG,1.0"
    query = f"/.A.SOCX.PT_B1GQ.ES10._T._T.?startPeriod={start_year}"
    if end_year:
        query += f"&endPeriod={end_year}"
    url = f"{base_url}{dataset}{query}&dimensionAtObservation=AllDimensions&format=csv"
    print(f"Downloading Social Expenditure data: {url}\n")
    df = safe_read_csv(url)
    print(f"Columns returned by OECD SOCX API: {list(df.columns)}")
    df = df.rename(columns={
        "REF_AREA": "CountryCode",
        "TIME_PERIOD": "Year",
        "OBS_VALUE": "Social_Expenditure_Percent_GDP"
    })
    df["CountryName"] = df["CountryCode"]
    df = df[["CountryCode", "CountryName", "Year", "Social_Expenditure_Percent_GDP"]]
    df.dropna(subset=["Social_Expenditure_Percent_GDP"], inplace=True)
    return df

def download_oecd_renewable_energy(start_year=2015, end_year=None):
    base_url = "https://sdmx.oecd.org/public/rest/data/"
    dataset = "OECD.WISE.RSB,DSD_SDG@DF_SDG_G_7,1.0"
    query = f"/...C070201.._T._T._T._T._T.?startPeriod={start_year}"
    if end_year:
        query += f"&endPeriod={end_year}"
    url = f"{base_url}{dataset}{query}&dimensionAtObservation=AllDimensions&format=csv"
    print(f"Downloading Renewable Energy data: {url}\n")
    df = safe_read_csv(url)
    print(f"Columns returned by OECD Renewable API: {list(df.columns)}")
    df = df.rename(columns={
        "REF_AREA": "CountryCode",
        "TIME_PERIOD": "Year",
        "OBS_VALUE": "Renewable_Energy_Share_Percent"
    })
    df["CountryName"] = df["CountryCode"]
    df = df[["CountryCode", "CountryName", "Year", "Renewable_Energy_Share_Percent"]]
    df.dropna(subset=["Renewable_Energy_Share_Percent"], inplace=True)
    return df

def download_oecd_trust_in_government(start_year=2015, end_year=None):
    base_url = "https://sdmx.oecd.org/public/rest/data/"
    dataset = "OECD.GOV.GIP,DSD_GOV_INT@DF_GOV_TDG_2025,1.0"
    query = f"/A.......?startPeriod={start_year}"
    if end_year:
        query += f"&endPeriod={end_year}"
    url = f"{base_url}{dataset}{query}&dimensionAtObservation=AllDimensions&format=csv"
    print(f"Downloading Trust in Government data: {url}\n")
    df = safe_read_csv(url)
    print(f"Columns returned by OECD Trust API: {list(df.columns)}")
    df = df.rename(columns={
        "REF_AREA": "CountryCode",
        "TIME_PERIOD": "Year",
        "OBS_VALUE": "Trust_in_Government_Percent"
    })
    df["CountryName"] = df["CountryCode"]
    df = df[["CountryCode", "CountryName", "Year", "Trust_in_Government_Percent"]]
    df.dropna(subset=["Trust_in_Government_Percent"], inplace=True)
    return df

def download_all_oecd_esg(start_year=2015, end_year=None, save_path=None):
    print("Fetching GHG emissions...")
    ghg = download_oecd_ghg(start_year, end_year)
    time.sleep(3)

    print("Fetching social expenditure...")
    socx = download_oecd_social_expenditure(start_year, end_year)
    time.sleep(3)

    print("Fetching renewable energy share...")
    ren = download_oecd_renewable_energy(start_year, end_year)
    time.sleep(3)

    print("Fetching trust in government...")
    trust = download_oecd_trust_in_government(start_year, end_year)
    time.sleep(3)

    df = ghg.merge(socx, on=["CountryCode", "CountryName", "Year"], how="outer")
    df = df.merge(ren, on=["CountryCode", "CountryName", "Year"], how="outer")
    df = df.merge(trust, on=["CountryCode", "CountryName", "Year"], how="outer")
    df.sort_values(by=["CountryCode", "Year"], inplace=True)

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"OECD ESG dataset saved to {save_path}")
    else:
        print("OECD ESG dataset ready (not saved)")

    return df

if __name__ == "__main__":
    df = download_all_oecd_esg(start_year=2015)
    print(df.head())
    print(f"\nTotal records: {len(df)}")
