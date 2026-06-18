import json
import time
from common.logger.logger import log_info, log_error
from services.direct_conversation_service import (
    start_direct_conversation,
    get_user_conversations,
    get_conversation_by_id,
)
from repository.direct_conversation_repository import get_user_by_cognito_sub
from common.response.response import success_response, error_response
from common.exceptions.exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)


def lambda_handler(event, context):
    print(json.dumps(event))

    try:
        log_info("Received event: {}".format(json.dumps(event)))
        method = event["httpMethod"]
        path = event["resource"]

        user_sub = event["requestContext"]["authorizer"]["claims"]["sub"]

        current_user = get_user_by_cognito_sub(user_sub)

        if not current_user:
            log_error("Current user not found for sub: {}".format(user_sub))
            raise NotFoundException("Current user not found")

        # CREATE CONVERSATION
        if method == "POST":
            log_info("Starting direct conversation for user_id: {}".format(current_user[0]))
            body = json.loads(event["body"])

            target_email = body.get("email")

            if not target_email:
                log_error("Email is required")
                raise ValidationException("Email is required")

            conversation = start_direct_conversation(current_user[0], target_email)

            log_info("Direct conversation started for user_id: {}".format(current_user[0]))

            return success_response(
                message="Conversation created successfully",
                data={"conversation_id": str(conversation)},
                status_code=201,
            )

        # GET CONVERSATIONS
        elif method == "GET" and path == "/api/v1/direct/conversations":
            log_info("Getting conversations for user_id: {}".format(current_user[0]))
            conversations = get_user_conversations(current_user[0])

            serialized = []

            for convo in conversations:
                serialized.append(
                    {
                        "id": str(convo[0]),
                        "user1_id": str(convo[1]),
                        "user2_id": str(convo[2]),
                        "created_at": convo[3].isoformat(),
                    }
                )

            log_info("Conversations retrieved for user_id: {}".format(current_user[0]))

            return success_response(
                message="Conversations retrieved successfully", data=serialized
            )

        elif method == "GET" and path == "/api/v1/direct/conversations/{dm_id}":
            dm_id = event["pathParameters"]["dm_id"]
            conversation = get_conversation_by_id(dm_id)

            log_info("Conversation retrieved for user_id: {}".format(current_user[0]))

            return success_response(
                message="Conversation retrieved successfully",
                data={
                    "id": str(conversation[0]),
                    "user1_id": str(conversation[1]),
                    "user2_id": str(conversation[2]),
                    "created_at": conversation[3].isoformat(),
                },
            )

        return error_response(message="Method not allowed", status_code=405)

    except ValidationException as e:
        return error_response(message=str(e), status_code=400)

    except NotFoundException as e:
        return error_response(message=str(e), status_code=404)

    except ConflictException as e:
        return error_response(message=str(e), status_code=409)

    except Exception as e:
        log_error("Unexpected error occurred: {}".format(str(e)))
        return error_response(message="Internal server error", status_code=500)
