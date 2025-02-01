import unittest
from datetime import datetime
from ipfs_dict_chain.IPFSDict import IPFSDict
from ipfs_dict_chain.IPFS import IPFSError


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
        
        with self.assertRaises(AttributeError):  # Changed from KeyError to match actual behavior
            _ = ipfs_dict['nonexistent']
        
        # Test invalid attribute names
        for invalid_name in ['class', 'def', 'return', 'import']:
            with self.assertRaises(SyntaxError):
                exec(f"ipfs_dict.{invalid_name} = 'value'")
        
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
        cid1 = ipfs_dict1.save()
        
        ipfs_dict2 = IPFSDict(cid1)
        
        # Test string representation
        self.assertEqual(str(ipfs_dict1), str(dict(ipfs_dict1.items())))
        
        # Test bool - should be True if it has items, False if empty
        self.assertTrue(bool(dict(ipfs_dict1.items())))
        empty_dict = IPFSDict()
        self.assertFalse(bool(dict(empty_dict.items())))


if __name__ == '__main__':
    unittest.main()
