from typing import Optional, Dict, Any, List

from .IPFS import add_json
from .IPFSDict import IPFSDict


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
        self._cid = add_json(data=dict(self.items()))
        return self._cid

    def changes(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary containing the changes between the current state and the previous state.

        :return: A dictionary of changes, with keys as attribute names and values as dictionaries containing the old and new values
        :rtype: Dict[str, Dict[str, Any]]
        """
        if self.previous_cid is not None:
            old_data = dict(IPFSDictChain(cid=self.previous_cid).items())

            changes = {
                key: {'old': old_data[key], 'new': self.__getattribute__(key)}
                for key in old_data
                if old_data[key] != self.__getattribute__(key)
            }

            changes.update(
                {
                    key: {'new': self.__getattribute__(key)}
                    for key in dict(self.items())
                    if key not in old_data
                }
            )

        else:
            changes = {key: {'new': self.__getattribute__(key)} for key in dict(self.items())}

        return changes

    def get_previous_states(self, max_depth: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns a list of previous states as dictionaries.

        :param max_depth: The maximum number of previous states to return, defaults to None
        :type max_depth: Optional[int], optional
        :return: A list of previous state dictionaries
        :rtype: List[Dict[str, Any]]
        """
        previous_states = []
        current_cid = self.previous_cid
        depth = 0

        while current_cid is not None and (max_depth is None or depth < max_depth):
            previous_state = IPFSDictChain(cid=current_cid)
            previous_states.append(dict(previous_state.items()))
            current_cid = previous_state.previous_cid
            depth += 1

        return previous_states

    def get_previous_cids(self, max_depth: Optional[int] = None) -> List[str]:
        """Returns a list of previous CIDs.

        :param max_depth: The maximum number of previous CIDs to return, defaults to None
        :type max_depth: Optional[int], optional
        :return: A list of previous CIDs
        :rtype: List[str]
        """
        previous_cids = []
        current_cid = self.previous_cid
        depth = 0

        while current_cid is not None and (max_depth is None or depth < max_depth):
            previous_cids.append(current_cid)
            previous_state = IPFSDictChain(cid=current_cid)
            current_cid = previous_state.previous_cid
            depth += 1

        return previous_cids
