from typing import Optional, Dict, Any, Coroutine

from ipfs_dict_chain import IPFSError, add_json, get_json
from CID import CID


class IPFSDict:
    def __init__(self, cid: Optional[str] = None):
        self._cid = CID(cid).__str__() if cid is not None else None

        if self._cid is not None:
            self.load(cid=self._cid)

    def get(self) -> Dict[str, Any]:
        return {key: value for key, value in self.__dict__.items() if key[0] != '_'}

    def cid(self) -> str:
        return self._cid

    def save(self) -> Coroutine[Any, Any, str]:
        self._cid = add_json(data=self.get())
        return self._cid

    def load(self, cid: str) -> None:
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
