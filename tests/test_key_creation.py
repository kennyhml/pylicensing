from datetime import datetime, timedelta
from time import sleep
from pymongo import MongoClient
import dotenv
import os
import pytest

from pylicensing.key import Key, KeyFormat
from pylicensing.managing.queries import add_key_to_database, remove_key_from_database

REG_FORMAT = KeyFormat(5, 5, "-")
dotenv.load_dotenv(dotenv.find_dotenv())

password = os.environ.get("FULL_PERM_PW")

test_client: MongoClient = MongoClient(
    f"mongodb+srv://kennyhml:{password}@ccdb.uo7s992.mongodb.net/?retryWrites=true&w=majority"
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
    add_key_to_database(key, test_client.test.keys)
    sleep(10)
    remove_key_from_database(key, test_client.test.keys)