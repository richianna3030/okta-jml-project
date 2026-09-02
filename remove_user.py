# remove_user.py
import os
import requests
from dotenv import load_dotenv
from audit import log_action

load_dotenv()

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")

headers = {
    "Authorization": f"SSWS {TOKEN}",
    "Accept": "application/json"
}


def get_user_groups(user_id):
    response = requests.get(
        f"{ORG_URL}/api/v1/users/{user_id}/groups",
        headers=headers
    )
    response.raise_for_status()
    return response.json()


def remove_from_group(user_id, group_id):
    response = requests.delete(
        f"{ORG_URL}/api/v1/groups/{group_id}/users/{user_id}",
        headers=headers
    )
    response.raise_for_status()


def deactivate_user(user_id):
    response = requests.post(
        f"{ORG_URL}/api/v1/users/{user_id}/lifecycle/deactivate",
        headers=headers
    )
    response.raise_for_status()


def remove_user(user_id, user_email):
    groups = get_user_groups(user_id)

    for group in groups:
        group_id = group["id"]
        group_name = group["profile"]["name"]

        if group_name == "Everyone":
            continue

        try:
            remove_from_group(user_id, group_id)
            print(f"  Removed from group: {group_name}")
            log_action("GROUP_REMOVE", user_id=user_id, user_email=user_email, detail=f"Group: {group_name}")
        except requests.exceptions.HTTPError as e:
            print(f"  FAILED to remove group {group_name}: {e}")
            log_action("GROUP_REMOVE", user_id=user_id, user_email=user_email, detail=f"Group: {group_name}", status="FAILURE")

    try:
        deactivate_user(user_id)
        print(f"User {user_id} deactivated.")
        log_action("DEACTIVATE", user_id=user_id, user_email=user_email, detail="User deactivated")
    except requests.exceptions.HTTPError as e:
        print(f"FAILED to deactivate user: {e}")
        log_action("DEACTIVATE", user_id=user_id, user_email=user_email, detail="Deactivation failed", status="FAILURE")


if __name__ == "__main__":
    remove_user(
        user_id="00u17522ktwpQzoIj698",
        user_email="test.auditor@example.com"
    )