import boto3
from botocore.exceptions import ClientError
from core.config import USER_POOL_ID, CLIENT_ID, AWS_REGION
from exceptions.exceptions import (
    InternalServerErrorException,
    UnauthorizedException,
    ValidationException,
    ForbiddenException,
)
from core.logger import log_info, log_error
from repository.user_repository import create_user

cognito_client = boto3.client("cognito-idp", region_name=AWS_REGION)


def register_user(username, password, email):
    try:
        log_info("Attempting to register user", username=username)
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "name", "Value": username},
            ],
        )
        create_user(response["UserSub"], username, email)
        log_info("User registration successful", username=username)
        return response

    except cognito_client.exceptions.UsernameExistsException:
        log_error("User already exists", username=username)
        raise ForbiddenException(message="User already exists")

    except cognito_client.exceptions.InvalidPasswordException:
        log_error("Invalid password", username=username)
        raise ValidationException(
            message="Password must contain uppercase, lowercase, number and special character"
        )

    except cognito_client.exceptions.InvalidParameterException as e:
        log_error("Invalid parameters", username=username, error=str(e))
        raise ValidationException(message=str(e))

    except ClientError as e:
        log_error(
            "Client error during user registration", username=username, error=str(e)
        )
        raise InternalServerErrorException(
            message="An error occurred during registration: " + str(e)
        )


def confirm_user_registration(email, confirmation_code):
    try:
        log_info("Attempting to confirm user registration", username=email)
        response = cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID, Username=email, ConfirmationCode=confirmation_code
        )
        log_info("User registration confirmed", username=email)
        return response

    except cognito_client.exceptions.CodeMismatchException:
        log_error("Invalid confirmation code", username=email)
        raise ValidationException(message="Invalid confirmation code")

    except cognito_client.exceptions.ExpiredCodeException:
        log_error("Confirmation code expired", username=email)
        raise ValidationException(message="Confirmation code has expired")

    except ClientError as e:
        log_error("Client error during confirmation", username=email, error=str(e))
        raise InternalServerErrorException(
            message="An error occurred during confirmation: " + str(e)
        )


def authenticate_user(email, password):
    try:
        log_info("Attempting to authenticate user", username=email)
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        log_info("User authentication successful", username=email)
        tokens = response["AuthenticationResult"]
        return {
            "access_token": tokens["AccessToken"],
            "id_token": tokens["IdToken"],
            "refresh_token": tokens["RefreshToken"],
        }

    except cognito_client.exceptions.NotAuthorizedException:
        log_error("Incorrect username or password", username=email)
        raise ValidationException(message="Incorrect username or password")

    except cognito_client.exceptions.UserNotConfirmedException:
        log_error("User not confirmed", username=email)
        raise ForbiddenException(
            message="User is not confirmed. Please confirm your registration first."
        )

    except ClientError as e:
        log_error("Client error during authentication", username=email, error=str(e))
        raise InternalServerErrorException(
            message="An error occurred during authentication: " + str(e)
        )


def show_user_details(access_token):
    try:
        log_info("Attempting to retrieve user details")

        response = cognito_client.get_user(AccessToken=access_token)

        user_attributes = {
            attr["Name"]: attr["Value"] for attr in response["UserAttributes"]
        }

        log_info("User details retrieved successfully", username=response["Username"])

        return {
            "usersub": response["Username"],
            "username": user_attributes.get("name"),
            "email": user_attributes.get("email"),
        }

    except cognito_client.exceptions.NotAuthorizedException:
        log_error("Invalid or expired access token")

        raise UnauthorizedException(message="Invalid or expired access token")

    except ClientError as e:
        log_error("Client error during user details retrieval", error=str(e))

        raise InternalServerErrorException(message="An error occurred while retrieving user details")
