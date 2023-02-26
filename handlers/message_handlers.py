from aiogram import types, Dispatcher, types

from middleware.auth_middleware.authentication_middleware import registration_required, current_room_required

from db.models.Message import Message 
from db.models.Connection import Connection

from middleware.message_middleware.message_sender import MessageSender
from middleware.message_middleware.message_parser import MessageParser

@registration_required
@current_room_required
async def send_message_handler(message: types.Message, room_id: str, user=None):
    """
    This handler sends user's message to all the users that are currently in the same room as the user and saves them in the database. 
    @command None 
    """
    connected_users = Connection.get_users_connected_to_room(room_id) 

    Message.create_message(
        sender_id=message.chat.id,
        room_id=room_id,
        message_text=message.text
    )

    await MessageSender.send_message_to_chats(
        chat_id_list=connected_users, 
        message_text=MessageParser.create_chat_message(message.text, '' if user is None else user.username)
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_message_handler)
        