"""Obtiene únicamente la cadena PostgreSQL y la escribe en .env ignorado por Git."""

import argparse
import getpass
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    parsed = urllib.parse.urlsplit(args.base_url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or not parsed.hostname.endswith(".insforge.app")
        or parsed.username
        or parsed.password
    ):
        raise SystemExit("Usa la URL HTTPS de tu proyecto InsForge.")
    base = f"https://{parsed.hostname}"
    key = os.getenv("INSFORGE_ADMIN_KEY") or getpass.getpass(
        "Clave administrativa (no se guardará): "
    )

    def fetch(path):
        request = urllib.request.Request(base + path, headers={"Authorization": "Bearer " + key})
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)

    try:
        masked = fetch("/api/metadata/database-connection-string")["connectionURL"]
        password = fetch("/api/metadata/database-password")["databasePassword"]
        if not password or set(password) == {"*"}:
            raise ValueError("La contraseña aún no está disponible")
        url = re.sub(
            r"^(postgresql://[^:]+:)[^@]+(@)",
            lambda m: m[1] + urllib.parse.quote(password, safe="") + m[2],
            masked,
        )
        if "****" in url:
            raise ValueError("Cadena incompleta")
        path = Path(".env")
        lines = path.read_text().splitlines() if path.exists() else []
        lines = [line for line in lines if not line.startswith("DATABASE_URL=")]
        path.write_text("\n".join(["DATABASE_URL=" + url, *lines]) + "\n")
        path.chmod(0o600)
    except Exception as exc:
        raise SystemExit(
            f"No se pudo configurar la conexión ({type(exc).__name__}). No se imprimieron credenciales."
        ) from None
    print("DATABASE_URL configurada en .env. La clave administrativa no se guardó.")


if __name__ == "__main__":
    main()
