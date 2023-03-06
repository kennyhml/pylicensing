from dataclasses import dataclass


@dataclass
class KeyFormat:
    """Represents the rules/format of a key"""

    sections: int
    chars_per_section: int
    seperator: str
    lowercase_ascii: bool
    uppercase_ascii: bool
    numeric_characters: bool
    special_characters: bool

    def __post_init__(self) -> None:
        if not any(
            (
                self.lowercase_ascii,
                self.uppercase_ascii,
                self.numeric_characters,
                self.special_characters,
            )
        ):
            raise ValueError("Key format can't forbid all characters!")
