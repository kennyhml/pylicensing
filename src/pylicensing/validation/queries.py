from importlib_metadata import Lookup
from pymongo import MongoClient
from pymongo.collection import Collection
from ..key import Key


def key_exists(key: str, collection: Collection) -> bool:
    return collection.find_one({"key": key}) is not None


def get_key(key: str, collection: Collection) -> Key:

    data = collection.find_one({"key": key})
    if not data:
        raise LookupError(f"Could not find key {key} in {collection.name}")

    return Key(key, **data)
