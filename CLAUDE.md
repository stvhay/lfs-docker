# lfs-docker

Dockerfile to build Linux From Scratch 11.1-systemd, supporting x86_64 and aarch64/arm64.

## Build

```bash
# Build x86_64 ISO
DOCKER_BUILDKIT=1 docker build -o . .

# Build aarch64 (requires QEMU setup for cross-arch)
# First modify ARG values at top of Dockerfile, then:
DOCKER_BUILDKIT=1 docker build -o . .
```

## Test

```bash
# Boot x86_64 ISO in QEMU (BIOS)
qemu-system-x86_64 -m 1024M -cdrom lfs-x86_64.iso

# Boot x86_64 ISO in QEMU (UEFI)
qemu-system-x86_64 -m 1024M -bios /usr/share/ovmf/OVMF.fd -cdrom lfs-x86_64.iso
```

## Architecture

The Dockerfile uses multi-stage builds:
1. **host** (Alpine) - Prepares host, builds cross-toolchain (LFS sections 2-7.3)
2. **toolchain** (scratch) - Chroots into toolchain, builds more packages (sections 7.4-7.14)
3. **system** (toolchain) - Builds final system packages (sections 8-10)
4. **iso-builder** (Alpine) - Produces bootable ISO with GRUB (BIOS + UEFI)

## Conventions

- All build logic is self-contained in the Dockerfile
- No external context files are used
- Architecture is controlled via ARG variables at the top of Dockerfile
- ISO supports both legacy BIOS and UEFI boot modes
