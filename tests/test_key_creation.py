from datetime import datetime, timedelta

import pytest

from pylicensing import Key, KeyFormat

REG_FORMAT = KeyFormat(5, 5, "-")


def test_key_uniqueness() -> None:
    """Checks that, within 20000 keys there are no duplicates"""
    SAMPLES = 20000

    keys = [
        Key.create(REG_FORMAT, f"Test{i}", 3, timedelta(30))
        for i in range(SAMPLES)
    ]
    assert len({key.key for key in keys}) == SAMPLES


def test_key_expiration_date() -> None:
    """Checks that the expiration date is set as expected"""
    key = Key.create(REG_FORMAT, "Test", 3, timedelta(30))
    assert key.valid_until.day == (datetime.now() + timedelta(30)).day


def test_invalid_formats() -> None:
    """Checks that bad format creation raises an error"""
    with pytest.raises(ValueError):
        KeyFormat(0, 5, "-")

    with pytest.raises(ValueError):
        KeyFormat(5, 0, "-")

    with pytest.raises(ValueError):
        KeyFormat(0, 0, "-")

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "A")

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "--")

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "/")
