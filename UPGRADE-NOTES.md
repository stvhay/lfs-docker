# LFS 11.1 → 13.0 Upgrade Notes

## Overview

This documents the upgrade from LFS 11.1-systemd to LFS 13.0-systemd.

## High-Risk Changes

These packages had major version jumps and may cause build issues:

| Package | Old | New | Risk |
|---------|-----|-----|------|
| GCC | 11.2.0 | 15.2.0 | Major compiler change |
| Glibc | 2.35 | 2.43 | Core library, ABI changes |
| Linux | 5.16.9 | 6.18.10 | Kernel API changes |
| Python | 3.10.2 | 3.14.3 | Major version |
| Gettext | 0.21 | 1.0 | Major version |
| Meson | 0.61.1 | 1.10.1 | Major version |

## Removed Packages

These packages were in LFS 11.1 but removed in LFS 13.0:

| Package | Reason |
|---------|--------|
| check-0.15.2 | Testing framework, not needed for base system |
| eudev-3.2.11 | systemd's built-in udev used instead |
| sysklogd-1.5.1 | systemd journal handles logging |
| sysvinit-3.01 | LFS 13.0 is systemd-only |
| udev-lfs-20171102 | Helper scripts for eudev, not needed |
| lfs-bootscripts-20210608 | sysvinit boot scripts, not needed |

## Package Renames

| Old | New |
|-----|-----|
| pkg-config-0.29.2 | pkgconf-2.5.1 |

## New Packages NOT Added

LFS 13.0 includes these new packages that we did NOT add (scope limited to version updates):

- flit-core-3.12.0
- libxcrypt-4.5.2
- lz4-1.10.0
- packaging-26.0
- pcre2-10.47
- setuptools-82.0.0
- sqlite-3510200
- wheel-0.46.3

## Patch Changes

### Removed Patches
- binutils-2.38-lto_fix-1.patch
- coreutils-9.0-chmod_fix-1.patch
- perl-5.34.0-upstream_fixes-1.patch
- systemd-250-upstream_fixes-1.patch
- sysvinit-3.01-consolidated-1.patch

### Updated Patches
- coreutils-9.0-i18n-1.patch → coreutils-9.10-i18n-1.patch
- glibc-2.35-fhs-1.patch → glibc-fhs-1.patch
- kbd-2.4.0-backspace-1.patch → kbd-2.9.0-backspace-1.patch

### Added Patches
- expect-5.45.4-gcc15-1.patch

### Patches NOT Added
- glibc-2.42-upstream_fixes-1.patch (mentioned in changelog, but not in official patches list; applies to glibc-2.42, not needed for glibc-2.43)

## Build Instructions Not Updated

This upgrade only changed versions. If builds fail, check the LFS 13.0 book for instruction changes:
https://www.linuxfromscratch.org/lfs/view/13.0-systemd/

## Issues Found During Upgrade

1. **Expat moved from SourceForge to GitHub** - URL changed to https://github.com/libexpat/libexpat/releases/
2. **PyPI package names are lowercase** - MarkupSafe and Jinja2 tarballs use lowercase names (markupsafe-3.0.3.tar.gz, jinja2-3.1.6.tar.gz)
3. **glibc-2.42-upstream_fixes-1.patch not needed** - The design mentioned this patch but it's for glibc-2.42; LFS 13.0 uses glibc-2.43 which has fixes included
