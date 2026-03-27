{
  description = "lfs-docker - Build Linux From Scratch 11.1-systemd via Docker";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            # Container runtime
            docker
            docker-buildx

            # Testing ISOs
            qemu
            OVMF  # UEFI firmware for qemu

            # Utilities
            coreutils
            gnugrep
            gnused
            gawk

            # Version management
            python3
          ];

          shellHook = ''
            echo "lfs-docker dev environment loaded"
            echo "  docker build: DOCKER_BUILDKIT=1 docker build -o . ."
            echo "  test x86_64:  qemu-system-x86_64 -m 1024M -cdrom lfs-x86_64.iso"
          '';
        };
      });
}
