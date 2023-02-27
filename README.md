# Anonymous telegram chat bot 

## Overview

This is a telegram bot that allows users to create and join anonymous chat rooms and communicate with other users. 

The bot was created using python `aiogram` library. 

Data about rooms, users and sent messages is stored in `sqlite` database, connection to the database was created via python's `sqlalchemy` library 

## Initialising and running the project 

Install dependencies 
```
pip install -r ./requirements.txt
``` 

Setup `config.json`, add key: 
```
{
    "BOT_TOKEN": "..."
}
```
Run the project:

```
python3 ./run.py
```

## Functionality 

The bot supports the following commands: 

- `/start`, `/help` - get the list of all possible commands 
- `/create_room <room_name>` - create a new chat room, returns an id of the newly created room 
- `/joined_rooms` - returns a list of all rooms joined by a user 
- `/join_room <room_id>` - join a room by room's id 
- `/switch_room <room_id>` - switch current room to room with id equal to room_id. After that all messages will be sent to the specified room 
- `/leave_room <room_id>` - allows the user to leave a room, after that all messages are deleted from the database  