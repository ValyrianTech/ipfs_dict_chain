import pytest
from ipfs_dict_chain.CID import CID

BASE32_LOWER_CID = 'bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi'
BASE32_UPPER_CID = 'BAFYBEIGDYRZT5SFP7UDM7HU76UH7Y26NF3EFUYLQABF3OCLGTQY55FBZDI'
BASE16_LOWER_CID = 'f01701220c3c4733ec8affd06cf9e9ff50ffc6bcd2ec85a6170004bb709669c31de94391a'
BASE16_UPPER_CID = 'F01701220C3C4733EC8AFFD06CF9E9FF50FFC6BCD2EC85A6170004BB709669C31DE94391A'
BASE58_CID = 'zQmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o'
BASE58_FLICKR_CID = '9QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o'
BASE36_UPPER_CID = 'U0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE36_LOWER_CID = 'V0123456789abcdefghijklmnopqrstuvwxyz'


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
    cid3 = CID("QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5p")  # Different last char

    # Test inequality with different CID
    assert cid1 != cid3
    assert cid1 != cid3

    # Test comparison with non-CID objects
    assert cid1 != str(cid1)
    assert cid1 is not None
    assert cid1 != 123
    assert cid1 != str(cid1)
    assert cid1 is not None

def test_short_cid():
    """Test that a CID too short raises ValueError."""
    with pytest.raises(ValueError):
        CID('Qm12345')


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


@pytest.mark.parametrize("valid_cid", [
    BASE32_LOWER_CID,
    BASE32_UPPER_CID,
    BASE16_LOWER_CID,
    BASE16_UPPER_CID,
    BASE58_CID,
    BASE58_FLICKR_CID,
    BASE36_UPPER_CID,
    BASE36_LOWER_CID,
])
def test_cidv1_valid(valid_cid):
    """Test that valid CIDv1 CIDs in all multibase formats are accepted."""
    cid = CID(valid_cid)
    assert cid.value == f'/ipfs/{valid_cid}'


@pytest.mark.parametrize("valid_cid", [
    BASE32_LOWER_CID,
    BASE32_UPPER_CID,
    BASE16_LOWER_CID,
    BASE16_UPPER_CID,
    BASE58_CID,
    BASE58_FLICKR_CID,
    BASE36_UPPER_CID,
    BASE36_LOWER_CID,
])
def test_cidv1_valid_with_ipfs_prefix(valid_cid):
    """Test that the /ipfs/ prefix is accepted for CIDv1 CIDs."""
    cid = CID(f'/ipfs/{valid_cid}')
    assert cid.value == f'/ipfs/{valid_cid}'


@pytest.mark.parametrize("invalid_cid", [
    'b1',       # '1' is not a valid base32 lower character
    'b0',       # '0' is not a valid base32 lower character
    'bZ',       # uppercase is not a valid base32 lower character
    'Ba',       # lowercase is not a valid base32 upper character
    'B1',       # '1' is not a valid base32 upper character
    'fG',       # 'G' is not a valid base16 lower character
    'Fg',       # 'g' is not a valid base16 upper character
    'z0',       # '0' is not a valid base58 character
    'zO',       # 'O' is not a valid base58 character
    'zI',       # 'I' is not a valid base58 character
    'zl',       # 'l' is not a valid base58 character
    '90',       # '0' is not a valid base58flickr character
    '9O',       # 'O' is not a valid base58flickr character
    '9I',       # 'I' is not a valid base58flickr character
    '9l',       # 'l' is not a valid base58flickr character
    'Ua',       # lowercase is not a valid base36 upper character
    'VA',       # uppercase is not a valid base36 lower character
    BASE32_LOWER_CID + '1',
    BASE16_LOWER_CID + 'g',
])
def test_cidv1_invalid(invalid_cid):
    """Test that CIDv1 CIDs with invalid characters are rejected."""
    with pytest.raises(ValueError):
        CID(invalid_cid)


def test_cidv1_methods():
    """Test CID class methods with a CIDv1 value."""
    cid = CID(BASE32_LOWER_CID)

    assert str(cid) == f'/ipfs/{BASE32_LOWER_CID}'
    assert repr(cid) == f"CID('/ipfs/{BASE32_LOWER_CID}')"
    assert cid == CID(f'/ipfs/{BASE32_LOWER_CID}')
    assert hash(cid) == hash(CID(f'/ipfs/{BASE32_LOWER_CID}'))
    assert cid.short() == BASE32_LOWER_CID
    assert cid.long() == f'/ipfs/{BASE32_LOWER_CID}'
