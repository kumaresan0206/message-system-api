from repository.group_message_repository import (
    send_message_to_group,
    get_group_member,
    get_group,
    get_group_messages,
    edit_group_message,
    delete_group_message,
    get_message_by_id,
    group_message_mark_as_read
)

from exceptions.exceptions import NotFoundException, ValidationException, UnauthorizedException


def send_message_service(group_id, sender_id, message):

    if not message.strip():
        raise ValidationException(message="Message cannot be empty")

    group = get_group(group_id)

    if not group:
        raise NotFoundException("Group not found")

    sender = get_group_member(group_id, sender_id)

    if not sender:
        raise NotFoundException(message="You are not a member of this group")

    return send_message_to_group(group_id, sender_id, message)


def list_group_messages(group_id, user_id):

    group = get_group(group_id)

    if not group:
        raise NotFoundException(message="Group not found")

    member = get_group_member(group_id, user_id)

    if not member:
        raise UnauthorizedException(message="You are not a member of this group")

    messages = get_group_messages(group_id)

    if not messages:
        raise NotFoundException(message="No messages found for this group")

    return messages


def edit_message(group_id, message_id, user_id, new_message_text):

    group = get_group(group_id)
    if not group:
        raise NotFoundException(message="Group not found")
    
    member = get_group_member(group_id, user_id)
    if not member:
        raise UnauthorizedException(message="You are not a member of this group")

    message = get_message_by_id(message_id)

    if not message:
        raise NotFoundException(message="Message not found")

    if message[2] != user_id:
        raise UnauthorizedException(message="You are not authorized to edit this message")

    return edit_group_message(message_id, user_id, new_message_text)

def delete_group_message_service(group_id, message_id, user_id):

    group = get_group(group_id)
    if not group:
        raise NotFoundException(message="Group not found")
    
    member = get_group_member(group_id, user_id)
    if not member:
        raise UnauthorizedException(message="You are not a member of this group")

    message = get_message_by_id(message_id)

    if not message:
        raise NotFoundException(message="Message not found")

    if message[2] != user_id:
        raise UnauthorizedException(message="You are not authorized to delete this message")

    return delete_group_message(message_id, user_id)

def mark_message_as_read(group_id, message_id, user_id):

    group = get_group(group_id)
    if not group:
        raise NotFoundException("Group not found")
    
    member = get_group_member(group_id, user_id)
    if not member:
        raise UnauthorizedException("You are not a member of this group")

    message = get_message_by_id(message_id)

    if not message:
        raise NotFoundException("Message not found")

    if str(message[1]) != str(group_id):
        raise ValidationException("Message does not belong to this group")

    return group_message_mark_as_read(message_id, user_id)