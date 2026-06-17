import json

from services.users.services.user_service import (
    register_user,
    confirm_user_registration,
    authenticate_user,
    show_user_details
)

from common.response.response import error_response, success_response

def lambda_handler(event, context):

    try:
        print(event)

        path = event["resource"]
        method = event["httpMethod"]

        body = {}

        if method in ["POST", "PUT", "PATCH"]:
            body = json.loads(event["body"])

        if path == "/api/v1/auth/users" and method == "POST":

            result = register_user(
                username=body["username"],
                email=body["email"],
                password=body["password"]
            )

            

            return success_response(message= "User registered successfully and Confirmation code sent to the mail.")

        elif path == "/api/v1/auth/confirm" and method == "POST":

            result = confirm_user_registration(
                email=body["email"],
                confirmation_code=body["code"]
            )

            return success_response(message= "Account Verified Successfully")

        elif path == "/api/v1/auth/login" and method == "POST":

            result = authenticate_user(
                email=body["email"],
                password=body["password"]
            )

            return success_response(message= "Login Successfully", data=result)

        elif path == "/api/v1/auth/me" and method == "GET":

            authorization = event["headers"]["Authorization"]

            access_token = authorization.replace(
                "Bearer ",
                ""
            )

            result = show_user_details(
                access_token=access_token
            )

            return success_response(
                message="User details retrieved",
                data=result
            )

        return error_response(
        message="Route not found"
    )

    except Exception as e:

        return error_response(
        message=str(e)
    )