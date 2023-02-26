from sqlalchemy import Column, update
from sqlalchemy.sql.sqltypes import String, JSON  

from db.db import SqlAlchemyBase, create_session

from db.models.Room import Room

class User(SqlAlchemyBase):
    __tablename__ = 'users' 

    user_id = Column(String, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    current_room_id = Column(String) 

    @staticmethod
    def get_user_data_by_id(user_id: str): 
        """
        Gets user data from database by user_id 
        :return: User
        """
        session = create_session() 
        user_data = session.query(
                User
            ).filter_by(
                user_id=user_id
            ).first() 
        return user_data

    @staticmethod 
    def get_users_current_room_data(user_id: str):
        """
        Gets user's current room data 
        :return: Room
        """
        session = create_session() 

        room_data = session.query(
            Room
        ).filter(
            User.user_id==user_id
        ).filter(
            Room.room_id == User.current_room_id
        ).first() 

        return room_data

    @staticmethod 
    def update_current_room_id(user_id: str, room_id: str):
        """
        Updates user's current room id
        """
        session = create_session() 

        session.execute(
            update(
                User
            ).where(
                User.user_id == user_id
            ).values(
                current_room_id=room_id
            )
        )

        session.commit()