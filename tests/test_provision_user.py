# tests/test_provision_user.py
from unittest.mock import patch, MagicMock
import provision_user


@patch("provision_user.requests.post")
def test_create_user_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "00u_fake_id", "status": "STAGED"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = provision_user.create_user("Test", "User", "test@example.com")

    assert result["id"] == "00u_fake_id"
    assert result["status"] == "STAGED"
    mock_post.assert_called_once()


@patch("provision_user.requests.put")
@patch("provision_user.requests.post")
@patch("provision_user.log_action")
def test_provision_user_logs_group_assign_failure(mock_log, mock_post, mock_put):
    mock_create_response = MagicMock()
    mock_create_response.json.return_value = {"id": "00u_fake_id", "status": "STAGED"}
    mock_create_response.raise_for_status.return_value = None
    mock_post.return_value = mock_create_response

    mock_put.side_effect = provision_user.requests.exceptions.HTTPError("Group assign failed")

    provision_user.provision_user(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        role="Standard Employee"
    )

    failure_calls = [
        call for call in mock_log.call_args_list
        if call.kwargs.get("status") == "FAILURE"
    ]
    assert len(failure_calls) == 1
    
@patch("provision_user.requests.post")
@patch("provision_user.log_action")
def test_provision_user_handles_create_failure(mock_log, mock_post):
    mock_post.side_effect = provision_user.requests.exceptions.HTTPError("Creation failed")

    result = provision_user.provision_user(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        role="Standard Employee"
    )

    assert result is None
    mock_log.assert_called_once()
    assert mock_log.call_args.kwargs["status"] == "FAILURE"