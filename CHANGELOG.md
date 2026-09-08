# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `IPFSDict.load()` now clears all existing data before loading new data from IPFS. Previously, loading into an already-populated `IPFSDict` merged the new data with the existing data (leaving stale keys behind); it now fully replaces the existing data with the data loaded from IPFS.

### Fixed

- Fixed CID format inconsistency between `IPFSDict.__init__`, `IPFSDict.load()`, and `IPFSDict.save()` methods. `save()` now returns CIDs with the `/ipfs/` prefix, consistent with the format used during initialization and loading. This prevents chain data corruption caused by inconsistent CID formats.
- `IPFSDict.load()` now raises `TypeError` instead of `ValueError` when a non-string CID is passed.
