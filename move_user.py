# move_user.py
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
    "Accept": "application/json"
}


def remove_from_group(user_id, group_id):
    response = requests.delete(
        f"{ORG_URL}/api/v1/groups/{group_id}/users/{user_id}",
        headers=headers
    )
    response.raise_for_status()


def assign_to_group(user_id, group_id):
    response = requests.put(
        f"{ORG_URL}/api/v1/groups/{group_id}/users/{user_id}",
        headers=headers
    )
    response.raise_for_status()


def move_user(user_id, user_email, old_role, new_role):
    if old_role not in ROLE_TO_GROUPS or new_role not in ROLE_TO_GROUPS:
        raise ValueError("Unknown role provided")

    old_groups = set(ROLE_TO_GROUPS[old_role])
    new_groups = set(ROLE_TO_GROUPS[new_role])

    groups_to_remove = old_groups - new_groups
    groups_to_add = new_groups - old_groups

    for group_id in groups_to_remove:
        try:
            remove_from_group(user_id, group_id)
            print(f"  Removed from group: {group_id}")
            log_action("GROUP_REMOVE", user_id=user_id, user_email=user_email, detail=f"Group: {group_id}")
        except requests.exceptions.HTTPError as e:
            print(f"  FAILED to remove group {group_id}: {e}")
            log_action("GROUP_REMOVE", user_id=user_id, user_email=user_email, detail=f"Group: {group_id}", status="FAILURE")

    for group_id in groups_to_add:
        try:
            assign_to_group(user_id, group_id)
            print(f"  Assigned to group: {group_id}")
            log_action("GROUP_ASSIGN", user_id=user_id, user_email=user_email, detail=f"Group: {group_id}")
        except requests.exceptions.HTTPError as e:
            print(f"  FAILED to assign group {group_id}: {e}")
            log_action("GROUP_ASSIGN", user_id=user_id, user_email=user_email, detail=f"Group: {group_id}", status="FAILURE")

    log_action("ROLE_CHANGE", user_id=user_id, user_email=user_email, detail=f"{old_role} -> {new_role}")
    print(f"Role change complete: {old_role} -> {new_role}")


if __name__ == "__main__":
    move_user(
        user_id="00u17522ktwpQzoIj698",
        user_email="test.auditor@example.com",
        old_role="Standard Employee",
        new_role="Manager"
    )