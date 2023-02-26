from aiogram import types, Dispatcher
from datetime import datetime

from db.db import create_session
from db.models.Room import Room
from db.models.User import User
from db.models.Connection import Connection
from db.models.Message import Message

from middleware.auth_middleware.authentication_middleware import registration_required
from middleware.message_middleware.message_parser import MessageParser 
from middleware.message_middleware.message_sender import MessageSender
from middleware.message_middleware.check_message_params import are_all_params_present
from middleware.auth_middleware.generate_id import generate_id

@registration_required
async def create_room(message: types.Message, user = None):   
    """
    This handler creates a chat room. Authentication is required 
    @command /create_room <room_name>
    """     
    COMMAND_PARAMS = ['room_name']

    parsed_message = MessageParser.parse_command_message_by_params(
        message=message.text,
        params=COMMAND_PARAMS
    ) 
    
    if not (await are_all_params_present(parsed_message, message, COMMAND_PARAMS)):
        return
    
    room_name = parsed_message.get('room_name')
    
    created_room_id = Room.create_room(room_name)

    Connection.create_connection(
        user_id= user.user_id,
        room_id=created_room_id
    )

    await MessageSender.send_message_to_chat(
        message=message,
        message_text=f'Room with id ```{ created_room_id }``` was created'
    ) 

@registration_required
async def join_room(message: types.Message, user = None):
    """
    This handler joins the user to a room Authentication is required 
    @command /join_room <room_id>
    """   
    COMMAND_PARAMS = ['room_id']

    parsed_message = MessageParser.parse_command_message_by_params(
        message=message.text,
        params=COMMAND_PARAMS
    ) 
    
    if not (await are_all_params_present(parsed_message, message, COMMAND_PARAMS)):
        return

    room_id = parsed_message['room_id']
    user_id = user.user_id

    existing_room = Room.get_room(room_id=room_id)

    if existing_room is None:
        await message.answer('Room not found') 
        return
    
    existing_connection = Connection.get_connection(user_id=user_id, room_id=room_id)

    if (existing_connection):
        await message.answer('Already joined')  
        return 
    
    Connection.create_connection(
        user_id=user_id, 
        room_id=room_id
    )

    MessageSender.send_message_to_chat_users(
        room_id=room_id,
        message_text=f'New user ```{ user.username }``` has joined the room'
    )

    await message.answer(f'Joined room with id { room_id }')

@registration_required
async def joined_rooms(message: types.Message, user = None):
    """
    This handler sends a list of rooms joined by the user. Authentication is required 
    @command /joined_rooms <room_name>
    """   

    session = create_session()
    
    user_id = user.user_id
    
    joined_rooms = session.query(
            Room
        ).filter(
            Connection.user_id == user_id
        ).filter(
            Room.room_id == Connection.room_id
        ).all()

    await MessageSender.send_message_to_chat(
        message=message,
        message_text=f'You have joined { len(joined_rooms) } rooms'
    ) 
    for room in joined_rooms:
        await MessageSender.send_message_to_chat(
            message=message,
            message_text=f'id:```{ room.room_id }```\nname: ```{ room.name }```'
        )

@registration_required
async def current_room(message: types.Message, user = None):
    """
    This handler outoputs the data of user's current room. Authentication is required 
    @command /current_room
    """   

    user_id = message.chat.id
    
    current_room_data = User.get_users_current_room_data(user_id)

    if not current_room_data:
        await message.answer('Currently you are not in a room') 
        return
    await MessageSender.send_message_to_chat(
        message=message,
        message_text=f'You are in room ```{ current_room_data.name }``` with id ```{ current_room_data.room_id }```', 
    )

@registration_required
async def switch_room(message: types.message, user=None): 
    """
    This handler switches a uset to a chat room. Authentication is required 
    @command /switch_room <room_id>
    """   
    COMMAND_PARAMS = ['room_id']

    session = create_session() 
    
    parsed_message = MessageParser.parse_command_message_by_params(
        message=message.text,
        params=COMMAND_PARAMS
    )

    if not (await are_all_params_present(parsed_message, message, COMMAND_PARAMS)):
        return

    user_id = user.user_id
    room_id = parsed_message['room_id']

    existing_connection = Connection.get_connection(user_id=user_id, room_id=room_id)

    if existing_connection is None:
        await MessageSender.send_message_to_chat(
            message=message,
            message_text='You havent joined the room'
        )
        return

    previous_login_time = existing_connection.last_login

    User.update_current_room_id(
        user_id=user_id,
        room_id=room_id
    )
    Connection.update_last_login(
        room_id=existing_connection.room_id,
        user_id=existing_connection.user_id,
        timestamp=datetime.now()
    )
    session.commit()

    unread_messages = Message.get_messages_after_timestamp(
        room_id=room_id,
        timestamp=previous_login_time
    )
    
    await MessageSender.send_messages_to_chat(
        message=message,
        messages=list(map(
            lambda msg : MessageParser.generate_message_text_from_message_object(
                message=msg,
                message_type='unread'
            ), 
            unread_messages
        ))
    )
    
    await MessageSender.send_message_to_chat_users(
        room_id=room_id,
        message_text=f'New user ```{ user.username }``` has joined the room'
    )

    await MessageSender.send_message_to_chat(
        message=message,
        message_text=f'Switched to room with id ``` { room_id } ```\n'
        'Now all the messages except for commands will be sent in this chatroom', 
    )

@registration_required
async def leave_room(message: types.message, user = None): 
    """
    This handler makes a user leave a room with room_id, all messages associated with the user are deleted. Authentication is required 
    @command /leave_room <room_id>
    """   
    COMMAND_PARAMS = ['room_id']
    
    parsed_message = MessageParser.parse_command_message_by_params(
        message=message.text,
        params=COMMAND_PARAMS
    )

    if not (await are_all_params_present(parsed_message, message, COMMAND_PARAMS)):
        return

    user_id = user.user_id 
    room_id = parsed_message['room_id']

    existing_connection = Connection.get_connection(user_id=user_id, room_id=room_id)

    if existing_connection is None:
        await MessageSender.send_message_to_chat(
            message=message,
            message_text='You havent joined the room'
        )
        return
    
    Connection.delete_connection(
        connection_id=existing_connection.connection_id
    )

    Message.delete_messages(
        user_id=user_id,
        room_id=existing_connection.connection_id
    ) 

    await MessageSender.send_message_to_chat_users(
        room_id=room_id,
        message_text=f'User { user.username } has left the chat!'
    )

    await MessageSender.send_message_to_chat(
        message=message,
        message_text=f'You have left the room and your messages have been deleted'
    )

def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        create_room,
        commands=['create_room']
    )
    dp.register_message_handler(
        join_room,
        commands=['join_room']
    )
    dp.register_message_handler(
        joined_rooms,
        commands=['joined_rooms']
    )
    dp.register_message_handler(
        current_room,
        commands=['current_room']
    )
    dp.register_message_handler(
        switch_room,
        commands=['switch_room']
    )
    dp.register_message_handler(
        leave_room,
        commands=['leave_room']
    )
    
    
    
    
    

        
    
