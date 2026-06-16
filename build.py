import os
import sys
import shutil
import subprocess
from pathlib import Path

APP_NAME = "MinersWorldCoinInstaller"
ROOT = Path(__file__).parent
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"

# -----------------------------
# CLEAN
# -----------------------------
def clean():
    print("Cleaning old builds...")
    for folder in [
        BUILD_DIR,
        DIST_DIR
    ]:
        if folder.exists():

            shutil.rmtree(folder)

# -----------------------------
# PYINSTALLER
# -----------------------------
def install_pyinstaller():
    try:
        import PyInstaller
        print(
            "PyInstaller already installed"
        )

    except ImportError:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "pyinstaller"
            ]
        )

# -----------------------------
# BUILD
# -----------------------------
def build():
    print(
        "Building MinersWorldCoin Installer..."
    )

    hidden_imports = [
        "requests",
        "tkinter",
        "logging",
        "zipfile",
        "hashlib",
        "shutil",
        "subprocess",
        "platform",
        "main",
        "system",
        "install_state",
        "downloader",
        "verify",
        "extractor",
        "config_writer",
        "bootstrap",
        "backup",
        "config"
    ]

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name",
        APP_NAME,
        str(
            ROOT / "gui.py"
        )

    ]

    # -------------------------
    # PLATFORM
    # -------------------------
    if sys.platform.startswith("win"):
        print("Windows build")
        command.extend(
            [
                "--windowed",
                "--onefile",
                "--uac-admin"
            ]
        )

    elif sys.platform == "darwin":
        print("macOS build")
        command.extend(
            [
                "--windowed",
                "--onedir"
            ]
        )

    else:
        print("Linux build")
        command.extend(
            [
                "--onefile",
                "--windowed"
            ]
        )

    # -------------------------
    # ASSETS
    # -------------------------
    assets = ROOT / "assets"
    if assets.exists():
        command.extend(
            [
                "--add-data",
                f"{assets}{os.pathsep}assets"
            ]
        )

    # -------------------------
    # ICON
    # -------------------------
    if sys.platform == "darwin":
        icon = (
            ROOT /
            "assets" /
            "mwc.icns"
        )
    else:
        icon = (
            ROOT /
            "assets" /
            "mwc.ico"
        )

    if icon.exists():
        command.extend(
            [
                "--icon",
                str(icon)
            ]
        )

    # -------------------------
    # HIDDEN IMPORTS
    # -------------------------
    for module in hidden_imports:
        command.extend(
            [
                "--hidden-import",
                module
            ]
        )

    print("\nRunning:")
    print(
        " ".join(
            str(x)
            for x in command
        )
    )

    subprocess.check_call(
        command
    )

# -----------------------------
# DONE
# -----------------------------
def finished():
    print()
    print("====================")
    print("BUILD COMPLETE")
    print("====================")

    if sys.platform.startswith("win"):
        output = (
            DIST_DIR /
            f"{APP_NAME}.exe"
        )

    elif sys.platform == "darwin":
        output = (
            DIST_DIR /
            f"{APP_NAME}.app"
        )

    else:
        output = (
            DIST_DIR /
            APP_NAME
        )

    print(
        f"Output:\n{output}"
    )

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    clean()
    install_pyinstaller()
    build()
    finished()