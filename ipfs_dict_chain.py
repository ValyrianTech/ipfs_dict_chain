#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ipfshttpclient
import logging
from typing import Any, Dict, Optional, Union

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

IPFS_API = None
IPFS_CACHE = {}


class IPFSError(Exception):
    pass


def connect_to_ipfs(host: str, port: int) -> None:
    global IPFS_API

    multi_address = f'/ip4/{host}/tcp/{port}/http'
    LOG.info(f'Trying to connect with IPFS on {multi_address}')
    try:
        IPFS_API = ipfshttpclient.connect(multi_address)
        LOG.info('Connected with IPFS')
    except Exception as ex:
        raise IPFSError(f'IPFS node is not running: {ex}')


def check_ipfs() -> bool:
    if IPFS_API is not None:
        return True
    else:
        LOG.warning('Not connected to IPFS, trying to reconnect')
        connect_to_ipfs()

    return IPFS_API is not None


class CID:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f'Value of a cid must be a string, got {type(value)} instead')

        self.value = value if value.startswith('/ipfs/') else f'/ipfs/{value}'

    def __str__(self) -> str:
        return self.value

    def short(self) -> str:
        return self.value[6:]

    def long(self) -> str:
        return self.value


def add_json(data: Dict[str, Any]) -> str:
    global IPFS_API

    if not check_ipfs():
        raise IPFSError("Not connected to IPFS")

    try:
        cid = IPFS_API.add_json(data)
    except Exception as e:
        raise IPFSError(f'Failed to store json data on IPFS: {e}')

    return CID(cid).__str__()


def get_json(cid: str) -> Optional[Dict[str, Any]]:
    global IPFS_API, IPFS_CACHE

    if not check_ipfs():
        raise IPFSError("Not connected to IPFS")

    if cid in IPFS_CACHE:
        return IPFS_CACHE[cid]

    try:
        json = IPFS_API.get_json(cid, timeout=2)
    except Exception as e:
        raise IPFSError(f'Failed to retrieve json data from IPFS hash {cid}: {e}')

    IPFS_CACHE[cid] = json
    return json


class IPFSDict:
    def __init__(self, cid: Optional[str] = None):
        self._cid = CID(cid).__str__() if cid is not None else None

        if self._cid is not None:
            self.load(cid=self._cid)

    def get(self) -> Dict[str, Any]:
        return {key: value for key, value in self.__dict__.items() if key[0] != '_'}

    def cid(self) -> str:
        return self._cid

    def save(self) -> str:
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


class IPFSDictChain(IPFSDict):
    def __init__(self, cid: Optional[str] = None):
        self.previous_cid = None

        super(IPFSDictChain, self).__init__(cid=cid)

    def save(self) -> str:
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
