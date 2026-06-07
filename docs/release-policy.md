# Release Policy

This repository distributes public data artifacts for Gene-Disease Evidence Index.

## Repository Boundary

- Production code lives in a private repository.
- This repository contains public release artifacts only.
- The rendered site should read from or mirror these artifacts.
- A paper should cite a fixed release, not the live rendered site.

## Development Releases

Development releases use `-dev` suffixes and exist only to validate package shape.
They should not be cited as scientific evidence.

## Paper-Grade Releases

A paper-grade release should include:

- release metadata
- source manifest
- schema version
- stable gene records
- stable disease records
- evidence-backed association objects
- evidence rows
- review artifacts
- changelog or release diff
- downloadable archive
- citation metadata
- DOI-backed mirror when appropriate

