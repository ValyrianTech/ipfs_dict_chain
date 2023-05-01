from typing import Optional, Dict, Any, Coroutine

from ipfs_dict_chain import add_json
from IPFSDict import IPFSDict


class IPFSDictChain(IPFSDict):
    def __init__(self, cid: Optional[str] = None):
        self.previous_cid = None

        super(IPFSDictChain, self).__init__(cid=cid)

    def save(self) -> Coroutine[Any, Any, str]:
        self.previous_cid = self._cid
        self._cid = add_json(data=self.get())
        return self._cid

    def changes(self) -> Dict[str, Dict[str, Any]]:
        changes = {}
        if self.previous_cid is not None:
            old_data = IPFSDictChain(cid=self.previous_cid).get()

            for key in old_data:
                if old_data[key] != self.__getattribute__(key):
                    changes[key] = {'old': old_data[key], 'new': self.__getattribute__(key)}

            for key in self.get():
                if key not in old_data:
                    changes[key] = {'new': self.__getattribute__(key)}

        else:
            for key in self.get():
                changes[key] = {'new': self.__getattribute__(key)}

        return changes
