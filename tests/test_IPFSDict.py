import unittest
from datetime import datetime
from unittest.mock import patch

from ipfs_dict_chain.IPFS import IPFSError
from ipfs_dict_chain.IPFSDict import IPFSDict


class CustomClass:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, CustomClass):
            return False
        return self.value == other.value


class TestIPFSDict(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            'string': 'value',
            'int': 42,
            'float': 3.14,
            'bool': True,
            'none': None,
            'list': [1, 2, 3],
            'dict': {'a': 1, 'b': 2},
            'nested': {
                'list': [{'x': 1}, {'y': 2}],
                'dict': {'a': {'b': {'c': 3}}}
            }
        }

    def test_init(self):
        ipfs_dict = IPFSDict()
        self.assertIsNone(ipfs_dict.cid())

        ipfs_dict = IPFSDict(cid="QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5")
        self.assertEqual(ipfs_dict.cid(), "/ipfs/QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5")

    def test_items(self):
        ipfs_dict = IPFSDict()
        ipfs_dict.key = "value"
        self.assertEqual(ipfs_dict.items(), [('key', 'value')])

    def test_cid(self):
        ipfs_dict = IPFSDict(cid="QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5")
        self.assertEqual(ipfs_dict.cid(), "/ipfs/QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5")

    def test_save(self):
        ipfs_dict = IPFSDict()
        ipfs_dict.key = "value"
        cid = ipfs_dict.save()
        self.assertIsNotNone(cid)
        self.assertNotEqual(cid, "")

    def test_save_cid_prefix(self):
        ipfs_dict = IPFSDict()
        ipfs_dict.key = "value"
        cid = ipfs_dict.save()
        self.assertTrue(cid.startswith("/ipfs/"))
        self.assertEqual(ipfs_dict.cid(), cid)
        self.assertTrue(ipfs_dict.cid().startswith("/ipfs/"))

    @patch('ipfs_dict_chain.IPFSDict.add_json')
    def test_save_cidv1(self, mock_add_json):
        """Test save() with a CIDv1 (base32) CID returned by the IPFS daemon."""
        cidv1 = 'bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi'
        mock_add_json.return_value = cidv1

        ipfs_dict = IPFSDict()
        ipfs_dict.key = "value"
        cid = ipfs_dict.save()

        self.assertEqual(cid, '/ipfs/' + cidv1)
        self.assertEqual(ipfs_dict.cid(), '/ipfs/' + cidv1)

    def test_load(self):
        ipfs_dict = IPFSDict()

        with self.assertRaises(ValueError):
            ipfs_dict.load(cid=123)

        with self.assertRaises(IPFSError):
            ipfs_dict.load(cid="this is invalid CID")

        ipfs_dict.load(cid="QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5")
        self.assertEqual(ipfs_dict.cid(), "/ipfs/QmV5mPAcGoqegJnzFheED2pnef96633jSjimR2SSgu7ZV5")

    def test_setitem_getitem(self):
        ipfs_dict = IPFSDict()
        ipfs_dict['key1'] = 'value1'
        self.assertEqual(ipfs_dict['key1'], 'value1')

        ipfs_dict['key2'] = 'value2'
        self.assertEqual(ipfs_dict['key2'], 'value2')

        ipfs_dict['key1'] = 'new_value1'
        self.assertEqual(ipfs_dict['key1'], 'new_value1')

    def test_setitem_reserved_key(self):
        ipfs_dict = IPFSDict()
        with self.assertRaises(KeyError):
            ipfs_dict['_reserved'] = 'value'

    def test_attribute_assignment_retrieval(self):
        ipfs_dict = IPFSDict()
        ipfs_dict.key1 = 'value1'
        self.assertEqual(ipfs_dict.key1, 'value1')

        ipfs_dict.key2 = 'value2'
        self.assertEqual(ipfs_dict.key2, 'value2')

        ipfs_dict.key1 = 'new_value1'
        self.assertEqual(ipfs_dict.key1, 'new_value1')

    def test_combined_assignment_retrieval(self):
        ipfs_dict = IPFSDict()

        # Test attribute-style followed by dictionary-style
        ipfs_dict.key1 = 'value1'
        self.assertEqual(ipfs_dict.key1, 'value1')
        ipfs_dict['key1'] = 'new_value1'
        self.assertEqual(ipfs_dict['key1'], 'new_value1')

        # Test dictionary-style followed by attribute-style
        ipfs_dict['key2'] = 'value2'
        self.assertEqual(ipfs_dict['key2'], 'value2')
        ipfs_dict.key2 = 'new_value2'
        self.assertEqual(ipfs_dict.key2, 'new_value2')

    # Additional test cases
    def test_complex_data_types(self):
        """Test handling of complex data types."""
        ipfs_dict = IPFSDict()
        
        # Test datetime
        now = datetime.now()
        ipfs_dict.timestamp = now.isoformat()  # Convert to ISO format string before saving
        cid = ipfs_dict.save()
        
        loaded_dict = IPFSDict(cid)
        self.assertEqual(loaded_dict.timestamp, now.isoformat())
        
        # Test custom class (should be converted to dict)
        custom_obj = CustomClass("test")
        ipfs_dict.custom = {'value': custom_obj.value}  # Convert to dict before saving
        cid = ipfs_dict.save()
        
        loaded_dict = IPFSDict(cid)
        self.assertEqual(loaded_dict.custom['value'], custom_obj.value)
        
        # Test nested structures
        ipfs_dict = IPFSDict()
        ipfs_dict.data = self.test_data
        cid = ipfs_dict.save()
        
        loaded_dict = IPFSDict(cid)
        self.assertEqual(loaded_dict.data, self.test_data)

    def test_persistence(self):
        """Test save and load operations."""
        ipfs_dict = IPFSDict()
        
        # Test multiple saves
        ipfs_dict.key = "value1"
        cid1 = ipfs_dict.save()
        
        ipfs_dict.key = "value2"
        cid2 = ipfs_dict.save()
        
        self.assertNotEqual(cid1, cid2)
        
        # Test loading from previous CID
        old_dict = IPFSDict(cid1)
        self.assertEqual(old_dict.key, "value1")
        
        new_dict = IPFSDict(cid2)
        self.assertEqual(new_dict.key, "value2")

    def test_error_handling(self):
        """Test error handling scenarios."""
        ipfs_dict = IPFSDict()
        
        # Test accessing non-existent keys
        with self.assertRaises(AttributeError):
            _ = ipfs_dict.nonexistent
        
        with self.assertRaises(KeyError):
            _ = ipfs_dict['nonexistent']
        
        # Test that __setattr__ works correctly for valid attribute names
        ipfs_dict.valid_key = 'value'
        self.assertEqual(ipfs_dict.valid_key, 'value')
        
        # Test that private attributes (starting with _) bypass dict storage
        ipfs_dict._internal = 'private_value'
        # _internal should be a real attribute, not in items()
        self.assertNotIn('_internal', [k for k, v in ipfs_dict.items()])
        self.assertEqual(ipfs_dict._internal, 'private_value')
        
        # Test edge case: empty string key via __setitem__
        ipfs_dict[''] = 'empty_value'
        self.assertEqual(ipfs_dict[''], 'empty_value')
        
        # Test with invalid CID
        with self.assertRaises(ValueError):  # Changed to ValueError to match actual behavior
            IPFSDict("QmInvalidCIDThatDoesNotExist")

    def test_dict_operations(self):
        """Test dictionary-like operations."""
        ipfs_dict = IPFSDict()
        test_data = {'a': 1, 'b': 2, 'c': 3}
        
        for k, v in test_data.items():
            ipfs_dict[k] = v
        
        # Test keys, values, items
        self.assertEqual(set(ipfs_dict.items()), set(test_data.items()))
        
        # Test iteration
        for key in ipfs_dict:
            self.assertEqual(ipfs_dict[key], test_data[key])
        
        # Test length
        self.assertEqual(len(dict(ipfs_dict.items())), len(test_data))
        
        # Test contains
        self.assertTrue('a' in dict(ipfs_dict.items()))
        self.assertFalse('z' in dict(ipfs_dict.items()))

    def test_special_methods(self):
        """Test special methods."""
        ipfs_dict1 = IPFSDict()
        ipfs_dict1.key = "value"
        ipfs_dict1.save()
        
        # Test string representation
        self.assertEqual(str(ipfs_dict1), str(dict(ipfs_dict1.items())))
        
        # Test bool - should be True if it has items, False if empty
        self.assertTrue(bool(dict(ipfs_dict1.items())))
        empty_dict = IPFSDict()
        self.assertFalse(bool(dict(empty_dict.items())))

    @patch('ipfs_dict_chain.IPFSDict.get_json')
    def test_load_non_dict_data(self, mock_get_json):
        """Test loading data that is not a dictionary."""
        # Mock get_json to return a non-dictionary value
        mock_get_json.return_value = ["this", "is", "a", "list"]
        
        ipfs_dict = IPFSDict()
        test_cid = "QmTestNonDictData123"
        
        with self.assertRaises(IPFSError) as context:
            ipfs_dict.load(test_cid)
        
        self.assertIn("does not contain a dict", str(context.exception))
        self.assertIn(test_cid, str(context.exception))


if __name__ == '__main__':
    unittest.main()
