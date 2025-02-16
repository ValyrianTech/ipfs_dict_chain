import pytest
from ipfs_dict_chain.CID import CID


def test_init_valid():
    cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert cid.value == '/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o'

def test_init_invalid():
    with pytest.raises(ValueError):
        CID('this cid is invalid')

def test_str():
    cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert str(cid) == '/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o'

def test_repr():
    cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert repr(cid) == "CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')"

def test_eq():
    cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    cid2 = CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert cid1 == cid2

def test_hash():
    cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    cid2 = CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert hash(cid1) == hash(cid2)

def test_short():
    cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert cid.short() == 'QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o'

def test_long():
    cid = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    assert cid.long() == '/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o'

def test_init_edge_cases():
    """Test initialization with edge cases."""
    # Test with minimum valid CID
    min_cid = "Qm" + "1" * 44  # Base58 minimum length
    cid_min = CID(min_cid)
    assert min_cid in str(cid_min)

@pytest.mark.parametrize("invalid_input", [
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
])
def test_init_invalid_types(invalid_input):
    """Test initialization with invalid types."""
    try:
        CID(invalid_input)
        pytest.fail(f"Expected ValueError for input: {invalid_input}")
    except (ValueError, TypeError):
        # Both ValueError and TypeError are acceptable for invalid inputs
        pass

def test_equality_extended():
    """Test extended equality comparisons."""
    cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    cid2 = CID('/ipfs/QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    cid3 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5p")  # Different last char

    # Test inequality with different CID
    assert cid1 != cid3
    assert cid1 != cid3

    # Test comparison with non-CID objects
    assert cid1 != str(cid1)
    assert cid1 != None
    assert cid1 != 123
    assert cid1 != str(cid1)
    assert cid1 != None

def test_collection_usage():
    """Test using CID in various Python collections."""
    cid1 = CID('QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o')
    cid2 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5p")  # Different last char
    cid3 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5q")  # Different last char

    # Test in list
    cid_list = [cid1, cid2, cid3]
    assert len(cid_list) == 3
    assert cid1 in cid_list

    # Test in set
    cid_set = {cid1, cid2, cid1, cid3}  # Duplicate cid1
    assert len(cid_set) == 3
    assert cid2 in cid_set

    # Test in dictionary
    cid_dict = {cid1: "first", cid2: "second", cid3: "third"}
    assert len(cid_dict) == 3
    assert cid_dict[cid1] == "first"

    # Test sorting
    sorted_cids = sorted(cid_set, key=lambda x: x.value)
    assert len(sorted_cids) == 3
    assert sorted_cids[0] == min(sorted_cids, key=lambda x: x.value)
