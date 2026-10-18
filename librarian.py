#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

EXPECTED_VENV = "venv"
REQUIREMENTS_FILE = "requirements.txt"  # Используем один файл

KERNEL_NAME = "movielens"
KERNEL_DISPLAY_NAME = "Python (movielens venv)"

# Packages that pip installs into every venv; no need to pin them.
EXCLUDE_FROM_LOCK = {"pip", "setuptools", "wheel"}

PROJECT_ROOT = Path(__file__).resolve().parent


def in_correct_env() -> bool:
    """Return True only if running inside the expected virtual environment."""
    if sys.prefix == sys.base_prefix:
        return False
    return Path(sys.prefix).name == EXPECTED_VENV


def pip_install(req_file: Path) -> None:
    """Install packages from req_file using this venv's pip."""
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
        check=True,
    )


def pip_freeze_lines() -> list[str]:
    """Return `pip freeze` output as a list, minus trivial bootstrap packages."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True,
    )
    kept = []
    for line in result.stdout.splitlines():
        name = line.split("==", 1)[0].split("@", 1)[0].strip().lower()
        if name in EXCLUDE_FROM_LOCK:
            continue
        kept.append(line)
    return kept


def write_lock_file(lock_file: Path) -> None:
    """Write pinned versions to requirements.txt."""
    lines = pip_freeze_lines()
    lock_file.write_text("\n".join(lines) + "\n")
    print(f"Wrote {lock_file.name} with {len(lines)} pinned packages.")


def kernel_is_registered() -> bool:
    """Check whether this exact venv is the registered movielens kernel."""
    result = subprocess.run(
        [sys.executable, "-m", "jupyter", "kernelspec", "list", "--json"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False
    try:
        specs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return False

    spec = specs.get("kernelspecs", {}).get(KERNEL_NAME)
    if spec is None:
        return False

    resource_dir = spec.get("resource_dir", "")
    if not resource_dir:
        return False

    kernel_json = Path(resource_dir) / "kernel.json"
    if not kernel_json.exists():
        return False

    try:
        cfg = json.loads(kernel_json.read_text())
    except json.JSONDecodeError:
        return False

    argv = cfg.get("argv", [])
    if not argv:
        return False

    return Path(argv[0]).resolve() == Path(sys.executable).resolve()


def register_jupyter_kernel() -> None:
    """Register this venv as a Jupyter kernel (idempotent, replaces stale entries)."""
    if kernel_is_registered():
        print(
            f"Jupyter kernel '{KERNEL_NAME}' already registered for this venv — skipping."
        )
        return

    print(f"Registering Jupyter kernel '{KERNEL_NAME}'...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ipykernel",
            "install",
            "--user",
            f"--name={KERNEL_NAME}",
            f"--display-name={KERNEL_DISPLAY_NAME}",
        ],
        check=True,
    )


def main() -> None:
    if not in_correct_env():
        raise RuntimeError(
            f"This script must run inside the '{EXPECTED_VENV}' virtual environment. "
            f"Current prefix: {sys.prefix}"
        )

    print(f"Running inside: {sys.prefix}")

    req_file = PROJECT_ROOT / REQUIREMENTS_FILE
    if not req_file.exists():
        raise FileNotFoundError(f"Missing {req_file}")

    print(f"Installing from {req_file.name}...")
    pip_install(req_file)

    # После установки перезаписываем requirements.txt точными версиями
    print("Freezing installed versions...")
    write_lock_file(req_file)

    register_jupyter_kernel()

    print("Done.")


if __name__ == "__main__":
    main()
