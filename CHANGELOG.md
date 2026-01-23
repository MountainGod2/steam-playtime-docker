# CHANGELOG

<!-- version list -->

## v1.1.2 (2026-01-23)

### Bug Fixes

- **release**: Allow continuation on error when downloading release info
  ([`21e2557`](https://github.com/MountainGod2/steam-playtime-docker/commit/21e25574100edb764a936b9000b864cc400f0c03))

### Chores

- **deps**: Update dependency pyrefly to v0.49.0
  ([#9](https://github.com/MountainGod2/steam-playtime-docker/pull/9),
  [`4b81dc8`](https://github.com/MountainGod2/steam-playtime-docker/commit/4b81dc80062b1dbe5ef9bbad51c23eec3a8938d8))


## v1.1.1 (2026-01-21)

### Bug Fixes

- **release**: Add 'latest' tag to container image metadata
  ([`377e110`](https://github.com/MountainGod2/steam-playtime-docker/commit/377e110870066376fcf52ffbef3b744d82cee583))


## v1.1.0 (2026-01-21)

### Features

- **ci-cd**: Remove build-container job and add release-container workflow
  ([`9b5b693`](https://github.com/MountainGod2/steam-playtime-docker/commit/9b5b6937d230124984c5e1f527c333ca27ade8d5))


## v1.0.3 (2026-01-21)

### Bug Fixes

- **ci-cd**: Refine build-container job conditions and remove unused deploy job
  ([`ab4ec47`](https://github.com/MountainGod2/steam-playtime-docker/commit/ab4ec475472a05175631a4bca67411f248aefdf9))

### Chores

- **deps**: Pin dependencies
  ([`3c7e276`](https://github.com/MountainGod2/steam-playtime-docker/commit/3c7e276d5cc4c2193a387985a83c786b5c30c60f))

- **deps**: Update actions/cache action to v5
  ([#7](https://github.com/MountainGod2/steam-playtime-docker/pull/7),
  [`dd63bf6`](https://github.com/MountainGod2/steam-playtime-docker/commit/dd63bf648b3fe4d9c78417c97dd3eec6f074109d))

- **deps**: Update dependency pyrefly to v0.48.2
  ([#6](https://github.com/MountainGod2/steam-playtime-docker/pull/6),
  [`dd42bda`](https://github.com/MountainGod2/steam-playtime-docker/commit/dd42bdad2173a6b4927610a89234c6455fb3636d))

- **deps**: Update docker/metadata-action digest to c299e40
  ([#8](https://github.com/MountainGod2/steam-playtime-docker/pull/8),
  [`c3a3e53`](https://github.com/MountainGod2/steam-playtime-docker/commit/c3a3e53163726363057600958437e862ca8313a1))

- **deps**: Update docker/metadata-action digest to c299e40
  ([`60a4414`](https://github.com/MountainGod2/steam-playtime-docker/commit/60a44143b1e748700ce6842f63fffd4d146ef966))

- **deps**: Update docker/setup-buildx-action digest to 8d2750c
  ([#5](https://github.com/MountainGod2/steam-playtime-docker/pull/5),
  [`c03a00f`](https://github.com/MountainGod2/steam-playtime-docker/commit/c03a00ff808c25fb9a0d66da3cf55857bdb9afc7))

### Refactoring

- Consolidate CI/CD workflows by removing redundant docker.yml
  ([`7441ff9`](https://github.com/MountainGod2/steam-playtime-docker/commit/7441ff9693806b0fc60cb93fb5fa135757e4dc76))


## v1.0.2 (2026-01-17)

### Bug Fixes

- Update push tags to match semantic versioning format
  ([`485e4a6`](https://github.com/MountainGod2/steam-playtime-docker/commit/485e4a684468d0c21e80fd555f1f9a61adc3089b))


## v1.0.1 (2026-01-17)

### Bug Fixes

- Add missing newline at the end of __init__.py
  ([`e17fce6`](https://github.com/MountainGod2/steam-playtime-docker/commit/e17fce656af1cabba27aff0320713574a955d2cd))

- Simplify build job sync command
  ([`653bdf6`](https://github.com/MountainGod2/steam-playtime-docker/commit/653bdf6b9c020a19ae555c655a06e79e47921f7f))

- Update sync command to use all groups for consistency
  ([`29ed5e2`](https://github.com/MountainGod2/steam-playtime-docker/commit/29ed5e202dcd85998369b296f53405b9e4adff03))

### Refactoring

- Remove cleanup job from Docker workflow
  ([`89daeeb`](https://github.com/MountainGod2/steam-playtime-docker/commit/89daeeb892967f5fe3caa42464f40bda93e763f9))

- Simplify CI/CD workflow
  ([`5f9cda2`](https://github.com/MountainGod2/steam-playtime-docker/commit/5f9cda214f9188edcc4923609648fda44858ff51))


## v1.0.0 (2026-01-17)

- Initial Release
