from sqlalchemy import Column, delete
from sqlalchemy.sql.sqltypes import String, DateTime
from datetime import datetime

from db.db import SqlAlchemyBase, create_session

from middleware.auth_middleware.generate_id import generate_id

class Message(SqlAlchemyBase):
    __tablename__ = 'messages' 

    message_id = Column(String, nullable=False, primary_key=True)
    room_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    time = Column(DateTime, nullable=False) 

    @staticmethod
    def create_message(sender_id: str, room_id: str, message_text: str) -> None:
        """
        Adds a new message data to database
        """
        session = create_session() 

        new_message = Message(
            message_id=generate_id(),
            room_id=room_id,
            user_id=sender_id,
            text=message_text,
            time=datetime.now()
        ) 

        session.add(new_message) 
        session.commit()
    
    @staticmethod 
    def get_messages_after_timestamp(room_id: str, timestamp: datetime) -> list:
        """
        Gets a list of messages that were sent after a given timestamp 
        :return: list[Message]
        """
        session = create_session() 

        messages_list = session.query(
            Message
        ).filter(
            Message.room_id == room_id
        ).filter(
            Message.time >= timestamp
        ).all()

        return messages_list
    
    @staticmethod 
    def delete_messages(**kwargs):
        """
        Deletes messages that satisfy given criterias
        """
        session = create_session() 

        session.execute(
            delete(
                Message
            ).filter_by(
                **kwargs
            )
        )

        session.commit()