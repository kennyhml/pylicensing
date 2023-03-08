class QueryError(Exception):
    """Base class for all errors occurring during key query"""

class KeyAlreadyExistsError(QueryError):
    """Raised when a key already exists in a collection"""


class KeyDoesntExistError(QueryError):
    """Raised when an expected key does not exist, for example during deletion"""