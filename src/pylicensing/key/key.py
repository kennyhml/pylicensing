from dataclasses import dataclass

from bson.objectid import ObjectId

from ._generate import generate_key
from .format import KeyFormat


@dataclass
class Key:
    key: str
    owner: str
    hwid_locked: bool
    hwid_limit: int
    rules: KeyFormat
    db_id: ObjectId | None = None


def create_key(
    rules: KeyFormat, owner: str, hwid_locked: bool, hwid_limit: int = 1
) -> Key:
    return Key(generate_key(rules), owner, hwid_locked, hwid_limit, rules)
