import unittest
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


if __name__ == '__main__':
    unittest.main()