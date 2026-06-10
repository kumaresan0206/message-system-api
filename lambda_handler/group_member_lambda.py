import json

from repository.group_member_repository import get_user_by_cognito_sub

from services.group_member_services import add_member_to_group, get_group_members, promote_member, remove_member

from utils.responses import success_response, error_response

from exceptions.exceptions import (
    ValidationException,
    NotFoundException,
    UnauthorizedException,
    ConflictException,
)

from utils.logger import log_info, log_error


def lambda_handler(event, context):

    try:
        method = event["httpMethod"]

        user_sub = event["requestContext"]["authorizer"]["claims"]["sub"]

        current_user = get_user_by_cognito_sub(user_sub)

        if not current_user:
            raise NotFoundException("Current user not found")

        group_id = event["pathParameters"]["group_id"]

        # ADD MEMBER
        if method == "POST":
            body = json.loads(event["body"])

            target_user_id = body.get("user_id")

            if not target_user_id:
                raise ValidationException("User id is required")

            add_member_to_group(group_id, current_user[0], target_user_id)

            return success_response(
                message="Member added successfully", data=None, status_code=201
            )

        # GET MEMBERS
        elif method == "GET":
            members = get_group_members(group_id, current_user[0])

            serialized_members = []

            for member in members:
                serialized_members.append(
                    {
                        "membership_id": str(member[0]),
                        "group_id": str(member[1]),
                        "user_id": str(member[2]),
                        "role": member[3],
                    }
                )

            return success_response(
                message="Group members retrieved successfully",
                data=serialized_members,
                status_code=200,
            )

        elif method == "PATCH":

            target_user_id = event["pathParameters"]["user_id"]

            if not target_user_id:
                raise ValidationException("User id is required")

            response = promote_member(group_id, current_user[0], target_user_id)

            result = [
                    {
                        "membership_id": str(response[0]),
                        "group_id": str(response[1]),
                        "user_id": str(response[2]),
                        "role": response[3],
                    }
            ]

            return success_response(
                message="Member promoted successfully", data=result, status_code=200
            )

        elif method == "DELETE":

            target_user_id = event["pathParameters"]["user_id"]

            if not target_user_id:
                raise ValidationException("User id is required")

            remove_member(group_id, current_user[0], target_user_id)

            return success_response(
                message="Member deleted successfully", data=None, status_code=200
            )

        return error_response(message="Method not allowed", status_code=405)

    except ValidationException as e:
        return error_response(message=str(e), status_code=400)

    except NotFoundException as e:
        return error_response(message=str(e), status_code=404)

    except UnauthorizedException as e:
        return error_response(message=str(e), status_code=403)

    except ConflictException as e:
        return error_response(message=str(e), status_code=409)

    except Exception as e:
        log_error("Error while processing group member request", data=str(e))

        return error_response(message="Internal server error", status_code=500)
