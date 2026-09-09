# provision_user.py
import os
import requests
from dotenv import load_dotenv
from role_mapping import ROLE_TO_GROUPS
from audit import log_action

load_dotenv()

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")

headers = {
    "Authorization": f"SSWS {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def create_user(first_name, last_name, email):
    payload = {
        "profile": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "login": email
        }
    }
    response = requests.post(
        f"{ORG_URL}/api/v1/users?activate=false",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()


def assign_to_group(user_id, group_id):
    response = requests.put(
        f"{ORG_URL}/api/v1/groups/{group_id}/users/{user_id}",
        headers=headers
    )
    response.raise_for_status()


def provision_user(first_name, last_name, email, role):
    if role not in ROLE_TO_GROUPS:
        raise ValueError(f"Unknown role: {role}")

    try:
        user = create_user(first_name, last_name, email)
    except requests.exceptions.HTTPError as e:
        print(f"FAILED to create user: {e}")
        log_action("CREATE", user_id=None, user_email=email, detail=f"Role: {role} — creation failed", status="FAILURE")
        return None

    user_id = user["id"]
    print(f"Created user: {user_id} — {user['status']}")
    log_action("CREATE", user_id=user_id, user_email=email, detail=f"Role: {role}")

    for group_id in ROLE_TO_GROUPS[role]:
        try:
            assign_to_group(user_id, group_id)
            print(f"  Assigned to group: {group_id}")
            log_action("GROUP_ASSIGN", user_id=user_id, user_email=email, detail=f"Group: {group_id}")
        except requests.exceptions.HTTPError as e:
            print(f"  FAILED to assign group {group_id}: {e}")
            log_action("GROUP_ASSIGN", user_id=user_id, user_email=email, detail=f"Group: {group_id}", status="FAILURE")

    print(f"Provisioning complete for {email} as {role}")
    return user_id


if __name__ == "__main__":
    provision_user(
        first_name="Test",
        last_name="Auditor",
        email="test.auditor@example.com",
        role="Standard Employee"
    )