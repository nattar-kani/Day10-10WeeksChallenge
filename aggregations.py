import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["LLMChatMongo"]

messages = db["messages"]
sessions = db["sessions"]
users = db["users"]
print(messages.find_one())
# Pipeline 1: Message count per session
result = messages.aggregate([
    {
        "$group":{
            "_id": "$session_id",
            "message_count": {"$sum": 1}
        }
    }
])
for row in result:
    print(row)

# Pipeline 2 — Total tokens per session

result = messages.aggregate([
    {
        "$group":{
            "_id": "$session_id",
            "total_tokens": {
                "$sum": "$tokens.total"
            }
        }
    }
])
for row in result:
    print(row)

# Pipeline 3 — Average tokens per message by session

result = messages.aggregate([
    {
        "$group":{
            "_id":"$session_id",
            "avg_tokens":{
                "$avg": "$tokens.total"
            }
        }
    }
])
for row in result:
    print(row)

# Pipeline 4 — Sessions ranked by total tokens
result = messages.aggregate([
    {
        "$group":{
            "_id":"$session_id",
            "total_tokens":{
                "$sum": "$tokens.total"
            }
        }
    },
    {
        "$sort":{
            "total_tokens": -1
        }

    }
])
for row in result:
    print(row)

# Pipeline 5 — Find messages with high token usage greater than 100
result = messages.aggregate([
    {
        "$match":{
            "tokens.total":{
                "$gt":150
            }
        }

    },
    {
        "$project":{
            "_id":0,
            "message_id":"$_id",
            "session_id": 1,
            "total_tokens": "$tokens.total"
        }
    }
])
for row in result:
    print(row)

# Pipeline 6 — Join messages with users
result = messages.aggregate([
    {
        "$lookup":{
            "from":"sessions",
            "localField":"session_id",
            "foreignField":"_id",
            "as":"session"
        }
    }
])
for row in result:
    print(row)

# Pipeline 7 — lookup + unwind
result = messages.aggregate([
    {
        "$lookup":{
            "from": "sessions",
            "localField": "session_id",
            "foreignField": "_id",
            "as": "session"
        }
    },
    {
        "$unwind": "$session"
    },
    {
        "$project":{
            "_id":0,
            "message_id": "_id",
            "session_id": 1,
            "role": 1,
            "model_name": "$session.model_name"
        }
    }
])
for row in result:
    print(row)

# Pipeline 8 — Total tokens by model
result = messages.aggregate([
    {
        "$lookup": {
            "from": "sessions",
            "localField": "session_id",
            "foreignField": "_id",
            "as": "session"
        }
    },
    {
        "$unwind":"$session"
    },
    {
        "$group": {
            "_id": "$session.model_name",
            "total_tokens": {
                "$sum": "$tokens.total"
            }
        }
    }
])
for row in result:
    print(row)

# Pipeline 9 — Messages by role
result = messages.aggregate([
    {
        "$group": {
            "_id": "$role",

            "total_messages": {
                "$sum": 1
            }
        }
    }
])
for row in result:
    print(row)

# Pipeline 10 — Top 3 messages by token usage
result = messages.aggregate([
    {
        "$sort": {
            "tokens.total": -1
        }
    },
    {
        "$limit": 3
    },
    {
        "$project":{
            "_id": 0,
            "message_id": "$_id",
            "role": 1,
            "total_tokens": "$tokens.total"
        }
    }
])
for row in result:
    print(row)