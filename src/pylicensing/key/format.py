from dataclasses import dataclass, field


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
    lowercase_ascii: bool = field(kw_only=True, default=False)
    uppercase_ascii: bool = field(kw_only=True, default=True)
    numeric_characters: bool = field(kw_only=True, default=False)
    special_characters: bool = field(kw_only=True, default=False)

    def __post_init__(self) -> None:
        if not self.sections:
            raise ValueError(f"Sections must be greater than 0")

        elif not self.chars_per_section:
            raise ValueError(f"Characters per section must be greater than 0")

        elif len(self.seperator) >= 2:
            raise ValueError(f"Seperator should be a single character")

        elif (
            self.seperator.isnumeric()
            or self.seperator.isalpha()
            or self.seperator in r"!§$%&/()[]\/+#<>"
        ):
            raise ValueError(f"Invalid seperator")

        elif not any(
            (
                self.lowercase_ascii,
                self.uppercase_ascii,
                self.numeric_characters,
                self.special_characters,
            )
        ):
            raise ValueError("Key format cannot forbid all characters!")
