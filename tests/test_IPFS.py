import unittest
import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock
from ipfs_dict_chain.IPFS import IPFSCache, add_json, get_json, connect, IPFSError, get_file_content
from multiaddr.exceptions import StringParseError


class TestIPFSConnection(unittest.TestCase):
    def test_connect_invalid_host(self):
        """Test connection with invalid host"""
        with self.assertRaises(IPFSError):
            try:
                connect('invalid_host', 5001)
            except StringParseError as e:
                raise IPFSError(str(e))

    def test_connect_invalid_port(self):
        """Test connection with invalid port"""
        with self.assertRaises(IPFSError):
            connect('127.0.0.1', 9999)

    @patch('ipfs_dict_chain.IPFS.add_json')
    def test_connect_timeout(self, mock_add_json):
        """Test connection timeout"""
        mock_add_json.side_effect = TimeoutError("Connection timed out")
        with self.assertRaises(IPFSError):
            connect('127.0.0.1', 5001)


class TestIPFSCache(unittest.TestCase):

    def test_cache_set_and_get(self):
        cache = IPFSCache()
        test_data = {"key": "value"}
        test_cid = "QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5"
        cache.set(test_cid, test_data)
        self.assertEqual(test_data, cache.get(test_cid))


class TestIPFSFunctions(unittest.TestCase):
    """Test IPFS operations with focus on error handling and edge cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Clean up test fixtures"""
        self.loop.close()

    def test_add_json(self):
        test_data = {"test_key": "test_value"}
        cid = add_json(test_data)
        self.assertIsNotNone(cid)
        self.assertIsInstance(cid, str)

    def test_get_json(self):
        test_cid = "QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5"
        expected_data = {"key": "value"}
        json_data = get_json(test_cid)
        self.assertEqual(expected_data, json_data)

    def test_add_and_get_json(self):
        test_data = {"test_key": "test_value"}
        cid = add_json(test_data)
        retrieved_data = get_json(cid)
        self.assertEqual(test_data, retrieved_data)

    def test_add_json_empty_data(self):
        """Test adding empty data structure"""
        empty_data = {}
        cid = add_json(empty_data)
        self.assertIsNotNone(cid)
        retrieved_data = get_json(cid)
        self.assertEqual(empty_data, retrieved_data)

    def test_add_json_special_characters(self):
        """Test handling of special characters in data"""
        special_data = {
            "special": "!@#$%^&*()",
            "unicode": "🌟🔥🌈",
            "nested": {"path/with/slashes": "value"}
        }
        cid = add_json(special_data)
        retrieved_data = get_json(cid)
        self.assertEqual(special_data, retrieved_data)

    def test_get_json_invalid_cid(self):
        """Test retrieving data with invalid CID"""
        invalid_cid = "InvalidCID123"
        with self.assertRaises(IPFSError):
            get_json(invalid_cid)

    @patch('aioipfs.AsyncIPFS')
    def test_network_failure(self, mock_ipfs):
        """Test handling of network failures during IPFS operations"""
        mock_client = AsyncMock()
        mock_client.add_json = AsyncMock(side_effect=ConnectionError("Network failure"))
        mock_client.close = AsyncMock()
        mock_ipfs.return_value = mock_client
        
        test_data = {"key": "value"}
        with self.assertRaises(IPFSError):
            add_json(test_data)

    def test_get_file_content(self):
        """Test file content retrieval with various scenarios"""
        # Test successful retrieval
        test_data = b"Test content"
        
        async def mock_successful_retrieval():
            return test_data

        with patch('aioipfs.AsyncIPFS') as mock_ipfs:
            mock_client = AsyncMock()
            mock_client.cat = AsyncMock(return_value=test_data)
            mock_client.close = AsyncMock()
            mock_ipfs.return_value = mock_client
            
            result = self.loop.run_until_complete(get_file_content("valid_cid"))
            self.assertEqual(result, test_data.decode())

        # Test failed retrieval
        with patch('aioipfs.AsyncIPFS') as mock_ipfs:
            mock_client = AsyncMock()
            mock_client.cat = AsyncMock(side_effect=Exception("Failed to retrieve content"))
            mock_client.close = AsyncMock()
            mock_ipfs.return_value = mock_client
            
            with self.assertRaises(Exception):
                self.loop.run_until_complete(get_file_content("invalid_cid"))


class TestIPFSCacheExtended(unittest.TestCase):
    """Extended tests for IPFSCache functionality"""

    def test_cache_miss(self):
        """Test cache miss scenario"""
        cache = IPFSCache()
        self.assertIsNone(cache.get("non_existent_cid"))

    def test_cache_concurrent_access(self):
        """Test concurrent access to cache"""
        cache = IPFSCache()
        test_data = {"key": "value"}
        test_cid = "QmTest123"

        def cache_operation():
            cache.set(test_cid, test_data)
            return cache.get(test_cid)

        # Simulate concurrent access using threads
        import threading
        threads = []
        results = []
        
        for _ in range(10):
            thread = threading.Thread(target=lambda: results.append(cache_operation()))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Verify all operations were successful
        for result in results:
            self.assertEqual(result, test_data)


