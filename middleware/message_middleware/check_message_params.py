from aiogram import types

from middleware.message_middleware.message_sender import MessageSender

async def are_all_params_present(message_data: dict, message: types.message, params: list[str]) -> bool:
    """
    Checks if all params are specified in message_data
    :return: bool
    """ 
    for param in params:
        if not message_data.get(param):
            await MessageSender.send_message_to_chat(
                message=message,
                message_text=f'You must specify <{ param }>'
            )
            return False 
    
    return True