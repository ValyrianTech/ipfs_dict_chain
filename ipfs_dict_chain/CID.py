"""Content Identifier (CID) representation for IPFS."""

import re
from typing import Any


class CID:
    """
    A class representing a Content Identifier (CID) in the IPFS network.

    :param value: The CID value as a string.
    """

    # CIDv0: starts with Qm, always 46 characters (base58)
    CIDV0_REGEX = re.compile(r'^[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{46}$')
    # CIDv1: starts with multibase prefix, then base-encoded data (variable length)
    CIDV1_REGEX = re.compile(r'^[bBzZ9FfUV][123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]+$')
    # Full CID (with optional /ipfs/ prefix)
    CID_REGEX = re.compile(r'^(/ipfs/)?([123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{46}|[bBzZ9FfUV][123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]+)$')

    def __init__(self, value: str) -> None:
        """Initialize the CID object.

        :param value: The CID value as a string.
        :type value: str
        :raises ValueError: If the provided value is not a valid CID string.
        """
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

    def __ne__(self, other: Any) -> bool:
        """Return True if the other object is not a CID or has a different value, False otherwise."""
        return not self.__eq__(other)

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
