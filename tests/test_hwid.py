from datetime import timedelta

import pytest

from pylicensing import hwid_tools, exceptions
from pylicensing.key import Key, KeyFormat

REG_FORMAT = KeyFormat(5, 5, "-")


def test_hwid_assignment() -> None:
    key = Key.create(REG_FORMAT, f"Test", 1, timedelta(30))
    hwid_tools.add_device_hwid(key)

    assert key.hwids != []


def test_hwid_limit_exceeded() -> None:
    key = Key.create(REG_FORMAT, f"Test", 1, timedelta(30))
    hwid_tools.add_device_hwid(key)

    with pytest.raises(exceptions.ExceededMaximumHWIDError):
        hwid_tools.add_device_hwid(key)


def test_hwid_already_registered() -> None:
    key = Key.create(REG_FORMAT, f"Test", 2, timedelta(30))
    hwid_tools.add_device_hwid(key)

    with pytest.raises(exceptions.HWIDAlreadyRegisteredError):
        hwid_tools.add_device_hwid(key)


def test_hwid_allowed() -> None:
    key = Key.create(REG_FORMAT, f"Test", 1, timedelta(30))
    hwid_tools.add_device_hwid(key)

    assert hwid_tools.device_hwid_allowed(key)

    key.hwids = ["This is not a valid HWID"]
    assert not hwid_tools.device_hwid_allowed(key)
