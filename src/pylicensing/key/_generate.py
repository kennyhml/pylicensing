import random
import string

from .format import KeyFormat


def generate_random_sequence(rules: KeyFormat) -> str:
    mapped = {
        string.ascii_uppercase: rules.uppercase_ascii,
        string.ascii_lowercase: rules.lowercase_ascii,
        "".join(str(i) for i in range(10)): rules.numeric_characters,
        r"!§$%&/()[]\/+#<>": rules.special_characters,
    }
    allowed = "".join(k for k, v in mapped.items() if v)
    return "".join(random.choice(allowed) for _ in range(rules.chars_per_section))


def generate_key(rules: KeyFormat) -> str:
    return rules.seperator.join(
        generate_random_sequence(rules) for _ in range(rules.sections)
    )
