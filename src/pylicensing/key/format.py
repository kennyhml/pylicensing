from dataclasses import dataclass


@dataclass(frozen=True)
class KeyFormat:
    """Contains the rules/formatting of a `Key`.

    Knowing the format of a key can be useful, as it allows to ensure
    that a key conforms to a certain format to avoid unneccessary database
    calls. The uniqueness of a key greatly depends on the chosen format,
    be mindful of the length / allowed characters of your key.

    A `KeyFormat` is frozen, meaning you will not be able to change it once
    it has been created to avoid accidental changing of the key.

    If attempting to create a format with no characters allowed, a `ValueError`
    will be raised as it is not possible.
    """

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
