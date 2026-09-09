# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-09-09

### Changed (Breaking)

- **`IPFSDict` base class changed from `typing.Dict` to built-in `dict`**: Data keys are now stored as actual dict items instead of instance attributes in `__dict__`. This changes the internal data storage model fundamentally. Code that accessed `ipfs_dict.__dict__` directly will break.
- **`IPFSDict.load()` now clears all existing data before loading**: Previously, loading into an already-populated `IPFSDict` merged the new data with the existing data (leaving stale keys behind); it now fully replaces the existing data with the data loaded from IPFS.
- **`IPFSDict.save()` now returns CIDs with `/ipfs/` prefix**: Previously `save()` returned a bare CID; it now wraps the result through `CID().__str__()`, consistent with the format used during initialization and loading. Code expecting bare CIDs will receive `/ipfs/<cid>` instead.
- **`IPFSDict.load()` raises `TypeError` instead of `ValueError`** when a non-string CID is passed.
- **Underscore-prefixed keys are now rejected in `__setitem__`**: Using `d['_key'] = value` now raises `KeyError`. Keys starting with `_` are reserved for internal use.
- **`__getattribute__` gives class methods precedence over data keys**: Dot notation access (e.g. `my_dict.save`) now always returns the class method if one exists, rather than a data key with the same name. Accessing a genuinely missing attribute via dot notation raises `AttributeError` instead of `KeyError` or returning `None`.
- **`IPFSDictChain.__init__` extracts `previous_cid` from loaded data**: `previous_cid` is now a dict key stored in the dict, not an instance attribute set to `None` before loading. It is extracted from the loaded data after `super().__init__()`.
- **`IPFSDictChain.save()` persists `previous_cid` as part of the dict data**: Since `previous_cid` is now a dict key, it is serialized as part of `dict(self)` in `save()`. Previously it was an instance attribute and was never persisted — this is a bug fix that changes the stored data format.
- **`connect()` no longer modifies global `multi_address` on failure**: The global address is only updated after a successful connection test. Previously it was set before testing.
- **`connect()` wraps all connection errors in `IPFSError`**: Invalid host/port strings that previously raised `StringParseError` from `Multiaddr` now raise `IPFSError`.

### Fixed

- Fixed CID format inconsistency between `IPFSDict.__init__`, `IPFSDict.load()`, and `IPFSDict.save()` methods, preventing chain data corruption caused by inconsistent CID formats.
- Fixed CID validation regex to properly support CIDv0 (Base58, 46 chars) and CIDv1 (multiple multibase encodings). The old regex was too permissive.
- Fixed an issue where dictionary data keys could shadow `IPFSDict` class methods such as `save()`, `load()`, and `cid()` when accessed via dot notation.
- Fixed `IPFSDictChain.changes()` to properly detect key deletions (keys present in old state but absent in current state are now reported as `{'old': value, 'new': None}`).
- Fixed `IPFSDictChain.changes()` to filter out internal keys (`previous_cid`, underscore-prefixed) from change reports.
- Fixed `IPFSDict.items()` to filter underscore-prefixed keys consistently with `IPFSDictChain.changes()`.
- Fixed `IPFSDict.items()` crash with `IndexError` when dict contains an empty string key.
- Fixed module-level asyncio event loop leak: replaced per-call event loop creation/destruction with a shared global loop, properly closed at interpreter exit via `atexit`.
- Fixed `get_file_content()` to always close the IPFS client via `try/finally`.
- Fixed `_add_json()` to raise `IPFSError` when the IPFS response does not contain a `Hash`.
- Fixed `IPFSDictChain.get_previous_states()` and `get_previous_cids()` to use lightweight `get_json()` fetches instead of creating full `IPFSDictChain` instances, reducing redundant network calls.
- Fixed `IPFSDictChain.get_previous_states()` to filter out the internal `_cid` key from returned state dictionaries.
