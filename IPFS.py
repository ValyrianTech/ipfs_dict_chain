#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import os
import aioipfs
from multiaddr import Multiaddr
from typing import Dict
from contextlib import contextmanager

HOST = '127.0.0.1'
PORT = 5001
multi_address = Multiaddr(f'/ip4/{HOST}/tcp/{PORT}')


class IPFSError(Exception):
    """Custom exception for IPFS-related errors."""
    pass


class IPFSCache:
    """A simple cache for IPFS data."""

    def __init__(self):
        self._cache = {}

    def get(self, cid: str):
        return self._cache.get(cid)

    def set(self, cid: str, data: Dict):
        self._cache[cid] = data


ipfs_cache = IPFSCache()


@contextmanager
def event_loop():
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


async def get(cid: str) -> str:
    """Retrieve the content of a file from IPFS by its Content Identifier (CID).

    Args:
        cid (str): The Content Identifier (CID) of the file in IPFS.

    Returns:
        str: The content of the file.
    """
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    await client.get(cid, dstdir='.')
    await client.close()

    with open(cid, 'r') as f:
        data = f.read()

    os.remove(cid)

    return data


async def _add_json(data: Dict) -> str:
    """Add JSON data to IPFS and return its Content Identifier (CID).

    Args:
        data (Dict): The JSON data to be added to IPFS.

    Returns:
        str: The Content Identifier (CID) of the added JSON data.
    """
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    try:
        response = await client.add_json(data=data)
    except Exception as e:
        raise IPFSError(f'Failed to add JSON data to IPFS: {e}')
    finally:
        await client.close()

    return response.get('Hash', None)


async def _get_json(cid: str) -> Dict:
    """Retrieve JSON data from IPFS by its Content Identifier (CID) and cache the result.

    Args:
        cid (str): The Content Identifier (CID) of the JSON data in IPFS.

    Returns:
        Dict: The JSON data retrieved from IPFS.
    """
    cached_data = ipfs_cache.get(cid)
    if cached_data:
        return cached_data

    try:
        data = await get(cid=cid)
    except Exception as e:
        raise IPFSError(f'Failed to retrieve json data from IPFS hash {cid}: {e}')

    try:
        json_data = json.loads(data)
    except Exception as e:
        raise IPFSError(f'Failed to parse json data from IPFS hash {cid}: {e}')

    ipfs_cache.set(cid, json_data)
    return json_data


def add_json(data: Dict) -> str:
    """Add JSON data to IPFS and return its Content Identifier (CID) using a synchronous wrapper.

    Args:
        data (Dict): The JSON data to be added to IPFS.

    Returns:
        str: The Content Identifier (CID) of the added JSON data.
    """
    with event_loop() as loop:
        cid = loop.run_until_complete(_add_json(data=data))
    return cid


def get_json(cid: str) -> Dict:
    """Retrieve JSON data from IPFS by its Content Identifier (CID) using a synchronous wrapper.

    Args:
        cid (str): The Content Identifier (CID) of the JSON data in IPFS.

    Returns:
        Dict: The JSON data retrieved from IPFS.
    """
    with event_loop() as loop:
        json_data = loop.run_until_complete(_get_json(cid=cid))
    return json_data
