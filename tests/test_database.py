import os
from datetime import datetime, timedelta

import dotenv
import pytest
from pymongo import MongoClient

from pylicensing import Key, KeyFormat, KeyManager, hwid_tools, exceptions

REG_FORMAT = KeyFormat(5, 5, "-")
dotenv.load_dotenv(dotenv.find_dotenv())
all_perm_conn: MongoClient = MongoClient(os.environ.get("ACCESS_CONN"))
read_only_conn: MongoClient = MongoClient(os.environ.get("READ_CONN"))

database_manger = KeyManager(all_perm_conn.test.keys)


def test_key_upload() -> None:
    """Checks whether we can successfully create, upload and remove a key"""
    key = Key.create(REG_FORMAT, f"Test", True, 3, timedelta(30))
    database_manger.add_to_collection(key)
    database_manger.remove_from_collection(key)


def test_key_read() -> None:
    """Checks that we can successfully create, upload, read then delete a key."""
    key = Key.create(REG_FORMAT, f"Test", True, 3, timedelta(30))
    database_manger.add_to_collection(key)

    assert database_manger.exists(key.key)
    queried_key = database_manger.get(key.key)
    assert queried_key.to_database_data() == key.to_database_data()

    database_manger.remove_from_collection(key)


def test_key_register_hwid() -> None:
    """Checks that we can create a key with a HWID and then add that HWID
    to the database, and retrieve it the same."""
    key = Key.create(REG_FORMAT, "Test", True, 1, timedelta(30))

    hwid_tools.add_device_hwid(key)
    assert key.hwids[0] == hwid_tools.get_device_hwid()

    database_manger.add_to_collection(key)
    queried_key = database_manger.get(key.key)

    assert queried_key.hwids == key.hwids

    with pytest.raises(exceptions.ExceededMaximumHWIDError):
        hwid_tools.add_device_hwid(queried_key)

    queried_key.hwid_limit = 2

    with pytest.raises(exceptions.HWIDAlreadyRegisteredError):
        hwid_tools.add_device_hwid(queried_key)

    database_manger.remove_from_collection(queried_key)


def test_key_update() -> None:
    """Checks whether updating a key already in the database works as expected"""
    key = Key.create(REG_FORMAT, "Test", True, 1, timedelta(30))
    hwid_tools.add_device_hwid(key)

    database_manger.add_to_collection(key)

    key.owner = "Bert"
    key.hwid_limit = 3
    key.hwids[0] = "NOT A VALID HWID"
    database_manger.update(key)

    key = database_manger.get(key.key)
    assert key.owner == "Bert"
    assert key.hwid_limit == 3
    assert key.hwids[0] == "NOT A VALID HWID"

    database_manger.remove_from_collection(key)


def test_wipe_database() -> None:
    """Creates 10 keys, adds them to the database and then checks that they all
    get wiped when wiping the collection."""
    KEYS = 10

    keys = [
        Key.create(REG_FORMAT, f"Test{i}", True, 1, timedelta(30)) for i in range(KEYS)
    ]
    for key in keys:
        database_manger.add_to_collection(key)

    database_manger.wipe_database()

    assert not database_manger.get_all_keys()
