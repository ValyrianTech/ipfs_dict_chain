#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import aioipfs
from multiaddr import Multiaddr
from typing import Dict

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5001
multi_address = Multiaddr(f'/ip4/{DEFAULT_HOST}/tcp/{DEFAULT_PORT}')

event_loop = asyncio.get_event_loop()


def connect(host: str, port: int) -> None:
    """Connect to an IPFS daemon.

    :param host: The host of the IPFS daemon.
    :type host: str
    :param port: The port of the IPFS daemon.
    :type port: int
    """
    global multi_address
    multi_address = Multiaddr(f'/ip4/{host}/tcp/{port}')


class IPFSError(Exception):
    """Custom exception for IPFS-related errors."""
    pass


class IPFSCache:
    """A simple cache for IPFS data."""

    def __init__(self):
        self._cache = {}

    def get(self, cid: str) -> Dict:
        """Retrieve data from the cache by its Content Identifier (CID).

        :param cid: The Content Identifier (CID) of the data in the cache.
        :type cid: str
        :return: The data retrieved from the cache.
        :rtype: Dict
        """
        return self._cache.get(cid)

    def set(self, cid: str, data: Dict) -> None:
        """Store data in the cache with its Content Identifier (CID).

        :param cid: The Content Identifier (CID) of the data.
        :type cid: str
        :param data: The data to be stored in the cache.
        :type data: Dict
        """
        self._cache[cid] = data


ipfs_cache = IPFSCache()


async def get_file_content(cid: str) -> str:
    """Retrieve the content of a file from IPFS by its Content Identifier (CID).

    :param cid: The Content Identifier (CID) of the file in IPFS.
    :type cid: str
    :return: The content of the file.
    :rtype: str
    """
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    content = await client.cat(cid)
    await client.close()

    return content.decode()


async def _add_json(data: Dict) -> str:
    """Add JSON data to IPFS and return its Content Identifier (CID).

    :param data: The JSON data to be added to IPFS.
    :type data: Dict
    :return: The Content Identifier (CID) of the added JSON data.
    :rtype: str
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

    :param cid: The Content Identifier (CID) of the JSON data in IPFS.
    :type cid: str
    :return: The JSON data retrieved from IPFS.
    :rtype: Dict
    """
    cached_data = ipfs_cache.get(cid)
    if cached_data:
        return cached_data

    try:
        data = await get_file_content(cid=cid)
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

    :param data: The JSON data to be added to IPFS.
    :type data: Dict
    :return: The Content Identifier (CID) of the added JSON data.
    :rtype: str
    """
    cid = event_loop.run_until_complete(_add_json(data=data))
    return cid


def get_json(cid: str) -> Dict:
    """Retrieve JSON data from IPFS by its Content Identifier (CID) using a synchronous wrapper.

    :param cid: The Content Identifier (CID) of the JSON data in IPFS.
    :type cid: str
    :return: The JSON data retrieved from IPFS.
    :rtype: Dict
    """
    json_data = event_loop.run_until_complete(_get_json(cid=cid))
    return json_data
