from ..key import Key, KeyFormat


def key_conforms_format(
    key: Key | str, format: KeyFormat, *, show_reason: bool = False
) -> bool:
    """Returns whether a `Key` conforms to a `KeyFormat`.

    Parameters
    ----------
    key :class:`Key`:
        The key to check

    format :class:`KeyFormat`:
        The format that the key should follow

    show_reason :class:`bool`:
        Whether to print the reason a key is not valid in the console.
    """

    def _show_reason(reason) -> None:
        if show_reason:
            print(f"Key format is not valid: {reason}.")

    if isinstance(key, Key):
        key = key.key

    if format.seperator not in key:
        _show_reason(f"Key has no seperator '{format.seperator}'")
        return False

    sections = key.split(format.seperator)
    if not len(sections) == format.sections:
        _show_reason(f"Format has {format.sections} sections, key has {len(sections)}")
        return False

    if any((format.chars_per_section != len(subsection) for subsection in sections)):
        _show_reason(f"Chars per section do not match {format.chars_per_section}")
        return False

    key_string = key.replace(format.seperator, "")
    specials = r"!§$%&/()[]\/+#<>"

    for char in key_string:
        if char.islower() and not format.lowercase_ascii:
            _show_reason(f"Char '{char}' does not match non lower character format.")
            return False

        if char.isupper() and not format.uppercase_ascii:
            _show_reason(f"Char '{char}' does not match non upper character format.")
            return False

        if char.isnumeric() and not format.numeric_characters:
            _show_reason(f"Char '{char}' does not match non numeric character format.")
            return False

        if char in specials and not format.special_characters:
            _show_reason(f"Char '{char}' does not match non special character format.")
            return False

    if format.special_characters and not any(c in specials for c in key_string):
        _show_reason(f"Key is missing special characters")
        return False

    if format.lowercase_ascii and not any(c.islower() for c in key_string):
        _show_reason(f"Key is missing lowercase characters")
        return False

    if format.uppercase_ascii and not any(c.isupper() for c in key_string):
        _show_reason(f"Key is missing uppercase characters")
        return False

    if format.numeric_characters and not any(c.isnumeric() for c in key_string):
        _show_reason(f"Key is missing numeric characters")
        return False

    return True
