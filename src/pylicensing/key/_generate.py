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
    return format.seperator.join(
        generate_section(format) for _ in range(format.sections)
    )
