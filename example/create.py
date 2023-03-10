import os
from datetime import timedelta

import dotenv
from pymongo import MongoClient

from pylicensing import Key, KeyFormat, KeyManager

if __name__ == "__main__":

    # first we create the format of the key. If you use a uniform format for all keys on
    # certain application, it can later be useful when validating the key on the client side
    # because if it does not conform to the format you can avoid checking the database.
    format = KeyFormat(
        sections=5,
        chars_per_section=5,
        seperator="-",
        numeric_characters=True,
        lowercase_ascii=True,
    )

    # the connection string to my mongodb test database is included in a .env file for security
    # reasons. It is strongly recommended to not include any sort of full access connection string
    # on the client side of your application. Only include the read-only-user, if possible encrypt it
    dotenv.load_dotenv(dotenv.find_dotenv())

    # Now I create a key with the format we just specified
    key = Key.create(format, "Example User", hwid_limit=1, valid_for=timedelta(days=3))
    
    # I establish the connection to mongodb and pass the collection the keys are stored in to the
    # pylicensing key_manager
    client: MongoClient = MongoClient(os.environ.get("ACCESS_CONN"))
    key_manager = KeyManager(client.test.example)

    # Now the key is added to the collection. At this point the `Key` object actually gets it's ObjectId
    # assigned, but it will not be stored locally. Getting the key in a letter session is done via the key-string
    # as they also server as unique identifiers.
    key_manager.add_to_collection(key)

    """>>> 'P4DtL-gy68x-gI9P3-R8oKe-4S51j' has been inserted into users at 640a8dd2614255acef6afa1d!"""
