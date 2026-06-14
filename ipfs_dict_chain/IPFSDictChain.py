"""Dictionary-like data structure that stores its state on IPFS and keeps track of changes."""

import sys
from typing import Optional, Dict, Any, List

from .IPFS import IPFSError, get_json
from .IPFSDict import IPFSDict


class IPFSDictChain(IPFSDict):
    """A dictionary-like data structure that stores its state on IPFS and keeps track of changes.

    :param cid: The IPFS CID to initialize the dictionary with, defaults to None
    :type cid: Optional[str], optional
    """

    def __init__(self, cid: Optional[str] = None):
        """Initialize the IPFSDictChain object.

        :param cid: The IPFS CID to initialize the dictionary with, defaults to None.
        :type cid: Optional[str], optional
        """
        super(IPFSDictChain, self).__init__(cid=cid)

        self.previous_cid: Optional[str] = self.get('previous_cid')

    def save(self) -> str:
        """Saves the current state of the dictionary to IPFS and returns the new CID.

        :return: The new IPFS CID
        :rtype: str
        """
        self.previous_cid = self._cid
        return super().save()

    def changes(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary containing the changes between the current state and the previous state.

        :return: A dictionary of changes, with keys as attribute names and values as dictionaries containing the old and new values
        :rtype: Dict[str, Dict[str, Any]]
        """
        if self.previous_cid is not None:
            try:
                old_data = get_json(self.previous_cid)
            except IPFSError:
                # Previous state no longer available, treat all current data as new
                changes = {key: {'new': value} for key, value in dict(self.items()).items() if key != 'previous_cid'}
                return changes
            current_items = dict(self.items())

            changes = {}
            # Detect changed keys
            for key in old_data:
                if key == 'previous_cid':
                    continue
                if key in current_items:
                    if old_data[key] != current_items[key]:
                        changes[key] = {'old': old_data[key], 'new': current_items[key]}
                else:
                    # Key was deleted
                    changes[key] = {'old': old_data[key], 'new': None}

            # Detect new keys
            for key in current_items:
                if key == 'previous_cid':
                    continue
                if key not in old_data:
                    changes[key] = {'new': current_items[key]}
        else:
            changes = {key: {'new': value} for key, value in dict(self.items()).items() if key != 'previous_cid'}

        return changes

    def _get_previous_cid_for(self, cid: str) -> Optional[str]:
        """Lightweight fetch of just the previous_cid for a given state CID.

        This avoids creating a full IPFSDictChain instance which would make
        unnecessary network calls for data we don't need.

        :param cid: The CID of the state to fetch previous_cid from
        :type cid: str
        :return: The previous CID, or None if not found or on error
        :rtype: Optional[str]
        """
        try:
            data = sys.modules['ipfs_dict_chain.IPFSDict'].get_json(cid)
        except IPFSError:
            return None
        return data.get('previous_cid')

    def get_previous_states(self, max_depth: Optional[int] = None) -> List[Dict[str, Any]]:
        """Returns a list of previous states as dictionaries.

        :param max_depth: The maximum number of previous states to return, defaults to None
        :type max_depth: Optional[int], optional
        :return: A list of previous state dictionaries
        :rtype: List[Dict[str, Any]]
        """
        previous_states: List[Dict[str, Any]] = []

        # First, collect all CIDs using lightweight traversal
        cids = []
        current_cid = self.previous_cid
        depth = 0
        while current_cid is not None and (max_depth is None or depth < max_depth):
            cids.append(current_cid)
            current_cid = self._get_previous_cid_for(current_cid)
            if current_cid is None:
                break
            depth += 1

        # Then load each state's data
        for cid in cids:
            try:
                data = sys.modules['ipfs_dict_chain.IPFSDict'].get_json(cid)
                # Filter out internal keys
                state = {k: v for k, v in data.items() if k != '_cid'}
                previous_states.append(state)
            except IPFSError:
                break

        return previous_states

    def get_previous_cids(self, max_depth: Optional[int] = None) -> List[str]:
        """Returns a list of previous CIDs.

        Uses lightweight fetches to traverse the chain without loading
        full state data.

        :param max_depth: The maximum number of previous CIDs to return, defaults to None
        :type max_depth: Optional[int], optional
        :return: A list of previous CIDs
        :rtype: List[str]
        """
        previous_cids: List[str] = []
        current_cid = self.previous_cid
        depth = 0

        while current_cid is not None and (max_depth is None or depth < max_depth):
            previous_cids.append(current_cid)
            current_cid = self._get_previous_cid_for(current_cid)
            if current_cid is None:
                break
            depth += 1

        return previous_cids
