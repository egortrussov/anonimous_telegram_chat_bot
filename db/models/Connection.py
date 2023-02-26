from sqlalchemy import Column, update, delete
from sqlalchemy.sql.sqltypes import String, DateTime
from datetime import datetime

from ..db import SqlAlchemyBase, create_session

from middleware.auth_middleware.generate_id import generate_id

class Connection(SqlAlchemyBase):
    __tablename__ = 'connections' 

    connection_id = Column(String, nullable=False, primary_key=True)
    room_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    last_login = Column(DateTime) 

    @staticmethod
    def create_connection(user_id: str, room_id: str):
        """
        Created a new connection
        """
        session = create_session() 

        new_connection = Connection(
            connection_id=generate_id(),
            room_id=room_id,
            user_id=user_id,
            last_login=datetime.now()
        )

        session.add(new_connection) 
        session.commit() 

    @staticmethod 
    def get_connection(**kwargs):
        """
        Gets connection by fields specified in arguments
        :return: Connection
        """
        session = create_session() 
        
        connection_data = session.query(
                Connection    
            ).filter_by(
                **kwargs
            ).first() 
        
        return connection_data

    @staticmethod 
    def get_connection_list(**kwargs):
        session = create_session() 
        
        connections_data = session.query(
                Connection    
            ).filter_by(
                **kwargs
            ).all() 
        
        return connections_data


    @staticmethod 
    def get_users_connected_to_room(room_id: str) -> list[str]:
        """
        Gets a list of all user ids that are connected to a room
        :return: list[str]
        """
        session = create_session() 

        users_list = session.query(
            Connection
        ).filter_by(
            room_id=room_id
        ).all() 

        users_id = [] 

        for user_data in users_list:
            users_id.append(user_data.user_id) 
        
        return users_id

    @staticmethod
    def update_last_login(room_id: str, user_id: str, timestamp: datetime) -> None:
        """
        Updates a user's last login time to a room 
        """
        session = create_session() 

        session.execute(
            update(
                Connection
            ).where(
                Connection.user_id == user_id and Connection.room_id == room_id
            ).values(
                last_login=timestamp
            )
        )

        session.commit()
    
    @staticmethod 
    def delete_connection(connection_id: str):
        """
        Deletes a connection with id connection_id
        """
        session = create_session() 

        session.execute(
            delete(
                Connection
            ).filter_by(
                connection_id=connection_id
            )
        )

        session.commit()
