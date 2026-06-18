from repository.direct_message_repository import (
    create_direct_message, 
    get_direct_conversation_by_id, 
    get_messages_by_conversation_id, 
    edit_direct_conversation_message,
    get_direct_conversation_by_message_id,
    delete_message
    )

from common.exceptions.exceptions import NotFoundException, UnauthorizedException, ForbiddenException

def send_direct_message(conversation_id, sender_id, content):

    conversation = get_direct_conversation_by_id(conversation_id)

    if not conversation:
        raise NotFoundException(message="Conversation not found")

    user1_id = conversation[1]
    user2_id = conversation[2]

    if sender_id != user1_id and sender_id != user2_id:
        raise ForbiddenException(message="You are not part of this conversation")

    return create_direct_message(conversation_id, sender_id, content)

def get_direct_messages(conversation_id, user_id):

    conversation = get_direct_conversation_by_id(conversation_id)

    if not conversation:
        raise NotFoundException(message="Conversation not found")

    if user_id != conversation[1] and user_id != conversation[2]:
        raise ForbiddenException(message="You are not part of this conversation")

    return get_messages_by_conversation_id(conversation_id)

def edit_message(message_id, user_id, new_message_text):

    message = get_direct_conversation_by_message_id(message_id)

    if not message:
        raise NotFoundException(message="Message not found")

    if message[2] != user_id:
        raise UnauthorizedException(message="You are not authorized to edit this message")

    return edit_direct_conversation_message(message_id, new_message_text)

def delete_conversation_message(message_id, user_id):

    message = get_direct_conversation_by_message_id(message_id)

    if not message:
        raise NotFoundException(message="Message not found")

    if message[2] != user_id:
        raise UnauthorizedException(message="You are not authorized to delete this message")

    return delete_message(message_id)

