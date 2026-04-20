{
  description = "ChauchaApp";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python312
            pkgs.uv
            pkgs.git
            pkgs.docker
            pkgs.docker-compose
          ];

          shellHook = ''
            # Forzar a uv a usar SOLO el venv local, nunca el store de Nix
            export UV_PYTHON_DOWNLOADS=never
            export UV_PROJECT_ENVIRONMENT=.venv
            export VIRTUAL_ENV="$PWD/.venv"

            # Crear venv si no existe, apuntando explícitamente al Python de Nix
            if [ ! -d .venv ]; then
              echo "→ Creando entorno virtual..."
              ${pkgs.uv}/bin/uv venv .venv --python ${pkgs.python312}/bin/python3
            fi

            # Activar venv ANTES de cualquier operación con uv
            source .venv/bin/activate
            export PATH="$PWD/.venv/bin:$PATH"

            # Instalar/sincronizar dependencias dentro del venv ya activado
            if [ -f pyproject.toml ]; then
              uv sync --no-managed-python
            elif [ -f requirements.txt ]; then
              uv pip install -r requirements.txt
            fi

            echo "✓ Entorno ChauchaApp listo (Python: $(python --version))"
            echo "  Venv: $VIRTUAL_ENV"
          '';
        };
      }
    );
}
