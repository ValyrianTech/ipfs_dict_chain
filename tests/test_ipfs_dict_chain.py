import unittest
from ..IPFS import IPFSCache, add_json, get_json


class TestIPFSCache(unittest.TestCase):

    def test_cache_set_and_get(self):
        cache = IPFSCache()
        test_data = {"key": "value"}
        test_cid = "QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5"
        cache.set(test_cid, test_data)
        self.assertEqual(test_data, cache.get(test_cid))


class TestIPFSFunctions(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
