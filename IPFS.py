#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import aioipfs
from multiaddr import Multiaddr


IPFS_CACHE = {}
HOST = '127.0.0.1'
PORT = 5001
multi_address = Multiaddr(f'/ip4/{HOST}/tcp/{PORT}')


class IPFSError(Exception):
    """Custom exception for IPFS-related errors."""
    pass


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


async def add_json(data: dict) -> str:
    """Add JSON data to IPFS and return its Content Identifier (CID).

    Args:
        data (dict): The JSON data to be added to IPFS.

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


async def get_json(cid: str) -> dict:
    """Retrieve JSON data from IPFS by its Content Identifier (CID) and cache the result.

    Args:
        cid (str): The Content Identifier (CID) of the JSON data in IPFS.

    Returns:
        dict: The JSON data retrieved from IPFS.
    """
    global IPFS_CACHE

    if cid in IPFS_CACHE:
        return IPFS_CACHE[cid]

    try:
        data = await get(cid=cid)
    except Exception as e:
        raise IPFSError(f'Failed to retrieve json data from IPFS hash {cid}: {e}')

    try:
        json_data = json.loads(data)
    except Exception as e:
        raise IPFSError(f'Failed to parse json data from IPFS hash {cid}: {e}')

    IPFS_CACHE[cid] = data
    return json_data
