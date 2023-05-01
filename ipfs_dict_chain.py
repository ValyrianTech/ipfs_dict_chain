#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import aioipfs
from multiaddr import Multiaddr
from typing import Any, Coroutine


IPFS_CACHE = {}
HOST = '127.0.0.1'
PORT = 5001
multi_address = Multiaddr(f'/ip4/{HOST}/tcp/{PORT}')


class IPFSError(Exception):
    pass


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

    try:
        response = await client.add_json(data=data)
    except Exception as e:
        raise IPFSError(f'Failed to add json data to IPFS: {e}')
    finally:
        await client.close()

    return response.get('Hash', None)


async def get_json(cid: str) -> Coroutine[Any, Any, str] | Any:
    global IPFS_CACHE

    if cid in IPFS_CACHE:
        return IPFS_CACHE[cid]

    try:
        data = await get(cid=cid)
    except Exception as e:
        raise IPFSError(f'Failed to retrieve json data from IPFS hash {cid}: {e}')

    IPFS_CACHE[cid] = data
    return data
