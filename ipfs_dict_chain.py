#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import aioipfs
from multiaddr import Multiaddr
import logging
from typing import Any, Dict, Coroutine

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

CLIENT = None
IPFS_CACHE = {}

HOST = '127.0.0.1'
PORT = 5001
multi_address = Multiaddr(f'/ip4/{HOST}/tcp/{PORT}')


class IPFSError(Exception):
    pass


async def add_files(files: list) -> Dict[str, str]:
    client = aioipfs.AsyncIPFS(maddr=multi_address)
    cids = {}

    async for added_file in client.add(*files, recursive=True):
        cids[added_file['Name']] = added_file['Hash']

    await client.close()
    return cids


async def get(cid: str) -> str:
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    await client.get(cid, dstdir='.')
    await client.close()

    with open(cid, 'r') as f:
        data = f.read()

    os.remove(cid)

    return data


async def add_json(data: dict) -> str:
    client = aioipfs.AsyncIPFS(maddr=multi_address)
    response = await client.add_json(data=json.dumps(data, indent=2, sort_keys=True))
    await client.close()
    return response.get('Hash', None)


def get_json(cid: str) -> Coroutine[Any, Any, str] | Any:
    global IPFS_CACHE

    if cid in IPFS_CACHE:
        return IPFS_CACHE[cid]

    try:
        data = get(cid=cid)
    except Exception as e:
        raise IPFSError(f'Failed to retrieve json data from IPFS hash {cid}: {e}')

    IPFS_CACHE[cid] = data
    return data
