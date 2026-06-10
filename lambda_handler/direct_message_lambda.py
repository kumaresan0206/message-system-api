import json

from core.logger import log_info, log_error
from repository.direct_messages_repository import get_user_by_cognito_sub
from services.direct_message_services import send_direct_message, get_direct_messages, edit_message, delete_conversation_message
from utils.response import success_response, error_response
from exceptions.exceptions import ValidationException, NotFoundException, ForbiddenException, UnauthorizedException


def lambda_handler(event, context):

    try:
        method = event["httpMethod"]

        user_sub = event["requestContext"]["authorizer"]["claims"]["sub"]

        current_user = get_user_by_cognito_sub(user_sub)

        if not current_user:
            raise NotFoundException(message="Current user not found")

        # SEND MESSAGE
        if method == "POST":
            body = json.loads(event["body"])

            content = body.get("message")
            conversation_id = event["pathParameters"]["dm_id"]

            if not content:
                raise ValidationException(message="Content is required")

            message_id = send_direct_message(conversation_id, current_user[0], content)

            return success_response(
                message="Message sent successfully",
                data={"message_id": str(message_id)},
                status_code=201,
            )

        # GET MESSAGES
        elif method == "GET":

            conversation_id = event["pathParameters"]["dm_id"]
            messages = get_direct_messages(conversation_id, current_user[0])

            serialized = []

            for message in messages:
                serialized.append(
                    {
                        "id": str(message[0]),
                        "conversation_id": str(message[1]),
                        "sender_id": str(message[2]),
                        "content": message[3],
                        "created_at": (message[4].isoformat()),
                    }
                )

            return success_response(
                message="Messages retrieved successfully", data=serialized
            )
        
        #EDIT MESSAGE
        elif method == "PATCH":

            body = json.loads(event["body"])

            new_message_text = body.get("message")

            if not new_message_text:
                raise ValidationException(message="Content is required")

            message_id = event["pathParameters"]["message_id"]

            edit_message(
                message_id,
                current_user[0],
                new_message_text
            )

            return success_response(
                message="Message updated successfully",
                data=None,
                status_code=200
            )

        elif method == "DELETE":

            message_id = event["pathParameters"]["message_id"]

            delete_conversation_message(
                message_id,
                current_user[0]
            )

            return success_response(
                message="Message deleted successfully",
                data=None,
                status_code=200
            )

        return error_response(message="Method not allowed", status_code=405)

    except ValidationException as e:
        return error_response(message=str(e), status_code=400)

    except NotFoundException as e:
        return error_response(message=str(e), status_code=404)

    except ForbiddenException as e:
        return error_response(message=str(e), status_code=403)

    except UnauthorizedException as e:
        return error_response(message=str(e), status_code=401)

    except Exception as e:
        print(e)

        return error_response(message="Internal server error", status_code=500)
