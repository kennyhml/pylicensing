from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from bson.objectid import ObjectId

from ._generate import generate_key
from .format import KeyFormat


@dataclass
class Key:
    """Key information container.

    A key provides all information related to a license such as
    the key itself, the owner of the key, HWIDs and expiration data.

    The `KeyFormat` used to create the key should be remembered, as it can
    later be used to validate that the key is of a correct format, to avoid
    checking the database for a key that wouldn't possibly be valid to begin with.

    Note that, during key creation, it will not automatically be checked
    whether the key already exists, meaning you avoid choosing short key
    formats, such as 1 section with 5 characters, of course allowed characters
    also play a role here.

    A `key` object is hashable, because the key is not expected to change during
    it's lifetime, thus they are hashed by key.
    """

    key: str
    owner: str
    hwid_locked: bool
    hwid_limit: int
    created: datetime
    valid_until: datetime
    hwids: list = field(default_factory=list)
    _id: ObjectId | None = None

    @classmethod
    def create(
        cls,
        format: KeyFormat,
        owner: str,
        hwid_locked: bool,
        hwid_limit: int,
        valid_for: timedelta,
    ) -> Key:
        """Returns a `Key` created from a `KeyFormat` and other details.\n
        The key will be randomly generated using said format during creation.
        """
        return cls(
            generate_key(format),
            owner,
            hwid_locked,
            hwid_limit,
            created=datetime.now().replace(microsecond=0),
            valid_until=(datetime.now() + valid_for).replace(microsecond=0),
        )

    def to_database_data(self) -> dict:
        """Turns a `Key` into the data that is valuable for the database.

        For this, the `__dict__` of the `Key` is copied and the `_id` is popped
        off, since mongodb sets its own `_id`.
        """
        data = self.__dict__.copy()
        data.pop("_id")
        return data
