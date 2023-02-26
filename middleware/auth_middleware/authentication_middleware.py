from aiogram import types
from sqlalchemy import or_

from db.db import create_session

from db.models.User import User

def registration_required(function):
    """
    A decorator that checks if a user has been registered
    """
    async def decorator(message: types.Message):
        user_id = message.chat.id 
        
        existing_user = User.get_user_data_by_id(user_id)
        
        if existing_user is None:
            await message.answer("You have to register first") 
            return
        
        return await function(message, user=existing_user) 
    return decorator

def current_room_required(function):
    """
    A decorator that checks if a user has chosen a current room
    """
    async def decorator(message, **kwargs):        
        user_id = message.chat.id 
        
        existing_user = User.get_user_data_by_id(user_id)
        
        if existing_user.current_room_id is None:
            await message.answer("You have to choose or join a room to send messages") 
            return
        
        return await function(
            message, 
            room_id=existing_user.current_room_id,
            **kwargs
        ) 
    return decorator

def validate_username(username: str) -> bool:
    """
    Checks if given username is valid
    :return: bool
    """
    if not (3 <= len(username) <= 10):
        return False
    for character in username:
        if not character.isalnum():
            return False 
    return True

def check_if_user_exists(username: str, user_id: str) -> bool:
    """
    Checks if user with user_id or username already exists
    :return: bool
    """
    session = create_session() 

    existing_user: User = session.query(
            User
        ).filter(
            or_(User.user_id == user_id, User.username == username)
        ).first()

    return not (existing_user is None)