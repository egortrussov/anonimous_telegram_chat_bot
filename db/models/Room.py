from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, JSON  

from ..db import SqlAlchemyBase, create_session

from middleware.auth_middleware.generate_id import generate_id

class Room(SqlAlchemyBase):
    __tablename__ = 'rooms' 

    room_id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)

    @staticmethod 
    def create_room(room_name: str) -> str: 
        """
        Adds a new room data to database, returns created room id
        :return: str
        """
        session = create_session() 

        room_id = generate_id()

        new_room = Room(
            room_id=room_id,
            name=room_name
        )
        session.add(new_room) 
        session.commit() 

        return room_id

    @staticmethod 
    def get_room(**kwargs):
        """
        Retrieves room data from database filtered by fields specified in args
        :return: Room
        """
        session = create_session() 

        room_data = session.query(
                Room
            ).filter_by(
                **kwargs
            ).first() 
        
        return room_data