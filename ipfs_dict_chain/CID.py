"""Content Identifier (CID) representation for IPFS."""

import re
from typing import Any

BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE58_FLICKR = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
BASE32_LOWER = 'abcdefghijklmnopqrstuvwxyz234567'
BASE32_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
BASE16_LOWER = '0123456789abcdef'
BASE16_UPPER = '0123456789ABCDEF'
BASE36_LOWER = '0123456789abcdefghijklmnopqrstuvwxyz'
BASE36_UPPER = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class CID:
    """
    A class representing a Content Identifier (CID) in the IPFS network.

    :param value: The CID value as a string.
    """

    # Full CID (with optional /ipfs/ prefix)
    CID_REGEX = re.compile(
        rf'^(/ipfs/)?('
        rf'[{BASE58}]{{46}}|'
        rf'b[{BASE32_LOWER}]+|'
        rf'B[{BASE32_UPPER}]+|'
        rf'z[{BASE58}]+|'
        rf'9[{BASE58_FLICKR}]+|'
        rf'f[{BASE16_LOWER}]+|'
        rf'F[{BASE16_UPPER}]+|'
        rf'U[{BASE36_UPPER}]+|'
        rf'V[{BASE36_LOWER}]+'
        rf')$'
    )

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
