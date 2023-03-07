from importlib_metadata import Lookup
from pymongo import MongoClient
from pymongo.collection import Collection
from ..key import Key


def add_key_to_database(key: Key, collection: Collection) -> None:
    collection.insert_one(key.to_database_data())


def remove_key_from_database(key: Key, collection: Collection) -> None:
    if key._id is not None:
        collection.delete_one({"_id": key._id})
    else:
        collection.delete_one({"key": key.key})
