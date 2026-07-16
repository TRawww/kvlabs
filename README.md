# KVLabs iOS Jailbreak Repo

APT/Cydia/Sileo/Zebra repo for KVLabs jailbreak and iOS runtime packages.

Once GitHub Pages is enabled, add this repo in Cydia/Sileo/Zebra:

```text
https://<github-user>.github.io/kvlabs/
```

## Layout

- `debs/` — put `.deb` packages here.
- `Packages` / `Packages.gz` / `Release` — generated repo indexes.
- `scripts/build_repo.py` — regenerates package indexes.

## Build repo index

```bash
python3 scripts/build_repo.py
```

Commit the generated files.

## Management

See [`MANAGEMENT.md`](MANAGEMENT.md) for adding, updating, removing, validating, and publishing packages.
