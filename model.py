import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["LLMChatMongo"]
users = db["users"]
sessions = db["sessions"]
messages = db["messages"]

user = {
    "name":"murugan",
    "email":"murugan@yahoo.in"
}
user_result = users.insert_one(user)
user_id = user_result.inserted_id
print("User ID: ", user_id)

session_1 = {
    "user_id": user_id,
    "model_name":"gpt-5",
    "started_at": "2026-08-15T09:27:00"
}
session_2 = {
    "user_id": user_id,
    "model_name": "gpt-5",
    "started_at": "2026-08-16T04:20:36"
}

session_result = sessions.insert_many([session_1,session_2])
session_ids = session_result.inserted_ids

print("Sessions IDs:",session_ids)

messages_data = [
    {
        "session_id": session_ids[0],
        "role": "user",
        "content": "Explain SQL window functions",
        "created_at": "2026-08-16T04:21:00",
        "tokens":{
            "input": 50,
            "output": 100,
            "total":150
        }
    },
    {
        "session_id": session_ids[0],
        "role": "assistant",
        "content": "Window functions perform calculations across related rows.",
        "created_at": "2026-08-16T04:21:02",
        "tokens": {
            "input": 100,
            "output": 200,
            "total": 300
        }
    },
    {
        "session_id": session_ids[0],
        "role": "user",
        "content": "Give me an example using RANK",
        "created_at": "2026-08-30T10:02:00",
        "tokens": {
            "input": 40,
            "output": 80,
            "total": 120
        }
    },
    {
        "session_id": session_ids[1],
        "role": "user",
        "content": "What is MongoDB?",
        "created_at": "2026-08-30T11:01:00",
        "tokens": {
            "input": 30,
            "output": 70,
            "total": 100
        }
    }
]

message_result = messages.insert_many(messages_data)
print("message ids:",message_result.inserted_ids)