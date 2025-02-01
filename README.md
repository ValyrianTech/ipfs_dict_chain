# ipfs_dict_chain

ipfs_dict_chain is a Python package that provides IPFSDict and IPFSDictChain objects, which are dictionary-like data structures that store their state on IPFS and keep track of changes, basically creating a mini-blockchain of dicts on IPFS for efficient and secure data management.

## Requirements

- Python >= 3.10
- An IPFS node
- aioipfs >= 0.6.3
- multiaddr >= 0.0.9

## Installation

To install the ipfs_dict_chain package, run the following command:

```bash
pip install ipfs_dict_chain
```

## Usage

If your IPFS node is not running on localhost on the default port, you must first connect to your IPFS node:

```python
from ipfs_dict_chain.IPFS import connect

connect(host='127.0.0.1', port=5001)
```

### IPFSDict

IPFSDict is a dictionary-like object that stores its data on IPFS. Here's an example of how to use IPFSDict:

```python
from ipfs_dict_chain.IPFSDict import IPFSDict

my_dict = IPFSDict()

# Add data to the dictionary, you can use both dot notation and bracket notation
my_dict.my_key1 = 'value1'
my_dict['my_key2'] = 'value2'

# Save the dictionary to IPFS
cid = my_dict.save()

# Load the dictionary from IPFS
loaded_dict = IPFSDict(cid=cid)

# Access the data
print(loaded_dict.my_key1)  # Output: 'value1'
```

### IPFSDictChain

IPFSDictChain is a dictionary-like data structure that stores its state on IPFS and keeps track of changes. Here's an example of how to use IPFSDictChain:

```python
from ipfs_dict_chain.IPFSDictChain import IPFSDictChain

my_chain = IPFSDictChain()

# Add data to the dictionary, you can use both dot notation and bracket notation
my_chain.my_key1 = 'value1'
my_chain['my_key2'] = 'value2'

# Save the current state of the dictionary to IPFS
cid1 = my_chain.save()

my_chain.my_key1 = 'value1_changed'
cid2 = my_chain.save()

# Load the dictionary from IPFS
loaded_chain = IPFSDictChain(cid=cid2)

# Access the data
print(loaded_chain.my_key1)  # Output: 'value1_changed'

# Get the changes between the current state and the previous state
changes = loaded_chain.changes()
print(changes)  # Output: {'previous_cid': {'old': None, 'new': 'QmSdydVMD2E7taf42gwQNhakBAc379u8y9X4Kbyoig36Fs'}, 'my_key1': {'old': 'value1', 'new': 'value1_changed'}}

# Get the previous states of the dictionary
previous_states = loaded_chain.get_previous_states()
print(previous_states)  # Output: [{'previous_cid': None, 'my_key1': 'value1', 'my_key2': 'value2'}]

# Get the previous CIDs of the dictionary
previous_cids = loaded_chain.get_previous_cids()
print(previous_cids)  # Output: ['QmSdydVMD2E7taf42gwQNhakBAc379u8y9X4Kbyoig36Fs']
```

## Contributing

If you'd like to contribute to the ipfs_dict_chain package, please submit a pull request, issue, or feature request on the project's GitHub repository.

## License

This package is released under the [MIT License](LICENSE).

## Authors

- Wouter Glorieux - [Twitter](https://twitter.com/WouterGlorieux)
- Serendipity - AI Assistant
