.. ipfs_dict_chain documentation master file, created by
   sphinx-quickstart on Sun Feb  2 10:42:14 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ipfs_dict_chain documentation
=============================

Welcome to ipfs_dict_chain's documentation!
======================================

``ipfs_dict_chain`` is a Python package that provides dictionary-like data structures that store their state on IPFS and track changes.

Features
--------

* Store dictionary data on IPFS
* Track state changes in a chain-like structure
* Support for both dot notation and bracket notation
* Automatic IPFS content addressing
* History tracking and state retrieval

Requirements
-----------

* Python >= 3.10
* IPFS node
* aioipfs >= 0.6.3
* multiaddr >= 0.0.9

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   contributing
   changelog

API Documentation
----------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/ipfs_dict_chain.CID
   api/ipfs_dict_chain.IPFS
   api/ipfs_dict_chain.IPFSDict
   api/ipfs_dict_chain.IPFSDictChain

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
