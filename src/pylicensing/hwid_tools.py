import machineid  # type: ignore[import]

from . import exceptions
from .key import Key


def get_device_hwid() -> str:
    """Returns the hashed HWID of the current device using `machineid`.

    If the HWID grab failed, a `HWIDNotDeterminedError` will be raised from
    the original exception.

    See here for reference: https://github.com/denisbrodbeck/machineid.
    """
    try:
        machine_id = machineid.hashed_id()
        return machine_id
    except Exception as e:
        print(f"HWID grab failed! {e}")
        raise exceptions.HWIDNotDeterminedError(e)


def add_device_hwid(key: Key) -> None:
    """Adds the HWID of the current device to a `Key`.

    Note that this will only update the `Key` instance, and not update the key
    in the database.

    Raises
    ------
    `ExceededMaximumHWIDError`
        If the limit of allowed HWIDs on the key is being exceeded

    `HWIDAlreadyRegisteredError`
        If the HWID is already registered on this key
    """
    if not key.hwid_limit:
        return

    if len(key.hwids) >= key.hwid_limit:
        raise exceptions.ExceededMaximumHWIDError(key)

    machine_id = get_device_hwid()
    if machine_id in key.hwids:
        raise exceptions.HWIDAlreadyRegisteredError(machine_id)

    key.hwids.append(machine_id)


def device_hwid_allowed(key: Key) -> bool:
    """Returns whether the HWID of the current device is registered on a `Key`."""
    return get_device_hwid() in key.hwids or not key.hwid_limit



