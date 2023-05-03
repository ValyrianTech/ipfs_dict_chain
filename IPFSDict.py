from typing import Optional, Dict, Any, List, Tuple

from IPFS import IPFSError, add_json, get_json
from CID import CID


class IPFSDict(Dict):
    """A dictionary-like object that stores its data on IPFS.

    :param cid: The IPFS content identifier (CID) of the dictionary data, defaults to None
    :type cid: Optional[str], optional
    """

    def __init__(self, cid: Optional[str] = None):
        super().__init__()
        self._cid = CID(cid).__str__() if cid is not None else None

        if self._cid is not None:
            self.load(cid=self._cid)

    def items(self) -> List[Tuple[str, Any]]:
        """Get the dictionary data. This is a list of key-value pairs with all the data except values that start with an underscore.

        :return: The dictionary data
        :rtype: List[Tuple[str, Any]]
        """
        return [(key, value) for key, value in self.__dict__.items() if key[0] != '_']

    def cid(self) -> str:
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
        self._cid = add_json(data=dict(self.items()))
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

        self._cid = CID(cid).__str__()

        for key, value in data.items():
            if key != '_cid':
                self.__setattr__(key, value)
