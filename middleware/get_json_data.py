import json 
import os

json_file = open(os.path.join(os.path.abspath(os.getcwd()), 'config.json')) 

def get_json_data(fields: list[str] = None) -> dict:
    """
    Retrieves data from json file, returns dict containing keys specified in fields list 
    :return: dict
    """
    data = json.load(json_file)

    if fields is None:
        return data
    
    result = dict() 

    for field in fields:
        if field not in data.keys():
            raise Exception(f'Wrong field specified: { field }')
        result[field] = data[field] 
    
    return result