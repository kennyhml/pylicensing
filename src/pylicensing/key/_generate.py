import random
import string

from .format import KeyFormat


def generate_section(format: KeyFormat) -> str:
    """Generates a singular section of a key, the length and allowed
    characters depend on the passed `format`.
    """
    mapped = {
        string.ascii_uppercase: format.uppercase_ascii,
        string.ascii_lowercase: format.lowercase_ascii,
        "".join(str(i) for i in range(10)): format.numeric_characters,
        r"!§$%&/()[]\/+#<>": format.special_characters,
    }
    allowed = "".join(k for k, v in mapped.items() if v)
    return "".join(random.choice(allowed) for _ in range(format.chars_per_section))


def generate_key(format: KeyFormat) -> str:
    """Generates a key string given a format."""
    key = format.seperator.join(
        generate_section(format) for _ in range(format.sections)
    )
    return _add_missing_characters(key, format)


def _add_missing_characters(key: str, format: KeyFormat) -> str:
    def replace(key: str, index: int, new_char: str) -> str:
        if key[index] == format.seperator:
            index += 1
        return key[:index] + new_char + key[index + 1 :]

    if format.lowercase_ascii and not any(c.islower() for c in key):
        key = replace(
            key, random.randrange(len(key)), random.choice(string.ascii_lowercase)
        )
        return _add_missing_characters(key, format)

    if format.uppercase_ascii and not any(c.isupper() for c in key):
        key = replace(
            key, random.randrange(len(key)), random.choice(string.ascii_uppercase)
        )
        return _add_missing_characters(key, format)

    if format.numeric_characters and not any(c.isnumeric() for c in key):
        key = replace(
            key,
            random.randrange(len(key)),
            random.choice("".join(str(i) for i in range(10))),
        )
        return _add_missing_characters(key, format)

    if format.special_characters and not any(c in r"!§$%&/()[]\/+#<>" for c in key):
        key = replace(
            key, random.randrange(len(key)), random.choice(r"!§$%&/()[]\/+#<>")
        )

    return key
