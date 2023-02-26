from aiogram import executor, types, Dispatcher
from sqlalchemy import or_

from bot.bot import bot

from db.db import create_session
from db.models.User import User

from middleware.message_middleware.message_parser import MessageParser
from middleware.message_middleware.message_sender import MessageSender
from middleware.message_middleware.check_message_params import are_all_params_present
from middleware.auth_middleware.authentication_middleware import check_if_user_exists,validate_username

async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    @command /start, /help
    """
    await MessageSender.send_message_to_chat(
        message=message, 
        message_text='Type /register username to register\n'
                        '/createroom room name to create a room\n'
                        '/switchroom room id to switch to a room\n'
                        '/joinedrooms to get a list of your joined rooms\n'
                        '/joinroom room id to join a room (you must first recieve a room id)\n'
                        '/leaveroom room id to leave a room. All your messages will be deleted'
    )

async def register_user(message: types.Message):
    """
    This handler registers a user, adds user data to the database
    @command /register <username>
    """
    COMMAND_PARAMS = ['username']

    session = create_session()
    
    message_data = MessageParser.parse_command_message_by_params(
        message=message.text,
        params=['username']
    )
    
    if not (await are_all_params_present(message_data, message, COMMAND_PARAMS)):
        return 
    
    if not validate_username(username):
        await MessageSender.send_message_to_chat(
            message=message,
            message_text='Invalid username'
        )
        return

    username = message_data.get('username')

    if check_if_user_exists(username=username, user_id=message.chat.id):
        await MessageSender.send_message_to_chat(message, 'Already registered')
        return 
    

    new_user = User(
        user_id=message.chat.id,
        username=username,
        current_room_id=None
    ) 

    session.add(new_user)
    
    session.commit() 

    await MessageSender.send_message_to_chat(message, 'Registered')
        

def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        send_welcome,
        commands=['start', 'help']
    ) 
    dp.register_message_handler(
        register_user,
        commands=['register']
    )