import requests
import pandas as pd
import time
from google.colab import drive

# 🔐 Replace this with your real API key
API_KEY = 'your_rentcast_api_key_here'

# 📍 Target ZIP code
ZIP_CODE = '32827'
STATE = 'FL'

# 📦 API details
BASE_URL = 'https://api.rentcast.io/v1/properties'
HEADERS = {
    'Accept': 'application/json',
    'X-Api-Key': API_KEY
}

# 📊 Setup
LIMIT = 500
MAX_REQUESTS = 50  # Prevent using all your quota at once
all_properties = []

print(f"🚀 Starting scrape for ZIP {ZIP_CODE}...")

# 🔁 Paginate through results using offset
for i in range(MAX_REQUESTS):
    offset = i * LIMIT
    print(f"Fetching records {offset + 1} to {offset + LIMIT}...")

    params = {
        'zipCode': ZIP_CODE,
        'state': STATE,
        'limit': LIMIT,
        'offset': offset
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        batch = response.json()
        if not batch:
            print("No more data returned by API.")
            break
        all_properties.extend(batch)
    else:
        print(f"❌ Failed at offset {offset}: {response.status_code}")
        break

    time.sleep(1)  # Respect API rate limits

# 🧼 Convert to DataFrame and drop duplicates
df = pd.DataFrame(all_properties)
df.drop_duplicates(subset='id', inplace=True)
print(f"\n✅ Collected {len(df)} unique properties for ZIP {ZIP_CODE}")

# 💾 Save locally
local_path = f"rentcast_32827_properties.csv"
df.to_csv(local_path, index=False)
print(f"📁 File saved locally as {local_path}")

# ☁️ Mount Google Drive and save there
drive.mount('/content/drive')
drive_path = f"/content/drive/MyDrive/rentcast_32827_properties.csv"
df.to_csv(drive_path, index=False)
print(f"✅ File also saved to your Google Drive: {drive_path}")
