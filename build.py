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

            shutil.rmtree(
                folder
            )


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

        print(
            "Installing PyInstaller..."
        )

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

        # python libs
        "requests",
        "tkinter",
        "logging",
        "zipfile",
        "hashlib",
        "shutil",
        "subprocess",
        "platform",

        # project modules
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

        "--windowed",

        "--onefile",

        "--name",
        APP_NAME,


        str(
            ROOT /
            "gui.py"
        )
    ]


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
    # WINDOWS ONLY
    # -------------------------

    if sys.platform.startswith("win"):

        print(
            "Windows build detected"
        )

        # allows Program Files install
        command.append(
            "--uac-admin"
        )


    else:

        print(
            f"Building for {sys.platform}"
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

    exe = (
        DIST_DIR /
        APP_NAME
    )


    if sys.platform.startswith("win"):

        exe = exe.with_suffix(
            ".exe"
        )


    print()
    print("====================")
    print("BUILD COMPLETE")
    print("====================")

    print(
        f"Output:\n{exe}"
    )


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":

    clean()

    install_pyinstaller()

    build()

    finished()