from repository.group_conversation_repository import (
    create_group_conversation,
    get_group_conversation_by_group_and_creator,
    add_user_to_group_conversation,
    get_user_group,
    get_group_by_id,
    get_group_conversation_by_id,
    update_group_conversation,
    delete_group_conversation,
)
from common.exceptions.exceptions import (
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)


def create_group(group_name, description, creator_id, members=[]):

    existing_conversation = get_group_conversation_by_group_and_creator(
        group_name, creator_id
    )
    if existing_conversation:
        raise ConflictException(
            message="Group conversation with the same name already exists"
        )

    conversation = create_group_conversation(group_name, description, creator_id)

    add_user_to_group_conversation(conversation[0], creator_id, "admin")

    for member_id in members:
        add_user_to_group_conversation(conversation[0], member_id, "member")

    return conversation[0]


def get_user_groups(user_id):

    conversations = get_user_group(user_id)

    if not conversations:
        raise NotFoundException(message="No group conversations found")

    return conversations


def get_group(group_id, user_id):

    conversation = get_group_conversation_by_id(group_id)

    if not conversation:
        raise NotFoundException(message="Group conversation not found")

    group = get_group_by_id(group_id, user_id)

    if not group:
        raise UnauthorizedException(message="You're not a member of this group")

    return conversation


def update_group_conversation_service(
    group_id, user_id, new_group_name, new_description
):

    conversation = get_group_conversation_by_id(group_id)

    if not conversation:
        raise NotFoundException(message="Group conversation not found")

    group = get_group_by_id(group_id, user_id)

    if not group:
        raise UnauthorizedException(message="You're not a member of this group")

    update_conversation = update_group_conversation(
        group_id, user_id, new_group_name, new_description
    )

    if not update_conversation:
        raise UnauthorizedException(
            message="You are not authorized to update this group conversation"
        )

    return update_conversation


def delete_group_conversation_service(group_id, user_id):

    conversation = get_group_conversation_by_id(group_id)

    if not conversation:
        raise NotFoundException(message="Group conversation not found")

    group = get_group_by_id(group_id, user_id)

    if not group:
        raise UnauthorizedException(message="You're not a member of this group")

    delete_conversation = delete_group_conversation(group_id, user_id)

    if not delete_conversation:
        raise UnauthorizedException(
            message="You are not authorized to delete this group conversation"
        )

    return True
