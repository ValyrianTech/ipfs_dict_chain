from typing import Optional, Dict, Any

from IPFS import add_json
from IPFSDict import IPFSDict


class IPFSDictChain(IPFSDict):
    """A dictionary-like data structure that stores its state on IPFS and keeps track of changes.

    :param cid: The IPFS CID to initialize the dictionary with, defaults to None
    :type cid: Optional[str], optional
    """

    def __init__(self, cid: Optional[str] = None):
        self.previous_cid = None

        super(IPFSDictChain, self).__init__(cid=cid)

    def save(self) -> str:
        """Saves the current state of the dictionary to IPFS and returns the new CID.

        :return: The new IPFS CID
        :rtype: str
        """
        self.previous_cid = self._cid
        self._cid = add_json(data=self.items())
        return self._cid

    def changes(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary containing the changes between the current state and the previous state.

        :return: A dictionary of changes, with keys as attribute names and values as dictionaries containing the old and new values
        :rtype: Dict[str, Dict[str, Any]]
        """
        if self.previous_cid is not None:
            old_data = IPFSDictChain(cid=self.previous_cid).items()

            changes = {
                key: {'old': old_data[key], 'new': self.__getattribute__(key)}
                for key in old_data
                if old_data[key] != self.__getattribute__(key)
            }

            changes.update(
                {
                    key: {'new': self.__getattribute__(key)}
                    for key in self.items()
                    if key not in old_data
                }
            )

        else:
            changes = {key: {'new': self.__getattribute__(key)} for key in self.items()}

        return changes
