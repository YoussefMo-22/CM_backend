# in a new file: coptic_bot/db_to_json.py
import psycopg2
import json
def test_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="coptic_museum",
            user="postgres",
            password="ym2205@postgresql"
        )
        print("✅ Connected to the database successfully.")
        conn.close()
    except Exception as e:
        print("❌ Failed to connect to the database.")
        print(e)

import requests
import json
import os

import requests
import json

def export_artifacts_from_db():
    import os

    SHARED_TOKEN = os.environ.get("DJANGO_SHARED_SECRET")

    HEADERS = {
        "X-API-Token": SHARED_TOKEN
    }
    print("🔄 Syncing from Django backend...")

    base_url = "http://127.0.0.1:8000/api"  # Update if using a different port or domain

    endpoints = {
        "artifacts": f"{base_url}/artifacts/",
        "events": f"{base_url}/events/",
        "programs": f"{base_url}/programs/",
        "models3d": f"{base_url}/3d-models/",
    }

    all_data = {}

    for key, url in endpoints.items():
        try:
            print(f"📦 Fetching {key}...")
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            all_data[key] = response.json()
        except Exception as e:
            print(f"❌ Error fetching {key}: {e}")
            all_data[key] = []

    # Write all combined data to a JSON file
    with open("data/exported_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("✅ Sync complete. Data saved to 'data/exported_data.json'")



if __name__ == "__main__":
    test_connection()