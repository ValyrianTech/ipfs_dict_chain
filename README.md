# ipfs_dict_chain

[![Tests](https://github.com/ValyrianTech/ipfs_dict_chain/actions/workflows/tests.yml/badge.svg)](https://github.com/ValyrianTech/ipfs_dict_chain/actions/workflows/tests.yml)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://valyriantech.github.io/ipfs_dict_chain/)
[![codecov](https://codecov.io/gh/ValyrianTech/ipfs_dict_chain/branch/main/graph/badge.svg)](https://codecov.io/gh/ValyrianTech/ipfs_dict_chain)
[![License](https://img.shields.io/github/license/ValyrianTech/ipfs_dict_chain)](https://github.com/ValyrianTech/ipfs_dict_chain/blob/main/LICENSE)

ipfs_dict_chain is a Python package that provides IPFSDict and IPFSDictChain objects, which are dictionary-like data structures that store their state on IPFS and keep track of changes, basically creating a mini-blockchain of dicts on IPFS for efficient and secure data management.

## Requirements

- Python >= 3.10
- An IPFS node
- aioipfs >= 0.6.3
- multiaddr >= 0.0.9

## Installation

To install the ipfs_dict_chain package, run the following command:

```bash
pip install ipfs-dict-chain
```

## Usage

By default, ipfs_dict_chain will attempt to connect to an IPFS node running on localhost (127.0.0.1) on port 5001. If your IPFS node is running with these default settings, you can start using the package immediately.

If your IPFS node is running on a different host or port, you must first connect to it using the `connect()` function:

```python
from ipfs_dict_chain.IPFS import connect

# Connect to a local IPFS node on a different port
connect(host='127.0.0.1', port=8080)

# Or connect to a remote IPFS node
connect(host='192.168.1.100', port=5001)
```

The `connect()` function will test the connection by attempting to add a small test object to IPFS. If the connection fails, it will raise an `IPFSError` with details about the connection failure.

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

## Development and Testing

To install development dependencies:

```bash
pip install -e ".[dev]"
```

To run tests with coverage:

```bash
pytest
```

This will:
- Run all tests in the `tests` directory
- Generate a coverage report in the terminal
- Create an HTML coverage report in the `htmlcov` directory

To view specific test coverage details:
```bash
# View coverage in terminal with missing lines
pytest --cov=ipfs_dict_chain --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=ipfs_dict_chain --cov-report=html
```

## Documentation

The documentation is built using Sphinx and can be found at [GitHub Pages](https://valyriantech.github.io/ipfs_dict_chain/).

To build the documentation locally:

1. Install the documentation dependencies:
   ```bash
   pip install sphinx sphinx-rtd-theme
   ```

2. Build the documentation:
   ```bash
   cd docs
   python -m sphinx.cmd.build -b html source build/html
   ```

The documentation will be available in `docs/build/html/index.html`.

## Contributing

If you'd like to contribute to the ipfs_dict_chain package, please submit a pull request, issue, or feature request on the project's GitHub repository.

## License

This package is released under the [MIT License](LICENSE).

## Authors

- Wouter Glorieux - [Twitter](https://twitter.com/WouterGlorieux)
- Serendipity - AI Assistant
