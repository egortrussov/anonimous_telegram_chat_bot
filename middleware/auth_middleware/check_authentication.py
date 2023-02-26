from db.db import create_session 
from db.models.User import User

def check_user_authentication(user_id: str) -> bool:
    """
    Checks if user with user_id is authenticated 
    :return: bool
    """
    session = create_session() 

    existing_user = session.query(User).filter_by(user_id=user_id).first() 

    return not(existing_user is None)