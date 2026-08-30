import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["LLMChatMongo"]
users = db["users"]

users.create_index(
    "email", unique=True
)
# create
user = {
    "name": "Jaya",
    "email": "jaya@gmail.com"
}

result = users.insert_one(user)
print(result.inserted_id)


# read
user = users.find_one({
    "email": "jaya@gmail.com"
})
print(user)


users_list = [
    {
        "name": "Arun",
        "email": "arun@gmail.com"
    },
    {
        "name": "Meena",
        "email": "meena@gmail.com"
    }
]
result = users.insert_many(users_list)
print("Inserted:",result.inserted_ids)

for user in users.find():
    print(user)
# update
result = users.update_one(
    {"email":"jaya@gmail.com"},
    {"$set": {"name": "Jayam"}}
)
print(result.modified_count)

updated_user = users.find_one({
    "email":"jaya@gmail.com"
})
print(updated_user)

result  = users.update_many(
    {"email": {"$regex": "@gmail.com"}},
    {"$set": {"email_verified":True}}
)

for user in users.find():
    print(user)
# delete

result = users.delete_one({
    "email":"jaya@gmail.com"
})
print(result.deleted_count)

result = users.delete_many({
    "email":"jaya@gmail.com"
})
for user in users.find():
    print(user)