class QueryError(Exception):
    """Base class for all errors occurring during key query"""


class KeyAlreadyExistsError(QueryError):
    """Raised when a key already exists in a collection"""


class KeyDoesntExistError(QueryError):
    """Raised when an expected key does not exist, for example during deletion"""


class LicenseKeyError(Exception):
    """Base class for all license key errors"""

    def __init__(self, key) -> None:
        self.key = key

    def __str__(self) -> str:
        return f"Unknown error for {self.key}"

class ExceededMaximumHWIDError(LicenseKeyError):
    def __str__(self) -> str:
        return (
            f"Attempted to exceed maximum HWID limit for {self.key.key}.\n"
            f"{self.key.hwid_limit} allowed, {len(self.key.hwids)} registered.\n"
            f"{self.key.hwids}"
        )
    

class HWIDError(Exception):
    """Base class for all hwid related exceptions"""

    def __init__(self, hwid) -> None:
        self.hwid = hwid

    def __str__(self) -> str:
        return f"Unknown error for HWID {self.hwid}"


class HWIDAlreadyRegisteredError(HWIDError):
    """Raised when a HWID is already registered on a device."""

    def __str__(self) -> str:
        return f"HWID {self.hwid} is already registered on this key!"


class HWIDNotDeterminedError(HWIDError):
    """Raised when the HWID of the current device could not be determined"""

    def __str__(self) -> str:
        return f"Failed to determine the HWID on {self.hwid}"
