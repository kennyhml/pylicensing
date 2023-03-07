from datetime import timedelta
from datetime import datetime, timedelta
from pylicensing.key import Key, KeyFormat
import pytest

REG_FORMAT = KeyFormat(5, 5, "-")


def test_key_uniqueness() -> None:
    SAMPLES = 2000

    keys = [
        Key.create(REG_FORMAT, f"Test{i}", True, 3, timedelta(30))
        for i in range(SAMPLES)
    ]
    assert len({key.key for key in keys}) == SAMPLES


def test_key_expiration_date() -> None:
    key = Key.create(REG_FORMAT, f"Test", True, 3, timedelta(30))

    assert key.valid_until.day == (datetime.now() + timedelta(30)).day


def test_invalid_formats() -> None:

    with pytest.raises(ValueError):
        KeyFormat(0, 5, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 0, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(0, 0, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "A", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "--", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "-", uppercase_ascii=False)

    with pytest.raises(ValueError):
        KeyFormat(5, 5, "-", uppercase_ascii=False)
