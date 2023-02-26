from random import randint 

POOL = 'abcdefghijklmnopqrstuvwxyz&$#@1234567890' 
ID_LENGTH = 20

def generate_id() -> str:
    """
    Generates a random id
    :return: str
    """
    result = ''
    for _ in range(ID_LENGTH):
        result += POOL[randint(0, len(POOL) - 1)] 
    return result