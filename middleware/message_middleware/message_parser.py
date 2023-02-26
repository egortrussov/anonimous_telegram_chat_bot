from db.models.Message import Message

class MessageParser():

    def __init__(self):
        pass 

    @staticmethod
    def get_message_words(message: str) -> list:
        """
        Returns a list of words in a message, split by space symbol 
        :return: list[str]
        """
        words_list = list(filter(lambda x : x != '', message.split(' '))) 
        return words_list

    @staticmethod
    def parse_command_message_by_params(message: str, params: list[str]=[]) -> dict:
        """
        Parses a message and splits data by params
        :return: dict
        """
        message_words = MessageParser.get_message_words(message)[1:]

        message_data: dict = dict() 
        for (index, param) in enumerate(params):
            message_data[param] = None if index >= len(message_words) else message_words[index] 
        
        return message_data

    @staticmethod 
    def create_chat_message(message: str, sender_username: str):
        """
        Creates a chat message 
        :return: str
        """
        return '``` ' + f'New message by { sender_username }: ' ' ```\n' + message 
    
    @staticmethod 
    def generate_message_text_from_message_object(message: Message, message_type='none') -> str:
        """
        Generated a chat message based on its type
        :return: str
        """
        if message_type == 'none':
            return message.text 
        elif message_type == 'unread':
            return '``` Unread message:\n```' + message.text + '\n``` At ' + str(message.time) + '```' 