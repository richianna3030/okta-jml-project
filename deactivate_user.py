# deactivate_user.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")
USER_ID = "insert_user_id_here"

headers = {
    "Authorization": f"SSWS {TOKEN}",
    "Accept": "application/json"
}

response = requests.post(
    f"{ORG_URL}/api/v1/users/{USER_ID}/lifecycle/deactivate",
    headers=headers
)
response.raise_for_status()

print(f"User {USER_ID} deactivated.")
