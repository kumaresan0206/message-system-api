import json

from common.logger.logger import log_info, log_error
from repository.group_conversation_repository import get_user_by_cognito_sub
from services.group_conversation_services import (
    create_group,
    get_user_groups,
    get_group,
    update_group_conversation_service,
    delete_group_conversation_service,
)
from common.response.response import success_response, error_response
from common.exceptions.exceptions import (
    ValidationException,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
)


def lambda_handler(event, context):

    try:
        log_info("Received event: {}".format(json.dumps(event)))
        method = event["httpMethod"]

        user_sub = event["requestContext"]["authorizer"]["claims"]["sub"]

        current_user = get_user_by_cognito_sub(user_sub)

        if not current_user:
            raise NotFoundException(message="Current user not found")

        # CREATE GROUP
        if method == "POST":
            log_info(
                "Starting to create group conversation for user_id: {}".format(
                    current_user[0]
                )
            )
            body = json.loads(event["body"])

            group_name = body.get("name")

            members = body.get("members", [])
            description = body.get("description")

            if not group_name:
                raise ValidationException(message="Group name is required")

            group_id = create_group(
                creator_id=current_user[0],
                group_name=group_name,
                members=members,
                description=description,
            )

            log_info(
                "Group conversation created for user_id: {}".format(current_user[0])
            )

            return success_response(
                message="Group created successfully",
                data={"group_id": str(group_id)},
                status_code=201,
            )

        # GET MY GROUPS
        elif method == "GET":
            path_parameters = event.get("pathParameters")

            # GET /groups/{group_id}
            if path_parameters and path_parameters.get("group_id"):
                group_id = path_parameters["group_id"]

                log_info("Retrieving group for user_id: {}".format(current_user[0]))
                group = get_group(group_id, current_user[0])

                log_info("Group retrieved for user_id: {}".format(current_user[0]))

                return success_response(
                    message="Group retrieved successfully",
                    data={
                        "id": str(group[0]),
                        "name": group[1],
                        "created_by": str(group[2]),
                        "created_at": (group[3].isoformat() if group[3] else None),
                    },
                )

            # GET /groups
            else:
                log_info(
                    "Retrieving user groups for user_id: {}".format(current_user[0])
                )
                groups = get_user_groups(current_user[0])

                serialized = []

                for group in groups:
                    serialized.append(
                        {
                            "id": str(group[0]),
                            "name": group[1],
                            "created_by": str(group[2]),
                            "created_at": (group[3].isoformat() if group[3] else None),
                        }
                    )

                log_info(
                    "User groups retrieved for user_id: {}".format(current_user[0])
                )

                return success_response(
                    message="Groups retrieved successfully", data=serialized
                )
        elif method == "PATCH":
            log_info(
                "Starting to update group conversation for user_id: {}".format(
                    current_user[0]
                )
            )
            group_id = event["pathParameters"]["group_id"]

            body = json.loads(event["body"])

            new_group_name = body.get("group_name")

            new_description = body.get("description")

            if not new_group_name:
                raise ValidationException(message="Group name is required")

            updated_group = update_group_conversation_service(
                group_id, current_user[0], new_group_name, new_description
            )

            log_info(
                "Group conversation updated for user_id: {}".format(current_user[0])
            )

            return success_response(
                message="Group updated successfully",
                data={
                    "group_id": str(updated_group[0]),
                    "group_name": updated_group[1],
                    "description": updated_group[2],
                },
                status_code=200,
            )

        elif method == "DELETE":
            log_info(
                "Starting to delete group conversation for user_id: {}".format(
                    current_user[0]
                )
            )

            path_parameters = event.get("pathParameters")

            group_id = path_parameters["group_id"]

            delete_group_conversation_service(group_id, current_user[0])

            log_info(
                "Group conversation deleted for user_id: {}".format(current_user[0])
            )

            return success_response(message="Group deleted successfully", data=None)

        return error_response(message="Method not allowed", status_code=405)

    except ValidationException as e:
        return error_response(message=str(e), status_code=400)

    except NotFoundException as e:
        return error_response(message=str(e), status_code=404)

    except ConflictException as e:
        return error_response(message=str(e), status_code=409)

    except UnauthorizedException as e:
        return error_response(message=str(e), status_code=403)

    except Exception as e:
        log_error("Error while processing group request", data=str(e))

        return error_response(message="Internal server error", status_code=500)
