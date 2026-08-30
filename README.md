# Day 10 — MongoDB Chat Application

## 🎯 Objective

Model the LLM chat application from the SQL project using **MongoDB**, practice MongoDB CRUD operations and aggregation pipelines, and understand when to choose **SQL, NoSQL, or Vector Databases** for an LLM application.

---

## 🏗️ Project

I built a MongoDB-based data model for an LLM chat application.

### Collections

```text
LLMChatMongo
│
├── users
├── sessions
└── messages
```

### Data relationship

```text
users
  │
  └── user_id
        │
        ▼
     sessions
        │
        └── session_id
              │
              ▼
           messages
```

Messages also contain nested token information:

```json
{
  "role": "user",
  "content": "Explain SQL window functions",
  "tokens": {
    "input": 50,
    "output": 100,
    "total": 150
  }
}
```

---

## 🛠️ Tech Stack

* MongoDB Atlas
* Python
* PyMongo
* python-dotenv
* MongoDB Aggregation Framework

---

## 📁 Project Structure

```text
Day 10/
│
├── mongodb-venv/
├── .env
├── connection.py
├── crud.py
├── model.py
├── aggregations.py
├── DECISION_NOTE.md
├── requirements.txt
└── README.md
```
---

# 1. MongoDB Connection

Connected Python to MongoDB Atlas using **PyMongo**.

```python
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv("atlas-credentials.env")

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["LLMChatMongo"]
```

# 2. CRUD Operations

Implemented MongoDB CRUD operations using PyMongo.

### Create

```python
user = {
    "name": "Jaya",
    "email": "jaya@gmail.com"
}

result = users.insert_one(user)
```

### Read

```python
user = users.find_one({
    "email": "jaya@gmail.com"
})
```

### Update

```python
result = users.update_one(
    {"email": "jaya@gmail.com"},
    {"$set": {"name": "Jayam"}}
)
```

### Delete

```python
result = users.delete_one({
    "email": "jaya@gmail.com"
})
```

Also explored:

* `insert_many()`
* `update_many()`
* `delete_many()`

# 3. Document Modeling

Created users, sessions and messages with relationships using MongoDB `ObjectId`.

Example:

```text
User
 │
 ├── Session 1
 │      ├── Message 1
 │      ├── Message 2
 │      └── Message 3
 │
 └── Session 2
        └── Message 4
```

Explored the difference between:

### Embedded documents

```json
{
  "user": {
    "name": "Jaya",
    "sessions": [...]
  }
}
```

### Separate collections

```text
users
sessions
messages
```

The decision depends on access patterns, document size, relationship complexity and how frequently the data is accessed together.

# 4. MongoDB Aggregation Pipelines

Implemented 10 aggregation pipelines.

| #  | Analysis                            | MongoDB Concepts               |
| -- | ----------------------------------- | ------------------------------ |
| 1  | Message count per session           | `$group`, `$sum`               |
| 2  | Total tokens per session            | `$group`, `$sum`               |
| 3  | Average tokens per session          | `$group`, `$avg`               |
| 4  | Sessions ranked by token usage      | `$sort`                        |
| 5  | Messages using more than 150 tokens | `$match`, `$project`           |
| 6  | Messages with session details       | `$lookup`                      |
| 7  | Flatten joined session data         | `$lookup`, `$unwind`           |
| 8  | Total tokens by model               | `$lookup`, `$unwind`, `$group` |
| 9  | Messages by role                    | `$group`, `$sum`               |
| 10 | Top 3 messages by token usage       | `$sort`, `$limit`, `$project`  |

---

## Important MongoDB Concepts Learned

### `$match`

Similar to SQL `WHERE`.

```python
{
    "$match": {
        "tokens.total": {
            "$gt": 150
        }
    }
}
```

### `$group`

Similar to SQL `GROUP BY`.

```python
{
    "$group": {
        "_id": "$role",
        "total_messages": {
            "$sum": 1
        }
    }
}
```

### `$sort`

Similar to SQL `ORDER BY`.

```python
{
    "$sort": {
        "total_tokens": -1
    }
}
```

### `$project`

Controls which fields appear in the output.

```python
{
    "$project": {
        "_id": 0,
        "message_id": "$_id",
        "total_tokens": "$tokens.total"
    }
}
```

### `$lookup`

Used to combine documents from another collection.

Conceptually similar to a SQL `JOIN`.

```text
messages.session_id
        ↓
        JOIN
        ↓
sessions._id
```

### `$unwind`

Converts an array produced by `$lookup` into individual documents.

```text
session: [ {...} ]
       ↓
session: {...}
```

### `$limit`

Restricts the number of documents returned.

# Conclusion

A real LLM application may use multiple databases:

```text
                 LLM APPLICATION
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
         SQL       MongoDB      Vector DB
          │            │            │
    structured      flexible     embeddings
    relational      documents    semantic search
    transactional   metadata     RAG retrieval
          │            │            │
          └────────────┼────────────┘
                       ↓
                      LLM
```

# What I Learned

* How MongoDB stores JSON-like documents
* How `ObjectId` is used to identify documents
* MongoDB CRUD operations using PyMongo
* How nested fields are accessed using dot notation
* How MongoDB aggregation pipelines work
* `$group`, `$sum`, `$avg`, `$sort`, `$match`, `$project`
* `$lookup` and its similarity to SQL JOINs
* `$unwind` for flattening arrays
* How aggregation stages can be chained together
* How document modeling differs from relational modeling
* When SQL, MongoDB and Vector Databases make sense in an LLM application

---
