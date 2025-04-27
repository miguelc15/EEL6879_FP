import requests
import pandas as pd
import time
#from colabcode import ColabCode

# 🔐 Replace this with your real API key
API_KEY = 'c39e0650e4f846498fc7799dbce11a0f'

# 📍 Target ZIP code
ZIP_CODE = '32835'
STATE = 'FL'

# 📦 API details
BASE_URL = 'https://api.rentcast.io/v1/listings/sale'
HEADERS = {
    'Accept': 'application/json',
    'X-Api-Key': API_KEY
}

# 📊 Setup
LIMIT = 500
MAX_REQUESTS = 10  # Prevent using all your quota at once
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

local_path = f"listings_32835_properties.csv"
df.to_csv(local_path, index=False)
print(f"📁 File saved locally as {local_path}")


