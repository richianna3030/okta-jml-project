# tests/test_move_user.py
from role_mapping import ROLE_TO_GROUPS


def test_standard_to_manager_only_adds():
    old_groups = set(ROLE_TO_GROUPS["Standard Employee"])
    new_groups = set(ROLE_TO_GROUPS["Manager"])

    groups_to_remove = old_groups - new_groups
    groups_to_add = new_groups - old_groups

    assert groups_to_remove == set()
    assert len(groups_to_add) == 1


def test_manager_to_standard_only_removes():
    old_groups = set(ROLE_TO_GROUPS["Manager"])
    new_groups = set(ROLE_TO_GROUPS["Standard Employee"])

    groups_to_remove = old_groups - new_groups
    groups_to_add = new_groups - old_groups

    assert len(groups_to_remove) == 1
    assert groups_to_add == set()


def test_manager_to_it_admin_swaps_groups():
    old_groups = set(ROLE_TO_GROUPS["Manager"])
    new_groups = set(ROLE_TO_GROUPS["IT Admin"])

    groups_to_remove = old_groups - new_groups
    groups_to_add = new_groups - old_groups

    assert len(groups_to_remove) == 1
    assert len(groups_to_add) == 1