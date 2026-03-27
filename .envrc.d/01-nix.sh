# Nix flake configuration
# This file is sourced before `use flake` in .envrc

# Ensure nix-direnv is used if available (faster caching)
if has nix_direnv_version; then
  nix_direnv_version 3.0.0
fi
