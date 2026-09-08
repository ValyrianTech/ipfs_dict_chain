import unittest
from datetime import datetime
from unittest.mock import patch

from ipfs_dict_chain.IPFS import IPFSError
from ipfs_dict_chain.IPFSDictChain import IPFSDictChain


class TestIPFSDictChain(unittest.TestCase):

    def test_init(self):
        ipfs_dict_chain = IPFSDictChain()
        self.assertIsNotNone(ipfs_dict_chain)

    def test_save(self):
        ipfs_dict_chain = IPFSDictChain()
        ipfs_dict_chain['key'] = 'value'
        new_cid = ipfs_dict_chain.save()
        self.assertIsNotNone(new_cid)

    @patch('ipfs_dict_chain.IPFSDict.add_json')
    def test_save_cidv1(self, mock_add_json):
        """Test save() with a CIDv1 (base32) CID returned by the IPFS daemon."""
        cidv1 = 'bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi'
        mock_add_json.return_value = cidv1

        chain = IPFSDictChain()
        chain['key'] = 'value'
        new_cid = chain.save()

        self.assertEqual(new_cid, '/ipfs/' + cidv1)
        self.assertEqual(chain.cid(), '/ipfs/' + cidv1)
        self.assertTrue(chain.cid().startswith('/ipfs/'))

    def test_previous_cid_format_consistency(self):
        chain = IPFSDictChain()
        chain['key'] = 'value1'
        cid1 = chain.save()
        chain['key'] = 'value2'
        cid2 = chain.save()

        self.assertTrue(cid1.startswith('/ipfs/'))
        self.assertTrue(chain.previous_cid.startswith('/ipfs/'))

        loaded_chain = IPFSDictChain(cid2)
        self.assertTrue(loaded_chain.previous_cid.startswith('/ipfs/'))
        self.assertEqual(loaded_chain.previous_cid, cid1)

    def test_changes(self):
        ipfs_dict_chain = IPFSDictChain()
        ipfs_dict_chain['key'] = 'value'
        ipfs_dict_chain.save()
        ipfs_dict_chain['key'] = 'new_value'
        ipfs_dict_chain.save()
        changes = ipfs_dict_chain.changes()
        self.assertEqual(changes, {'key': {'old': 'value', 'new': 'new_value'}})

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
        ipfs_dict_chain.save()
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
            chain.save()
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
        self.assertEqual(chain.changes(), {})  # No changes when chain is empty
        
        # Save empty state
        cid = chain.save()
        self.assertIsNotNone(cid)
        
        # Load empty state (will contain previous_cid as None)
        loaded_chain = IPFSDictChain(cid)
        state = dict(loaded_chain.items())
        self.assertEqual(len(state), 1)  # Empty state contains previous_cid
        self.assertIsNone(state['previous_cid'])  # previous_cid is None for the first state

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
        branch_chain.save()
        
        # Verify branch and main chain are different
        self.assertNotEqual(branch_chain.cid(), main_chain.cid())
        self.assertEqual(branch_chain.value, "branch_1")
        self.assertEqual(main_chain.value, "main_2")

    def test_changes_ipfs_error(self):
        """Test changes when previous state loading raises IPFSError."""
        chain = IPFSDictChain()
        chain['key'] = 'value'
        chain.save()
        chain['key'] = 'new_value'
        chain.save()
        with patch('ipfs_dict_chain.IPFSDictChain.get_json', side_effect=IPFSError("Test error")):
            changes = chain.changes()
        self.assertEqual(changes, {'key': {'new': 'new_value'}})

    def test_changes_deleted_key(self):
        """Test changes detects deleted keys."""
        chain = IPFSDictChain()
        chain['a'] = 'value_a'
        chain.save()
        del chain['a']
        chain.save()
        changes = chain.changes()
        self.assertEqual(changes, {'a': {'old': 'value_a', 'new': None}})

    def test_changes_new_key(self):
        """Test changes detects newly added keys."""
        chain = IPFSDictChain()
        chain['a'] = 'value_a'
        chain.save()
        chain['b'] = 'value_b'
        chain.save()
        changes = chain.changes()
        self.assertEqual(changes, {'b': {'new': 'value_b'}})

    def test_get_previous_cids_ipfs_error(self):
        """Test get_previous_cids handles IPFSError in _get_previous_cid_for."""
        chain = IPFSDictChain()
        chain['key'] = 'value'
        chain.save()
        chain['key'] = 'new_value'
        chain.save()
        with patch('ipfs_dict_chain.IPFSDict.get_json', side_effect=IPFSError("Test error")):
            cids = chain.get_previous_cids()
        self.assertEqual(len(cids), 1)

    def test_get_previous_states_ipfs_error(self):
        """Test get_previous_states handles IPFSError when loading a state."""
        chain = IPFSDictChain()
        chain['key'] = 'value'
        chain.save()
        chain['key'] = 'new_value'
        chain.save()
        with patch('ipfs_dict_chain.IPFSDict.get_json', side_effect=IPFSError("Test error")):
            states = chain.get_previous_states()
        self.assertEqual(states, [])

    def test_get_previous_cids_max_depth(self):
        """Test get_previous_cids with max_depth and verify depth increment."""
        chain = IPFSDictChain()
        for i in range(5):
            chain['value'] = f"state_{i}"
            chain.save()
        cids = chain.get_previous_cids(max_depth=2)
        self.assertEqual(len(cids), 2)
        cids = chain.get_previous_cids(max_depth=3)
        self.assertEqual(len(cids), 3)


if __name__ == '__main__':
    unittest.main()