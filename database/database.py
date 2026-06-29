#(©)CodeXBotz
#recoded by @Its_Oreki_Hotarou


import pymongo, os
import motor.motor_asyncio
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

async_dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
async_database = async_dbclient[DB_NAME]

# Database collections
user_data = database['users']
premium_user = database['premium']
fsub_data = async_database['fsub']

# FSub functions
async def add_fsub(chat_id: int, title: str):
    await fsub_data.update_one({'_id': chat_id}, {'$set': {'title': title}}, upsert=True)

async def del_fsub(chat_id: int):
    await fsub_data.delete_one({'_id': chat_id})

async def get_fsubs():
    fsubs = []
    async for doc in fsub_data.find():
        fsubs.append({'chat_id': doc['_id'], 'title': doc.get('title', 'Unknown')})
    return fsubs

async def is_fsub(chat_id: int):
    found = await fsub_data.find_one({'_id': chat_id})
    return bool(found)

# User functions
async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)


async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return


async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])

    return user_ids


async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return


# Premium user functions
async def is_premium(user_id: int):
    found = premium_user.find_one({'_id': user_id})
    return bool(found)


async def add_premium(user_id: int):
    premium_user.insert_one({'_id': user_id})
    return


async def get_premium_users():
    premium_docs = premium_user.find()
    premium_ids = []
    for doc in premium_docs:
        premium_ids.append(doc['_id'])

    return premium_ids


async def remove_premium(user_id: int):
    premium_user.delete_one({'_id': user_id})
    return
