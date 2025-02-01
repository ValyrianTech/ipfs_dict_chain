import unittest
from datetime import datetime
from ipfs_dict_chain.IPFSDictChain import IPFSDictChain
from ipfs_dict_chain.IPFS import IPFSError


class TestIPFSDictChain(unittest.TestCase):

    def test_init(self):
        ipfs_dict_chain = IPFSDictChain()
        self.assertIsNotNone(ipfs_dict_chain)

    def test_save(self):
        ipfs_dict_chain = IPFSDictChain()
        ipfs_dict_chain['key'] = 'value'
        new_cid = ipfs_dict_chain.save()
        self.assertIsNotNone(new_cid)

    def test_changes(self):
        ipfs_dict_chain = IPFSDictChain()
        ipfs_dict_chain['key'] = 'value'
        ipfs_dict_chain.save()
        ipfs_dict_chain['key'] = 'new_value'
        ipfs_dict_chain.save()
        changes = ipfs_dict_chain.changes()
        self.assertEqual(changes, {'previous_cid': {'old': None, 'new': 'QmNqXUYiiNMFXKy5rYFfs1tFASH6kgMA4fA1JwRoGuam8D'}, 'key': {'old': 'value', 'new': 'new_value'}})

    def test_get_previous_states(self):
        ipfs_dict_chain = IPFSDictChain()
        ipfs_dict_chain['key'] = 'value'
        ipfs_dict_chain.save()
        dict1 = dict(ipfs_dict_chain.items())
        ipfs_dict_chain['key'] = 'new_value'
        ipfs_dict_chain.save()
        previous_states = ipfs_dict_chain.get_previous_states()
        self.assertEqual(previous_states, [dict1])

    def test_get_previous_cids(self):
        ipfs_dict_chain = IPFSDictChain()
        ipfs_dict_chain['key'] = 'value'
        cid1 = ipfs_dict_chain.save()
        ipfs_dict_chain['key'] = 'new_value'
        cid2 = ipfs_dict_chain.save()
        previous_cids = ipfs_dict_chain.get_previous_cids()
        self.assertEqual(previous_cids, [cid1])

    def test_multiple_state_changes(self):
        """Test multiple state changes and history tracking."""
        chain = IPFSDictChain()
        
        # Create a sequence of states
        states = []
        for i in range(5):
            chain.value = f"state_{i}"
            chain.counter = i
            cid = chain.save()
            states.append(dict(chain.items()))
        
        # Test depth-limited history
        self.assertEqual(len(chain.get_previous_states(max_depth=2)), 2)
        self.assertEqual(len(chain.get_previous_states(max_depth=3)), 3)
        
        # Verify state order (states are stored newest to oldest)
        previous_states = chain.get_previous_states(max_depth=3)
        for i, state in enumerate(previous_states):
            expected_state = 3 - i
            self.assertEqual(state['value'], f"state_{expected_state}")
            self.assertEqual(state['counter'], expected_state)

    def test_nested_data_changes(self):
        """Test tracking changes in nested data structures."""
        chain = IPFSDictChain()
        
        # Initial nested structure
        chain.data = {
            'list': [1, 2, 3],
            'dict': {'a': 1, 'b': 2},
            'nested': {'x': {'y': 'z'}}
        }
        chain.save()
        
        # Modify nested structure
        chain.data['list'].append(4)
        chain.data['dict']['c'] = 3
        chain.data['nested']['x']['new'] = 'value'
        chain.save()
        
        # Verify changes
        changes = chain.changes()
        self.assertIn('data', changes)
        self.assertNotEqual(changes['data']['old'], changes['data']['new'])

    def test_empty_chain_operations(self):
        """Test operations on empty chain."""
        chain = IPFSDictChain()
        
        # Test empty state operations
        self.assertEqual(chain.get_previous_states(), [])
        self.assertEqual(chain.get_previous_cids(), [])
        self.assertEqual(chain.changes(), {'previous_cid': {'new': None}})  # Chain always tracks previous_cid
        
        # Save empty state
        cid = chain.save()
        self.assertIsNotNone(cid)
        
        # Load empty state (will contain previous_cid as None)
        loaded_chain = IPFSDictChain(cid)
        state = dict(loaded_chain.items())
        self.assertEqual(len(state), 1)  # Only previous_cid
        self.assertIsNone(state['previous_cid'])

    def test_complex_data_serialization(self):
        """Test serialization of complex data types."""
        chain = IPFSDictChain()
        
        # Test with datetime
        now = datetime.now()
        chain.timestamp = now.isoformat()
        
        # Test with None values
        chain.none_value = None
        
        # Test with mixed types
        chain.mixed = {
            'string': 'text',
            'int': 42,
            'float': 3.14,
            'bool': True,
            'none': None,
            'list': [1, 'two', 3.0, None],
            'dict': {'a': 1, 'b': 'two'}
        }
        
        # Save and reload
        cid = chain.save()
        loaded_chain = IPFSDictChain(cid)
        
        # Verify all data types are preserved
        self.assertEqual(loaded_chain.timestamp, now.isoformat())
        self.assertIsNone(loaded_chain.none_value)
        self.assertEqual(loaded_chain.mixed['int'], 42)
        self.assertEqual(loaded_chain.mixed['float'], 3.14)
        self.assertTrue(loaded_chain.mixed['bool'])
        self.assertEqual(len(loaded_chain.mixed['list']), 4)
        self.assertEqual(loaded_chain.mixed['dict']['b'], 'two')

    def test_state_branching(self):
        """Test creating and managing state branches."""
        # Create main chain
        main_chain = IPFSDictChain()
        main_chain.value = "main_1"
        cid1 = main_chain.save()
        main_chain.value = "main_2"
        main_chain.save()
        
        # Create branch from first state
        branch_chain = IPFSDictChain(cid1)
        self.assertEqual(branch_chain.value, "main_1")
        
        # Modify branch
        branch_chain.value = "branch_1"
        branch_cid = branch_chain.save()
        
        # Verify branch and main chain are different
        self.assertNotEqual(branch_chain.cid(), main_chain.cid())
        self.assertEqual(branch_chain.value, "branch_1")
        self.assertEqual(main_chain.value, "main_2")


if __name__ == '__main__':
    unittest.main()