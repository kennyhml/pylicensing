# pylicensing
Pylicensing is a leightweight tool designed to make key authentication and creation on your distributed python programs easier.
It connects to a mongodb database. Click this link to learn more about [mongodb](https://www.mongodb.com/), a nosql easy-to-use database with a free tier.


## How to install
Pylicensing can be installed via pypi
```py
pip install pylicensing
```

## Warning
I do not recommend to connect to the database on the client directly. If your program was to be cracked, you would expose a database connection string to a possibly malicious person. Be precautious and introduce an API between your client and the database. Pylicensing provides the methods your API client needs.

You can still use pylicensing on your user client, as you could for example check that the `Key` your user entered conforms the `KeyFormat` you used for your application, this would prevent people from spamming meaningless keys.

## Features
- Customize the Format of a `Key`, i.e allow sets of characters, customize amount of sections...
- `Key` metadata (creation date, expiration date, owner, hwids..)
- HWID limitations and registrations (max hwids, registered hwids...)
- Key format validations, to avoid requesting a database query.
- Easy database management and queries

# Example
You can also check the [examples folder](https://github.com/kennyhml/pylicensing/edit/master/README.md) in the repository for more detailed examples.

## Creating a `Key` object
```py
my_key_format = KeyFormat(
    sections=5, chars_per_section=5, seperator="-", numeric_characters=True
)
new_user_key = Key.create(
    my_key_format, user="Freddie Faulig", hwid_limit=1, valid_for=timedelta(days=30)
)
```
## Establishing your database connection
```py
client: MongoClient = MongoClient(os.environ.get("DATABASE_CONNECTION"))
key_manager = KeyManager(client.test.example)
```

## Adding a key to the database
```py
new_user_key = Key.create(
    my_key_format, user="Freddie Faulig", hwid_limit=1, valid_for=timedelta(days=30)
)
key_manager = KeyManager(client.test.example)

key_manager.add_to_collection(new_user_key)
```
