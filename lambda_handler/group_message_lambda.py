import json

from repository.group_message_repository import get_user_by_cognito_sub
from services.group_message_service import (
    send_message_service, 
    list_group_messages, 
    edit_message, 
    delete_group_message_service, 
    mark_message_as_read
)
from utils.response import success_response, error_response
from exceptions.exceptions import (
    ValidationException,
    NotFoundException,
    UnauthorizedException,
    ConflictException,
)
from utils.logger import log_error


def lambda_handler(event, context):

    try:
        method = event["httpMethod"]

        user_sub = event["requestContext"]["authorizer"]["claims"]["sub"]

        current_user = get_user_by_cognito_sub(user_sub)

        if not current_user:
            raise NotFoundException("Current user not found")

        group_id = event["pathParameters"]["group_id"]

        # SEND MESSAGE
        if method == "POST":

            path = event["path"]

            # MARK AS READ
            if path.endswith("/read"):

                message_id = (event["pathParameters"]["message_id"])

                response = mark_message_as_read(
                    group_id,
                    message_id,
                    current_user[0]
                )

                if not response:
                    return success_response(message="Message Already read.")

                result = {
                    "message_id": str(response[1]),
                    "user_id": str(response[2]),
                    "read_at": (
                        response[3].isoformat()
                        if response[3]
                        else None
                    )
                }

                return success_response(
                    message="Message marked as read",
                    data=result,
                    status_code=200
                )
            else:
                body = json.loads(event["body"])

                message = body.get("message")

                if not message:
                    raise ValidationException(message="Message is required")

                response = send_message_service(group_id, current_user[0], message)

                return success_response(
                    message="Message sent successfully",
                    data={
                        "message_id": str(response[0]),
                        "group_id": str(response[1]),
                        "sender_id": str(response[2]),
                        "message": response[3],
                        "created_at": (response[6].isoformat() if response[6] else None),
                    }
                )

        # GET MESSAGES
        elif method == "GET":
            messages = list_group_messages(group_id, current_user[0])

            result = []

            for msg in messages:
                result.append(
                    {
                        "message_id": str(msg[0]),
                        "group_id": str(msg[1]),
                        "sender_id": str(msg[2]),
                        "message": msg[3],
                        "created_at": (msg[6].isoformat() if msg[6] else None),
                        "is_edited": msg[4],
                        "edited_at": (msg[5].isoformat() if msg[5] else None),
                    }
                )

            return success_response(
                message="Messages retrieved successfully", data=result, status_code=200
            )

        elif method == "PATCH":
            body = json.loads(event["body"])

            group_id = event["pathParameters"]["group_id"]

            message_id = event["pathParameters"]["message_id"]

            new_message = body.get("message")

            if not new_message:
                raise ValidationException(message="Message is required")

            response = edit_message(group_id, message_id, current_user[0], new_message)

            result = {
                "message_id": str(response[0]),
                "group_id": str(response[1]),
                "sender_id": str(response[2]),
                "message": response[3],
                "created_at": (response[6].isoformat() if response[6] else None),
                "is_edited": response[4],
                "edited_at": (response[5].isoformat() if response[5] else None),
            }

            return success_response(
                message="Message updated successfully", data=result, status_code=200
            )

        elif method == "DELETE":

            group_id = event["pathParameters"]["group_id"]
            message_id = event["pathParameters"]["message_id"]

            response = delete_group_message_service(group_id, message_id, current_user[0])

            result = {
                "message_id": str(response[0]),
                "group_id": str(response[1]),
                "sender_id": str(response[2]),
                "message": response[3],
                "created_at": (response[6].isoformat() if response[6] else None),
            }

            return success_response(
                message="Message deleted successfully", data=result, status_code=200
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
        log_error("Error while processing group message request", data=str(e))

        return error_response(message="Internal server error", status_code=500)
