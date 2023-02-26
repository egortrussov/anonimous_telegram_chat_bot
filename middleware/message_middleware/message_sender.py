from aiogram import types

from bot.bot import bot

from db.models.Connection import Connection

class MessageSender:
    
    def __init__(self):
        pass 
    
    @staticmethod
    async def send_message_to_chat(message: types.Message, message_text: str) -> None:
        """
        Sends message to chat associated with message object
        """
        await message.answer(message_text, parse_mode='markdown') 
    
    @staticmethod
    async def send_messages_to_chat(message: types.Message, messages: list[str]) -> None:
        """
        Sends messages to chat specified in message object
        """
        for msg in messages:
            await MessageSender.send_message_to_chat(
                message=message,
                message_text=msg
            )
    
    @staticmethod 
    async def send_message_by_chat_id(chat_id: str, message_text: str) -> None:
        """
        Sends message to chat with chat_id
        """
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='markdown') 
    
    @staticmethod 
    async def send_message_to_chats(chat_id_list: list[str], message_text: str) -> None:
        """
        Sends message to chats with id in chat_id_list
        """
        for chat_id in chat_id_list:
            await MessageSender.send_message_by_chat_id(chat_id, message_text) 
    
    @staticmethod 
    async def send_message_to_chat_users(room_id: str, message_text: str) -> None:
        """
        Sends message to users that joined room with id room_id
        """
        room_connections = Connection.get_connection_list(
            room_id=room_id
        )

        chat_ids_list = list(map(lambda x : x.user_id, room_connections)) 

        await MessageSender.send_message_to_chats(
            chat_id_list=chat_ids_list,
            message_text=message_text
        )