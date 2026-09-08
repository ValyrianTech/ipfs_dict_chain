# noqa: N999
"""IPFS client utilities for adding and retrieving JSON data."""

import asyncio
import atexit
import json
import time

import aioipfs
from multiaddr import Multiaddr

_loop = None

def _get_loop() -> asyncio.AbstractEventLoop:
    """Return the global asyncio event loop, creating it if necessary.

    If the global event loop is ``None`` or has been closed, a new event loop
    is created and set as the current event loop for the thread.

    :returns: The global asyncio event loop.
    :rtype: asyncio.AbstractEventLoop
    """
    global _loop
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop

@atexit.register
def _close_loop() -> None:
    """Close the global asyncio event loop at interpreter shutdown.

    This function is registered with :func:`atexit.register` so that the
    event loop is properly cleaned up when the Python interpreter exits.
    If the loop is already closed or was never created, no action is taken.
    """
    global _loop
    if _loop is not None and not _loop.is_closed():  # pragma: no cover
        _loop.close()  # pragma: no cover
        _loop = None  # pragma: no cover

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5001
multi_address = Multiaddr(f'/ip4/{DEFAULT_HOST}/tcp/{DEFAULT_PORT}')


def connect(host: str, port: int) -> None:
    """Connect to an IPFS daemon.

    :param host: The host of the IPFS daemon.
    :type host: str
    :param port: The port of the IPFS daemon.
    :type port: int
    :raises IPFSError: If the connection to the IPFS daemon fails.
    """
    global multi_address
    multi_address = Multiaddr(f'/ip4/{host}/tcp/{port}')
    try:
        _ = _get_loop().run_until_complete(_test_connection())
    except Exception as e:  # noqa: BLE001
        raise IPFSError(f'Failed to connect to IPFS daemon at {multi_address}: {e}')


class IPFSError(Exception):
    """Custom exception for IPFS-related errors."""


class IPFSCache:
    """An in-memory cache for IPFS data with TTL-based expiration.

    Entries are stored with an expiry timestamp. When an entry is retrieved,
    it is checked for expiration; expired entries are automatically removed.
    The TTL can be configured via the ``ttl`` parameter (default 300 seconds).
    """

    def __init__(self, ttl: int = 300) -> None:
        """Initialize an empty IPFS cache.

        :param ttl: Time-to-live for cache entries in seconds. Defaults to 300.
        :type ttl: int
        """
        self._cache: dict[str, tuple[dict, float]] = {}
        self._ttl: int = ttl

    def get(self, cid: str) -> dict | None:
        """Retrieve data from the cache by its Content Identifier (CID).

        Expired entries are removed and ``None`` is returned.

        :param cid: The Content Identifier (CID) of the data in the cache.
        :type cid: str
        :return: The data retrieved from the cache, or ``None`` if not found or expired.
        :rtype: Optional[Dict]
        """
        entry = self._cache.get(cid)
        if entry is None:
            return None
        data, expiry = entry
        if time.time() > expiry:
            del self._cache[cid]
            return None
        return data

    def set(self, cid: str, data: dict) -> None:
        """Store data in the cache with its Content Identifier (CID).

        The entry will expire after the configured TTL.

        :param cid: The Content Identifier (CID) of the data.
        :type cid: str
        :param data: The data to be stored in the cache.
        :type data: Dict
        """
        self._cache[cid] = (data, time.time() + self._ttl)

    def clear(self) -> None:
        """Remove all entries from the cache."""
        self._cache.clear()

    def cleanup(self) -> None:
        """Remove all expired entries from the cache."""
        now = time.time()
        expired = [cid for cid, (_, expiry) in self._cache.items() if now > expiry]
        for cid in expired:
            del self._cache[cid]


ipfs_cache = IPFSCache()


async def get_file_content(cid: str) -> str:
    """Retrieve the content of a file from IPFS by its Content Identifier (CID).

    :param cid: The Content Identifier (CID) of the file in IPFS.
    :type cid: str
    :return: The content of the file.
    :rtype: str
    """
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    try:
        content = await client.cat(cid)
        return content.decode()
    finally:
        await client.close()


async def _add_json(data: dict) -> str:
    """Add JSON data to IPFS and return its Content Identifier (CID).

    :param data: The JSON data to be added to IPFS.
    :type data: Dict
    :return: The Content Identifier (CID) of the added JSON data.
    :rtype: str
    """
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    try:
        response = await client.add_json(data=data)
    except Exception as e:  # noqa: BLE001
        raise IPFSError(f'Failed to add JSON data to IPFS: {e}')
    finally:
        await client.close()

    cid = response.get('Hash')
    if cid is None:
        raise IPFSError('IPFS response did not contain a Hash/CID')
    return cid


async def _get_json(cid: str) -> dict:
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
    except Exception as e:  # noqa: BLE001
        raise IPFSError(f'Failed to retrieve json data from IPFS hash {cid}: {e}')

    try:
        json_data = json.loads(data)
    except Exception as e:  # noqa: BLE001
        raise IPFSError(f'Failed to parse json data from IPFS hash {cid}: {e}')

    ipfs_cache.set(cid, json_data)
    return json_data


async def _test_connection() -> bool:
    """Test the connection to the IPFS daemon using a read-only operation.

    :return: True if the connection is successful.
    :rtype: bool
    :raises IPFSError: If the connection test fails.
    """
    client = aioipfs.AsyncIPFS(maddr=multi_address)

    try:
        await client.id()
    except Exception as e:  # noqa: BLE001
        raise IPFSError(f'Failed to connect to IPFS daemon at {multi_address}: {e}')
    finally:
        await client.close()

    return True


def add_json(data: dict) -> str:
    """Add JSON data to IPFS and return its Content Identifier (CID) using a synchronous wrapper.

    :param data: The JSON data to be added to IPFS.
    :type data: Dict
    :return: The Content Identifier (CID) of the added JSON data.
    :rtype: str
    """
    return _get_loop().run_until_complete(_add_json(data=data))


def get_json(cid: str) -> dict:
    """Retrieve JSON data from IPFS by its Content Identifier (CID) using a synchronous wrapper.

    :param cid: The Content Identifier (CID) of the JSON data in IPFS.
    :type cid: str
    :return: The JSON data retrieved from IPFS.
    :rtype: Dict
    """
    return _get_loop().run_until_complete(_get_json(cid=cid))
