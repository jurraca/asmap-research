{
  description = "shell";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = {nixpkgs, ...}: let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    devShells.x86_64-linux.default =
      let
        requests = (pkgs.python311.withPackages (ps: [ps.requests]));
      in pkgs.mkShell {
      packages = [ pkgs.python311 requests ] ;
    };
  };
}
