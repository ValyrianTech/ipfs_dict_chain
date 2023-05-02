import re
from typing import Any


class CID:
    """
    A class representing a Content Identifier (CID) in the IPFS network.

    :param value: The CID value as a string.
    """

    CID_REGEX = re.compile(r'^(/ipfs/)?[A-Za-z0-9]+$')

    def __init__(self, value: str) -> None:
        if not isinstance(value, str) or not self.CID_REGEX.match(value):
            raise ValueError(f'Invalid CID value: {value}')

        self.value = value if value.startswith('/ipfs/') else f'/ipfs/{value}'

    def __str__(self) -> str:
        """Return the string representation of the CID object."""
        return self.value

    def __repr__(self) -> str:
        """Return a more informative representation of the CID object."""
        return f"CID('{self.value}')"

    def __eq__(self, other: Any) -> bool:
        """Return True if the other object is a CID with the same value, False otherwise."""
        if not isinstance(other, CID):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Return the hash value of the CID object."""
        return hash(self.value)

    def short(self) -> str:
        """
        Return the short version of the CID value.

        :return: The short CID value as a string.
        """
        return self.value[6:]

    def long(self) -> str:
        """
        Return the long version of the CID value.

        :return: The long CID value as a string.
        """
        return self.value
