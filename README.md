# ipfs_dict_chain

ipfs_dict_chain is a Python package that provides IPFSDict and IPFSDictChain objects, which are dictionary-like data structures that store their state on IPFS and keep track of changes, basically creating a mini-blockchain of dicts on IPFS for efficient and secure data management.

## Requirements

- Python 3.10
- An IPFS node

## Installation

To install the ipfs_dict_chain package, run the following command:

```bash
pip install ipfs_dict_chain
```

## Usage

### IPFSDict

IPFSDict is a dictionary-like object that stores its data on IPFS. Here's an example of how to use IPFSDict:

```python
from ipfs_dict_chain import IPFSDict

my_dict = IPFSDict()

# Add data to the dictionary
my_dict['key'] = 'value'

# Save the dictionary to IPFS
cid = my_dict.save()

# Load the dictionary from IPFS
loaded_dict = IPFSDict(cid=cid)

# Access the data
print(loaded_dict['key'])  # Output: 'value'
```

### IPFSDictChain

IPFSDictChain is a dictionary-like data structure that stores its state on IPFS and keeps track of changes. Here's an example of how to use IPFSDictChain:

```python
from ipfs_dict_chain import IPFSDictChain

my_chain = IPFSDictChain()

# Add data to the dictionary
my_chain['key'] = 'value'

# Save the current state of the dictionary to IPFS
cid = my_chain.save()

# Load the dictionary from IPFS
loaded_chain = IPFSDictChain(cid=cid)

# Access the data
print(loaded_chain['key'])  # Output: 'value'

# Get the changes between the current state and the previous state
changes = loaded_chain.changes()

# Get the previous states of the dictionary
previous_states = loaded_chain.get_previous_states()

# Get the previous CIDs of the dictionary
previous_cids = loaded_chain.get_previous_cids()
```

## Contributing

If you'd like to contribute to the ipfs_dict_chain package, please submit a pull request, issue, or feature request on the project's GitHub repository.

## License

This package is released under the [MIT License](LICENSE).

## Authors

- Wouter Glorieux - [Twitter](https://twitter.com/WouterGlorieux)
- Serendipity - AI Assistant
