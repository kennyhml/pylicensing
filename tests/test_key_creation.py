import os
from datetime import datetime, timedelta

import dotenv
import pytest
from pymongo import MongoClient

from pylicensing.key import Key, KeyFormat
from pylicensing.management.queries import (add_key_to_collection,
                                            remove_key_from_collection)
from pylicensing.validation import get_key, key_exists

REG_FORMAT = KeyFormat(5, 5, "-")
dotenv.load_dotenv(dotenv.find_dotenv())

all_perm_conn: MongoClient = MongoClient(os.environ.get("ACCESS_CONN"))

read_only_conn: MongoClient = MongoClient(
    os.environ.get("READ_CONN")
)


def test_key_uniqueness() -> None:
    SAMPLES = 20000

    keys = [
        Key.create(REG_FORMAT, f"Test{i}", True, 3, timedelta(30))
        for i in range(SAMPLES)
    ]
    assert len({key.key for key in keys}) == SAMPLES


def test_key_expiration_date() -> None:
    key = Key.create(REG_FORMAT, f"Test", True, 3, timedelta(30))

    assert key.valid_until.day == (datetime.now() + timedelta(30)).day


def test_invalid_formats() -> None:

    with pytest.raises(ValueError):
        KeyFormat(0, 5, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 0, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(0, 0, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "A", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "--", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "-", uppercase_ascii=False)


def test_key_upload() -> None:
    key = Key.create(REG_FORMAT, f"Test", True, 3, timedelta(30))
    add_key_to_collection(key, all_perm_conn.test.keys)
    remove_key_from_collection(key, all_perm_conn.test.keys)


def test_key_read() -> None:
    key = Key.create(REG_FORMAT, f"Test", True, 3, timedelta(30))
    add_key_to_collection(key, all_perm_conn.test.keys)

    assert key_exists(key.key, read_only_conn.test.keys)
    queried_key = get_key(key.key, read_only_conn.test.keys)
    assert queried_key.to_database_data() == key.to_database_data()

    remove_key_from_collection(key, all_perm_conn.test.keys)
