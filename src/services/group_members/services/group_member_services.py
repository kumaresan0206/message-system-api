from repository.group_member_repository import (
    add_user_to_group_conversation,
    get_group_conversation_members,
    get_user_group,
    get_user_role_in_group,
    promote_member_to_admin,
    delete_member_from_group,
)

from common.exceptions.exceptions import (
    NotFoundException,
    ValidationException,
    ConflictException,
)


def add_member_to_group(group_id, current_user_id, target_user_id):

    admin = get_user_role_in_group(group_id, current_user_id)

    if not admin:
        raise NotFoundException(message="You are not a admin of this group")

    existing_member = get_user_group(group_id, target_user_id)

    if existing_member:
        raise ValidationException(message="User is already a member")

    add_user_to_group_conversation(group_id, target_user_id)

    return True


def get_group_members(group_id, user_id):

    group = get_user_group(group_id, user_id)  # Check if user is already a member
    if not group:
        raise NotFoundException(message="User is not a member of the group")

    members = get_group_conversation_members(group_id)
    if not members:
        raise NotFoundException(message="No members found for this group")

    return members


def promote_member(group_id, current_user_id, target_user_id):

    admin_role = get_user_role_in_group(group_id, current_user_id)

    if not admin_role:
        raise NotFoundException("You are not a member of this group")

    if admin_role != "admin":
        raise ConflictException(message="You are not a admin of this group")

    target_role = get_user_role_in_group(group_id, target_user_id)

    if not target_role:
        raise NotFoundException(message="Target user is not a member of the group")

    if target_role == "admin":
        raise ValidationException(message="Target user is already an admin")

    response = promote_member_to_admin(group_id, target_user_id)
    return response


def remove_member(group_id, current_user_id, target_user_id):

    admin_role = get_user_role_in_group(group_id, current_user_id)

    if not admin_role:
        raise NotFoundException("You are not a member of this group")

    if admin_role != "admin":
        raise NotFoundException(message="You are not a admin of this group")

    target_role = get_user_role_in_group(group_id, target_user_id)

    if not target_role:
        raise NotFoundException(message="Target user is not a member of the group")

    delete_member_from_group(group_id, target_user_id)
    return True
