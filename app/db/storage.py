from pymongo import MongoClient
from config.config import Config
from constants import CONFIG_FILE_PATH
import motor.motor_asyncio
from .helper import *

# ToDo create config from file
config = Config(yaml_file=CONFIG_FILE_PATH)
engine = "mongodb"
user = "eobuser"
password = "eobuserpass"
auth_db = "eob_system"
host = "eobdb-service"
port = "10010"
uri = "mongodb://%s:%s@%s:%s/%s" % (
    user, password, host, port, auth_db)
db = motor.motor_asyncio.AsyncIOMotorClient(uri)
storage = db.eob_system
twitter_cleared = storage.get_collection(
    "twitter_cleared")  # ?twitter cleared message collection
twitter_msg = storage.get_collection(
    "twitter_msg")  # ?twitter messages collection


async def get_dirty_twitter(profile: str) -> dict:
    """Add twitter msgs from user to db"""
    message_list = []
    pipeline = [
        {
            "$lookup": {
                "from": "twitter_cleared",
                "localField": "_id",
                "foreignField": "_id",
                "as": "cleared"
            }
        },
        {
            "$match": {
                "cleared._id": {
                    "$exists": False
                }
            }
        }
    ]
    async for message in twitter_msg.aggregate(pipeline):
        message_list.append(messageEntity(message))
    return message_list


async def save_cleared_twitter(messages_data: [dict]) -> dict:
    """Add cleared twitter msgs from user to db"""
    message_list = []
    profile = messages_data[0]["profile"]
    await twitter_cleared.insert_many(messages_data)
    async for message in twitter_cleared.find({"profile": profile}):
        message_list.append(clearedMessageEntity(message))
    return message_list
