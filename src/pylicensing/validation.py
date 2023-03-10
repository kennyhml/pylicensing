from .key import Key, KeyFormat


def conforms_format(
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
    
    char_match_problem = _characters_match_format(key, format)
    if char_match_problem is None:
        return True
    
    _show_reason(char_match_problem)
    return False

def _characters_match_format(key: str, format: KeyFormat) -> str | None:
    """Checks whether the characters of the string match the format, i.e it
    contains all types of characters the format specified, but not characters
    the format does not allow.
    
    Returns the reason the format does not match is valid if it is invalid,
    otherwise `None`.
    """
    key = key.replace(format.seperator, "")
    specials = r"!§$%&/()[]\/+#<>"

    for char in key:
        if char.islower() and not format.lowercase_ascii:
            return f"Char '{char}' does not match non lower character format."
            
        if char.isupper() and not format.uppercase_ascii:
            return f"Char '{char}' does not match non upper character format."
            
        if char.isnumeric() and not format.numeric_characters:
            return f"Char '{char}' does not match non numeric character format."
            
        if char in specials and not format.special_characters:
            return f"Char '{char}' does not match non special character format."
            
    if format.special_characters and not any(c in specials for c in key):
        return f"Key is missing special characters"
        
    if format.lowercase_ascii and not any(c.islower() for c in key):
        return f"Key is missing lowercase characters"
        
    if format.uppercase_ascii and not any(c.isupper() for c in key):
        return f"Key is missing uppercase characters"
        
    if format.numeric_characters and not any(c.isnumeric() for c in key):
        return f"Key is missing numeric characters"
    return None
