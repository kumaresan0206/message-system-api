import json
from unittest.mock import patch

from services.users.handler import lambda_handler


@patch("services.users.handler.register_user")
def test_register_user(mock_register):

    mock_register.return_value = {}

    event = {
        "resource": "/api/v1/auth/users",
        "httpMethod": "POST",
        "body": json.dumps({
            "username": "kumar",
            "email": "kumar@gmail.com",
            "password": "Password@123"
        })
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 200


@patch("services.users.handler.confirm_user_registration")
def test_confirm_user(mock_confirm):

    mock_confirm.return_value = {}

    event = {
        "resource": "/api/v1/auth/confirm",
        "httpMethod": "POST",
        "body": json.dumps({
            "email": "kumar@gmail.com",
            "code": "123456"
        })
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 200


@patch("services.users.handler.authenticate_user")
def test_login(mock_authenticate):

    mock_authenticate.return_value = {
        "access_token": "access",
        "id_token": "id",
        "refresh_token": "refresh"
    }

    event = {
        "resource": "/api/v1/auth/login",
        "httpMethod": "POST",
        "body": json.dumps({
            "email": "kumar@gmail.com",
            "password": "Password@123"
        })
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 200


@patch("services.users.handler.show_user_details")
def test_get_user(mock_show_user):

    mock_show_user.return_value = {
        "usersub": "123",
        "username": "kumar",
        "email": "kumar@gmail.com"
    }

    event = {
        "resource": "/api/v1/auth/me",
        "httpMethod": "GET",
        "headers": {
            "Authorization": "Bearer token"
        }
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 200


def test_invalid_route():

    event = {
        "resource": "/invalid",
        "httpMethod": "GET"
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 400