# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fixed CID format inconsistency between `IPFSDict.__init__`, `IPFSDict.load()`, and `IPFSDict.save()` methods. `save()` now returns CIDs with the `/ipfs/` prefix, consistent with the format used during initialization and loading. This prevents chain data corruption caused by inconsistent CID formats.
