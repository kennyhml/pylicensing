import os

import dotenv
from pymongo import MongoClient

from pylicensing import KeyFormat, KeyManager, hwid_tools, validation

if __name__ == "__main__":

    # first we recreate the format of the key, the same format was used to create the key.
    format = KeyFormat(
        sections=5,
        chars_per_section=5,
        seperator="-",
        numeric_characters=True,
        lowercase_ascii=True,
    )

    # the connection string to my mongodb test database is included in a .env file for security reasons.
    dotenv.load_dotenv(dotenv.find_dotenv())

    # This is the key that was created in create.py
    key = "P4DtL-gy68x-gI9P3-R8oKe-4S51j"
    
    # Now, before even establishing a connection to our database, we check whether the key matches the format
    # it should have been created with to begin with. In the case of this example, the format is valid.
    if not validation.conforms_format(key, format, show_reason=True):
        print("The key is not valid!")
        exit()

    # I establish the connection to mongodb and pass the collection the keys are stored in to the
    # pylicensing key_manager
    client: MongoClient = MongoClient(os.environ.get("ACCESS_CONN"))
    key_manager = KeyManager(client.test.example)

    # Now, we get the key from the database. If a key is not found, a LookupError is raised.
    # If the key is found, we get a `Key` object which includes all data of the key.
    try:
        license_key = key_manager.get(key)
    except LookupError:
        print("Key does not exist!")
        exit()

    # Now we can check whether the key has expired
    if license_key.expired:
        print("Key has expired!")
        exit()

    # Now we check whether the machine is allowed for this key
    if not license_key.hwids:
        # no devices are registered on this license yet
        hwid_tools.add_device_hwid(license_key)
        key_manager.update(license_key)
    
    elif hwid_tools.device_hwid_allowed(license_key):
        # hwid already registered
        print("Logged in successfully!")
    else:
        # The device is not already registered, attempt to register it.
        # This will raise an error if the hwid limit is being exceeded
        print("New login detected, attempting to register hwid...")
        hwid_tools.add_device_hwid(license_key)