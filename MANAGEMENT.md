# KVLabs repo management

KVLabs is a static APT repo hosted by GitHub Pages.

## URLs

- GitHub: `https://github.com/TRawww/kvlabs`
- Package repo: `https://trawww.github.io/kvlabs/`
- Local checkout: `/Users/traw/Desktop/AI-Projects/kvlabs`

Add repo URL to Cydia, Sileo, or Zebra:

```text
https://trawww.github.io/kvlabs/
```

## Add a package

1. Build or copy a `.deb` into:

```bash
/Users/traw/Desktop/AI-Projects/kvlabs/debs/
```

2. Rebuild repo index:

```bash
cd /Users/traw/Desktop/AI-Projects/kvlabs
python3 scripts/build_repo.py
```

3. Verify the package index contains the package:

```bash
grep -A20 '^Package:' Packages
```

4. Commit and push:

```bash
git add debs Packages Packages.gz Release
git commit -m "Add <package-name>"
git push
```

GitHub Pages serves the update from:

```text
https://trawww.github.io/kvlabs/
```

## Update an existing package

1. Put the new `.deb` in `debs/`.
2. Remove the old `.deb` if it should no longer be offered.
3. Run `python3 scripts/build_repo.py`.
4. Commit and push.
5. Refresh sources in Cydia/Sileo/Zebra on the phone.

## Remove a package

```bash
cd /Users/traw/Desktop/AI-Projects/kvlabs
rm debs/<package>.deb
python3 scripts/build_repo.py
git add -A
git commit -m "Remove <package-name>"
git push
```

## Validate from Mac

```bash
curl -L https://trawww.github.io/kvlabs/Release
curl -L https://trawww.github.io/kvlabs/Packages
curl -L https://trawww.github.io/kvlabs/Packages.gz | gzip -dc
```

## Validate from Sparrow/iPhone

After adding the repo to the package manager, refresh sources and confirm the package appears.

CLI shape if APT is usable:

```sh
apt-get update
apt-cache policy <package-name>
```

## Notes

- `scripts/build_repo.py` requires `dpkg-deb` when actual `.deb` files exist.
- Empty repo state is valid: `Packages` can be empty while `Release` still exists.
- Keep package identifiers lowercase and namespaced, e.g. `com.kvlabs.sparrowprefs`.
- For iOS 12/Substrate packages, prefer classic `iphoneos-arm` package architecture unless the package has a reason to do otherwise.
- Sign binaries/tweaks for iOS 12 with `ldid` before packaging.
- Do not publish secrets, tokens, device-specific `.env`, or private Sparrow runtime state into this repo.