class TestIPFSLargeData(unittest.TestCase):
    """Test IPFS operations with large data structures"""

    def setUp(self):
        """Set up test fixtures"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Clean up test fixtures"""
        self.loop.close()

    def test_large_nested_structure(self):
        """Test handling of large nested data structures"""
        # Create a large nested dictionary (approximately 1MB)
        large_data = {}
        for i in range(1000):
            large_data[f"key_{i}"] = {
                "nested1": {"data": "x" * 100},
                "nested2": [f"item_{j}" for j in range(100)],
                "nested3": {str(k): k * 100 for k in range(10)}
            }

        # Test adding and retrieving large data
        cid = add_json(large_data)
        self.assertIsNotNone(cid)
        retrieved_data = get_json(cid)
        self.assertEqual(large_data, retrieved_data)

    def test_large_file_content(self):
        """Test handling of large file content"""
        large_content = b"x" * (1024 * 1024)  # 1MB of data
        
        with patch('aioipfs.AsyncIPFS') as mock_ipfs:
            mock_client = AsyncMock()
            mock_client.cat = AsyncMock(return_value=large_content)
            mock_client.close = AsyncMock()
            mock_ipfs.return_value = mock_client
            
            result = self.loop.run_until_complete(get_file_content("large_file_cid"))
            self.assertEqual(len(result), len(large_content.decode()))


class TestIPFSMalformedData(unittest.TestCase):
    """Test IPFS operations with malformed data"""

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_malformed_json(self):
        """Test handling of malformed JSON data"""
        malformed_data = {
            "key": float('inf'),  # JSON doesn't support infinity
            "binary": b"binary_data",  # JSON doesn't support binary
            "function": lambda x: x  # JSON doesn't support functions
        }
        
        with self.assertRaises(IPFSError):
            add_json(malformed_data)

    def test_circular_reference(self):
        """Test handling of circular references"""
        circular_data = {"key": "value"}
        circular_data["self"] = circular_data
        
        with self.assertRaises(IPFSError):
            add_json(circular_data)

    def test_invalid_utf8(self):
        """Test handling of invalid UTF-8 content"""
        with patch('aioipfs.AsyncIPFS') as mock_ipfs:
            mock_client = AsyncMock()
            mock_client.cat = AsyncMock(return_value=b'\xff\xfe\xfd')  # Invalid UTF-8
            mock_client.close = AsyncMock()
            mock_ipfs.return_value = mock_client
            
            with self.assertRaises(UnicodeDecodeError):
                self.loop.run_until_complete(get_file_content("invalid_utf8_cid"))


class TestIPFSDaemonConfig(unittest.TestCase):
    """Test IPFS daemon configuration scenarios"""

    @patch('aioipfs.AsyncIPFS')
    def test_custom_timeout(self, mock_ipfs):
        """Test IPFS operations with custom timeout"""
        mock_client = AsyncMock()
        mock_client.add_json = AsyncMock(side_effect=TimeoutError("Operation timed out"))
        mock_client.close = AsyncMock()
        mock_ipfs.return_value = mock_client

        with self.assertRaises(IPFSError):
            add_json({"key": "value"})

    @patch('aioipfs.AsyncIPFS')
    def test_rate_limiting(self, mock_ipfs):
        """Test handling of rate limiting"""
        mock_client = AsyncMock()
        mock_client.add_json = AsyncMock(side_effect=Exception("Too many requests"))
        mock_client.close = AsyncMock()
        mock_ipfs.return_value = mock_client

        with self.assertRaises(IPFSError):
            add_json({"key": "value"})


class TestIPFSEndToEnd(unittest.TestCase):
    """End-to-end workflow tests"""

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.test_data = {
            "string": "test",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }

    def tearDown(self):
        self.loop.close()

    def test_complex_workflow(self):
        """Test a complex workflow with multiple operations"""
        # Step 1: Add initial data
        cid1 = add_json(self.test_data)
        self.assertIsNotNone(cid1)

        # Step 2: Modify and add updated data
        updated_data = self.test_data.copy()
        updated_data["updated"] = True
        cid2 = add_json(updated_data)
        self.assertNotEqual(cid1, cid2)

        # Step 3: Retrieve and verify both versions
        original_data = get_json(cid1)
        self.assertEqual(original_data, self.test_data)
        
        updated_retrieved = get_json(cid2)
        self.assertEqual(updated_retrieved, updated_data)

    def test_concurrent_operations(self):
        """Test multiple concurrent IPFS operations"""
        async def concurrent_ops():
            tasks = []
            for i in range(5):
                data = {"index": i, **self.test_data}
                # Mock the add_json result
                cid = f"test_cid_{i}"
                tasks.append(asyncio.create_task(get_file_content(cid)))
            return await asyncio.gather(*tasks)

        with patch('aioipfs.AsyncIPFS') as mock_ipfs:
            mock_client = AsyncMock()
            mock_client.cat = AsyncMock(return_value=json.dumps(self.test_data).encode())
            mock_client.close = AsyncMock()
            mock_ipfs.return_value = mock_client
            
            results = self.loop.run_until_complete(concurrent_ops())
            self.assertEqual(len(results), 5)
            for result in results:
                self.assertIsInstance(result, str)
                self.assertTrue(json.loads(result))  # Verify it's valid JSON


if __name__ == '__main__':
    unittest.main()
