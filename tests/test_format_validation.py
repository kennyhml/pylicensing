import random
from datetime import timedelta

from pylicensing import Key, KeyFormat, validation

ITERATIONS = 2000


def test_nonmatching_section() -> None:
    for _ in range(ITERATIONS):

        key_format = (random.randrange(2, 11), random.randrange(2, 11))
        bad_format = (random.randrange(2, 11), random.randrange(2, 11))

        KEY_FORMAT = KeyFormat(*key_format, "-")
        BAD_FORMAT = KeyFormat(*bad_format, "-")
        key = Key.create(KEY_FORMAT, "Test", 1, timedelta(30))

        assert validation.conforms_format(key, BAD_FORMAT) == (key_format == bad_format)


def build_random_format() -> dict:
    key_rules = {
        param: random.choice([True, False])
        for param in (
            "lowercase_ascii",
            "uppercase_ascii",
            "numeric_characters",
            "special_characters",
        )
    }
    if not any(key_rules.values()):
        key_rules["uppercase_ascii"] = True

    return key_rules


def test_nonmatching_character_rules() -> None:
    for _ in range(ITERATIONS):
        key_rules = build_random_format()
        format_rules = build_random_format()

        KEY_FORMAT = KeyFormat(5, 5, "-", **key_rules)
        BAD_FORMAT = KeyFormat(5, 5, "-", **format_rules)

        key = Key.create(KEY_FORMAT, "Test", 1, timedelta(30))
        assert validation.conforms_format(key, BAD_FORMAT) == (key_rules == format_rules)



