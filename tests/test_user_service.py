from unittest.mock import patch

from services.users.services.user_service import (
    register_user,
    authenticate_user
)


@patch("services.users.services.user_service.create_user")
@patch("services.users.services.user_service.cognito_client")
def test_register_user(mock_cognito, mock_create_user):

    mock_cognito.sign_up.return_value = {
        "UserSub": "123"
    }

    response = register_user(
        username="kumar",
        password="Password@123",
        email="kumar@gmail.com"
    )

    assert response["UserSub"] == "123"

    mock_create_user.assert_called_once()


@patch("services.users.services.user_service.cognito_client")
def test_authenticate_user(mock_cognito):

    mock_cognito.initiate_auth.return_value = {
        "AuthenticationResult": {
            "AccessToken": "access",
            "IdToken": "id",
            "RefreshToken": "refresh"
        }
    }

    response = authenticate_user(
        "kumar@gmail.com",
        "Password@123"
    )

    assert response["access_token"] == "access"