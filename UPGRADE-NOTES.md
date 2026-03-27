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

## New Packages Added

LFS 13.0 introduced new packages that we added:

- libxcrypt-4.5.2 (required by shadow - glibc 2.43 no longer includes libcrypt)
- lz4-1.10.0 (compression library)
- pcre2-10.47 (regular expression library)
- sqlite-3510200 (database library)
- flit-core-3.12.0 (Python build dependency)
- packaging-26.0 (Python build dependency)
- wheel-0.46.3 (Python build dependency)
- setuptools-82.0.0 (Python build dependency)

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

## Build Instructions Updated

The following packages required build instruction changes beyond version updates:

### Binutils (all passes)
- Added `--enable-gprofng=no` (pass 1 and pass 2 only)
- Added `--enable-new-dtags`
- Added `--enable-default-hash-style=gnu`
- System build: added `--sysconfdir=/etc`, removed `--enable-gold`
- System build: updated cleanup to remove gprofng/sframe files

### GCC hardcoded paths
- Updated hardcoded GCC version paths from 11.2.0 to 15.2.0 (mkheaders, include dirs, etc.)

### All Chapter 6 cross-compiled packages (MB_LEN_MAX workaround)
glibc 2.43 changed MB_LEN_MAX from 16 to 32. When cross-compiling on Alpine (musl-based), the host compiler's headers provide MB_LEN_MAX=16, but the target glibc headers expect 32, causing a compile-time assertion failure:
```
#error "Assumed value of MB_LEN_MAX wrong"
```

**Fix:** Add `CFLAGS="-isystem $LFS/usr/include"` to all chapter 6 cross-compile configure commands to prioritize target glibc headers over host headers.

Affected packages:
- m4, bash, coreutils, diffutils, file, findutils, gawk, grep, gzip, make, patch, sed, tar, xz

### Ncurses (cross-compile stage)
- Updated to LFS 13.0 build approach: build host tic first, install to `$LFS/tools/bin`, then cross-compile

### Util-linux (chapter 7 and 8)
- Added `--disable-liblastlog2` to disable liblastlog2 feature (requires sqlite3 which is not in base LFS)
- Added `--runstatedir=/run`
- Reordered configure options to match LFS 13.0 book

### Man-pages
- Added `rm -v man3/crypt*` to remove crypt man pages (libxcrypt provides better versions)
- Changed `make prefix=/usr install` to `make -R GIT=false prefix=/usr install`

### Bc
- Changed `CC=gcc` to `CC='gcc -std=c99'` to fix GCC 15 compatibility with true/false macros
- Added `-r` option to configure

### GMP
- Added `sed -i '/long long t1;/,+1s/()/(...)/' configure` for GCC 15 compatibility

### Shadow
- Added `--with-{b,yes}crypt` for bcrypt/yescrypt support
- Added `--without-libbsd` to use internal readpassphrase
- Added `--disable-logind` since systemd isn't available yet during build

### GCC (final build)
- Added `sed -i 's/char [*]q/const &/' libgomp/affinity-fmt.c` for const correctness
- Added `--enable-default-pie`, `--enable-default-ssp`, `--enable-host-pie` for security
- Added `--disable-fixincludes`
- Removed obsolete SIGSTKSZ sed command

### Glibc
- Added `--disable-nscd`
- Changed `--enable-kernel=3.2` to `--enable-kernel=5.4`
- Removed `--with-headers=/usr/include`

### Python
- Removed `--with-system-ffi` and `--with-ensurepip=yes`
- Added `--without-static-libpython`

### Ninja
- Added `--verbose` to configure.py

### Meson, MarkupSafe, Jinja2
- Changed from deprecated `setup.py` to `pip3 wheel` build method

### Kmod
- Changed from autoconf to meson build system
- Added `-D manpages=false`

### Elfutils
- Changed `make` to `make -C lib && make -C libelf` (builds only libelf)
- Tests removed (fail with glibc-2.43)

### Libffi
- Removed `--disable-exec-static-tramp`

### Systemd
- Changed to `meson setup ..` syntax
- Added `-D pamconfdir=no`, `-D dev-kvm-mode=0660`, `-D nobody-group=nogroup`
- Added `-D sysupdate=disabled`, `-D ukify=disabled`
- Changed `-Dhomed=false` to `-D homed=disabled`
- Changed `-Dman=false` to `-D man=disabled`

### Perl
- Updated version paths from 5.34 to 5.42

If other builds fail, check the LFS 13.0 book for instruction changes:
https://www.linuxfromscratch.org/lfs/view/13.0-systemd/

## Issues Found During Upgrade

1. **Expat moved from SourceForge to GitHub** - URL changed to https://github.com/libexpat/libexpat/releases/
2. **PyPI package names are lowercase** - MarkupSafe and Jinja2 tarballs use lowercase names (markupsafe-3.0.3.tar.gz, jinja2-3.1.6.tar.gz)
3. **glibc-2.42-upstream_fixes-1.patch not needed** - The design mentioned this patch but it's for glibc-2.42; LFS 13.0 uses glibc-2.43 which has fixes included
4. **dbus tarball extension changed** - Now distributed as .tar.xz instead of .tar.gz
5. **busybox source changed** - Now uses Alpine's busybox-static package instead of downloading from busybox.net (which has TLS timeout issues)
6. **Tcl source URL format changed** - Now uses `sourceforge.net/projects/tcl/files/.../download` suffix instead of `downloads.sourceforge.net/tcl/` due to Docker ADD redirect issues
7. **Tcl bundled packages updated** - tdbc changed from 1.1.3 to 1.1.12, itcl changed from 4.2.2 to 4.3.4
8. **Expect source URL format changed** - Same SourceForge redirect issue as Tcl
