# list_users.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")

headers = {
    "Authorization": f"SSWS {TOKEN}",
    "Accept": "application/json"
}

response = requests.get(f"{ORG_URL}/api/v1/users", headers=headers)
response.raise_for_status()

for user in response.json():
    print(f"{user['profile']['login']} — {user['status']}")