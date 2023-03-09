from bson.objectid import ObjectId
from pymongo import MongoClient, errors
from pymongo.collection import Collection

from ..exceptions import KeyAlreadyExistsError, KeyDoesntExistError
from ..key import Key


def add_key_to_collection(
    key: Key, collection: Collection, *, ignore_exists: bool = False
) -> None:
    """Adds a `Key` to a `Collection`.

    The key is converted to a dictionary using the keys `to_database_data`,
    which includes everything aside from the `_id` field, as this is meant
    to be generated by mongodb. Once the key has been inserted, the keys
    `_id` will be updated to the inserted id.

    Parameters
    ----------
    key :class:`Key`:
        The key to add to the collection.

    collection :class:`Collection`:
        The collection to add the key to.

    ignore_exists :class:`bool`:
        Whether to ignore the fact that the key already exists.
        In the case of this happening, the key will be inserted regardless.
    """
    if not ignore_exists and collection.find_one({"key": key.key}):
        raise KeyAlreadyExistsError(f"{key.key} already exists in {collection.name}!")

    result = collection.insert_one(key.to_database_data())
    key._id = result.inserted_id


def remove_key_from_collection(
    key: Key, collection: Collection, *, ignore_nonexistent: bool = False
) -> None:
    """Removes a `Key` from a `Collection`.

    The key will be found and deleted using the `_id` if available, otherwise
    they key-string will be used to find and delete it.

    Parameters
    ----------
    key :class:`Key`:
        The key to delete from the collection.

    collection :class:`Collection`:
        The collection to delete the key from.

    ignore_nonexistent :class:`bool`:
        Whether to ignore the fact that the key does not exist within the database.
        In the case of this happening, the key will be inserted regardless
    """
    data: dict[str, str | ObjectId]
    if key._id is not None:
        data = {"_id": key._id}
    else:
        data = {"key": key.key}

    result = collection.delete_one(data)
    if not result.deleted_count and not ignore_nonexistent:
        raise KeyDoesntExistError(f"{key.key} does not exist in {collection.name}")