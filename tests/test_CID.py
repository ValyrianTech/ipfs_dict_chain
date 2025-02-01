import unittest
from ipfs_dict_chain.CID import CID


class TestCID(unittest.TestCase):

    def test_init_valid(self):
        cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(cid.value, '/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')

    def test_init_invalid(self):
        with self.assertRaises(ValueError):
            CID('this cid is invalid')

    def test_str(self):
        cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(str(cid), '/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')

    def test_repr(self):
        cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(repr(cid), "CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')")

    def test_eq(self):
        cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        cid2 = CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(cid1, cid2)

    def test_hash(self):
        cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        cid2 = CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(hash(cid1), hash(cid2))

    def test_short(self):
        cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(cid.short(), 'QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')

    def test_long(self):
        cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        self.assertEqual(cid.long(), '/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')


if __name__ == '__main__':
    unittest.main()
