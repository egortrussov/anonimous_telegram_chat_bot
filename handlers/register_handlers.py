from aiogram import Dispatcher

import handlers.start_handlers as start_handlers
import handlers.message_handlers as message_handlers 
import handlers.rooms_handlers as rooms_handlers

def register_handlers(dp: Dispatcher) -> None:
    """
    Registers all application handlers
    """
    rooms_handlers.register_handlers(dp) 
    start_handlers.register_handlers(dp) 
    message_handlers.register_handlers(dp)