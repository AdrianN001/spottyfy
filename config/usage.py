import os
import requests


def fetch_usage_data_from_scrape() -> dict:
    
    API_TOKEN = os.environ["SCRAPE_API_TOKEN"]

    res = requests.get(
            f"https://api.scrape.do/info?token={API_TOKEN}"
            )

    return res.json()
