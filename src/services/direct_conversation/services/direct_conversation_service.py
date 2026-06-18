from common.exceptions.exceptions import ConflictException, NotFoundException
import time
from repository.direct_conversation_repository import (
    get_direct_conversation,
    create_direct_conversation,
    get_user_by_email,
    get_direct_conversations_for_user,
    get_direct_conversation_by_id
)


def start_direct_conversation(current_user_id, target_email):
    start1 = time.time()
    target_user = get_user_by_email(target_email)
    print("time for get user by email:", time.time() - start1)
    if not target_user:
        raise NotFoundException(message="User not found")

    target_user_id = target_user[0]
    if current_user_id == target_user_id:
        raise ConflictException(message="You cannot start a conversation with yourself")

    user_one_id = min(str(current_user_id), str(target_user_id))

    user_two_id = max(str(current_user_id), str(target_user_id))

    conversation = get_direct_conversation(user_one_id, user_two_id)

    if conversation:
        raise ConflictException(message="Conversation already exists")

    return create_direct_conversation(user_one_id, user_two_id)

def get_user_conversations(user_id):
    response = get_direct_conversations_for_user(user_id)

    if not response:
        raise NotFoundException(message="No conversations found")

    return response


def get_conversation_by_id(conversation_id):
    conversation = get_direct_conversation_by_id(conversation_id)

    if not conversation:
        raise NotFoundException("Conversation not found")

    return conversation