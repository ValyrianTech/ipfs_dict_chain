from typing import Any


class CID:
    def __init__(self, value: str):
        """
        Initialize a CID object with the given value.

        :param value: The CID value as a string.
        """
        if not isinstance(value, str):
            raise ValueError(f'Value of a cid must be a string, got {type(value)} instead')

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
