import unittest
from ipfs_dict_chain.CID import CID


class TestCID(unittest.TestCase):
    """Test cases for the CID (Content Identifier) class."""

    # Original test cases
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

    # Additional test cases
    def test_init_edge_cases(self):
        """Test initialization with edge cases."""
        # Test with minimum valid CID
        min_cid = "Qm" + "1" * 44  # Base58 minimum length
        cid_min = CID(min_cid)
        self.assertTrue(min_cid in str(cid_min))

        # Test with maximum valid CID
        max_cid = "Qm" + "z" * 44  # Base58 maximum length
        cid_max = CID(max_cid)
        self.assertTrue(max_cid in str(cid_max))

        # Test with all Base58 characters
        base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base58_cid = "Qm" + base58_chars[:44]  # Use first 44 chars for valid length
        cid_base58 = CID(base58_cid)
        self.assertTrue(base58_cid in str(cid_base58))

    def test_init_invalid_types(self):
        """Test initialization with invalid types."""
        invalid_inputs = [
            # Non-string inputs
            None,
            123,
            3.14,
            True,
            [],
            {},
            # Invalid string formats
            "",
            " ",
            "  ",
            # Invalid characters
            "QmInvalidCharacters!@#$%^&*()",
            "QmT78" + "0" * 40,  # Invalid Base58 character '0'
            "QmT78" + "O" * 40,  # Invalid Base58 character 'O'
            "QmT78" + "I" * 40,  # Invalid Base58 character 'I'
            "QmT78" + "l" * 40,  # Invalid Base58 character 'l',
            # Invalid prefix
            "/notipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o",
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(msg=f"Testing invalid input: {invalid_input}"):
                try:
                    CID(invalid_input)
                    self.fail(f"Expected ValueError for input: {invalid_input}")
                except (ValueError, TypeError):
                    # Both ValueError and TypeError are acceptable for invalid inputs
                    pass

    def test_equality_extended(self):
        """Test extended equality comparisons."""
        cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        cid2 = CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        cid3 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5p")  # Different last char

        # Test inequality with different CID
        self.assertNotEqual(cid1, cid3)
        self.assertTrue(cid1 != cid3)

        # Test comparison with non-CID objects
        self.assertNotEqual(cid1, str(cid1))
        self.assertNotEqual(cid1, None)
        self.assertNotEqual(cid1, 123)
        self.assertTrue(cid1 != str(cid1))
        self.assertTrue(cid1 != None)

    def test_collection_usage(self):
        """Test using CID in various Python collections."""
        cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
        cid2 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5p")  # Different last char
        cid3 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5q")  # Different last char

        # Test in list
        cid_list = [cid1, cid2, cid3]
        self.assertEqual(len(cid_list), 3)
        self.assertIn(cid1, cid_list)

        # Test in set
        cid_set = {cid1, cid2, cid1, cid3}  # Duplicate cid1
        self.assertEqual(len(cid_set), 3)
        self.assertIn(cid2, cid_set)

        # Test in dictionary
        cid_dict = {cid1: "first", cid2: "second", cid3: "third"}
        self.assertEqual(len(cid_dict), 3)
        self.assertEqual(cid_dict[cid1], "first")

        # Test sorting
        sorted_cids = sorted(cid_set, key=lambda x: x.value)
        self.assertEqual(len(sorted_cids), 3)
        self.assertEqual(sorted_cids[0], min(sorted_cids, key=lambda x: x.value))


if __name__ == '__main__':
    unittest.main()
