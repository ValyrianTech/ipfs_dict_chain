"""Dictionary-like object that stores its data on IPFS."""

from typing import Optional, Dict, Any, List, Tuple

from .IPFS import IPFSError, add_json, get_json
from .CID import CID


class IPFSDict(Dict):
    """A dictionary-like object that stores its data on IPFS.

    :param cid: The IPFS content identifier (CID) of the dictionary data, defaults to None
    :type cid: Optional[str], optional
    """

    _DICT_METHODS = frozenset({
        'items', 'keys', 'values', 'get', 'pop', 'update', 'clear',
        'copy', 'fromkeys', 'setdefault', 'popitem'
    })

    def __init__(self, cid: Optional[str] = None):
        """Initialize the IPFSDict object.

        :param cid: The IPFS content identifier (CID) of the dictionary data, defaults to None.
        :type cid: Optional[str], optional
        """
        super().__init__()
        self._cid = CID(cid).__str__() if cid is not None else None

        if self._cid is not None:
            self.load(cid=self._cid)

    def __setattr__(self, key: str, value: Any) -> None:
        """Set attribute, storing data keys in the inherited dict."""
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            super().__setitem__(key, value)

    def __getattribute__(self, key: str) -> Any:
        """Get attribute, retrieving data keys from the inherited dict."""
        if key.startswith('_') or key in IPFSDict._DICT_METHODS:
            return super().__getattribute__(key)
        try:
            return super().__getitem__(key)
        except KeyError:
            return super().__getattribute__(key)

    def items(self) -> List[Tuple[str, Any]]:  # type: ignore[override]
        """Get the dictionary data. This is a list of key-value pairs with all the data except values that start with an underscore.

        :return: The dictionary data
        :rtype: List[Tuple[str, Any]]
        """
        return [(key, value) for key, value in super().items() if not key.startswith('_')]

    def cid(self) -> Optional[str]:
        """Get the IPFS content identifier (CID) of the dictionary data.

        :return: The CID
        :rtype: str
        """
        return self._cid

    def save(self) -> str:
        """Save the dictionary data to IPFS and update the CID.

        :return: The new CID
        :rtype: str
        """
        self._cid = add_json(data=dict(self))
        return self._cid

    def load(self, cid: str) -> None:
        """Load the dictionary data from IPFS using the given CID.

        :param cid: The IPFS content identifier (CID) of the dictionary data
        :type cid: str
        :raises ValueError: If the CID is not a string
        :raises IPFSError: If there is an issue retrieving the data from IPFS
        """
        if not isinstance(cid, str):
            raise ValueError(f'Can not retrieve IPFS data: cid must be a string or unicode, got {type(cid)} instead')

        try:
            data = get_json(cid=cid)
        except IPFSError as e:
            raise IPFSError(f'Can not retrieve IPFS data of {cid}: {e}')

        if not isinstance(data, dict):
            raise IPFSError(f'IPFS cid {cid} does not contain a dict!')

        for key, value in data.items():
            if key != '_cid':
                super().__setitem__(key, value)

        self._cid = CID(cid).__str__()

    def __str__(self) -> str:
        """Convert the IPFSDict object to a string representation.

        :return: The string representation of the IPFSDict object
        :rtype: str
        """
        return str(dict(self))

    def __setitem__(self, key: str, value: Any) -> None:
        """Set the value of the given key in the IPFSDict object.

        :param key: The key to set the value for
        :type key: str
        :param value: The value to set
        :type value: Any
        """
        if key.startswith('_'):
            raise KeyError(f"Keys starting with '_' are reserved for internal use: {key}")
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> Any:
        """Get the value of the given key in the IPFSDict object.

        :param key: The key to get the value for
        :type key: str
        :return: The value of the given key
        :rtype: Any
        """
        return super().__getitem__(key)
