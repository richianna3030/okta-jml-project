# create_user.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")

headers = {
    "Authorization": f"SSWS {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "profile": {
        "firstName": "Test",
        "lastName": "Employee",
        "email": "test.employee@example.com",
        "login": "test.employee@example.com"
    }
}

response = requests.post(
    f"{ORG_URL}/api/v1/users?activate=false",
    headers=headers,
    json=payload
)
response.raise_for_status()

user = response.json()
print(f"Created user: {user['id']} — {user['status']}")