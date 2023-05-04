import unittest
from ipfs_dict_chain.IPFSDict import IPFSDict
from ipfs_dict_chain.IPFS import IPFSError


class TestIPFSDict(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
