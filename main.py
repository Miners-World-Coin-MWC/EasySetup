import logging
import shutil
from pathlib import Path

from config import *
from system import get_wallet_datadir, detect_wallet_key
from install_state import detect_existing_install, is_valid_install, blockchain_exists
from downloader import download_file
from verify import verify_sha256
from extractor import extract_zip
from config_writer import write_conf
from bootstrap import bootstrap

BASE_DIR = Path.home() / "MinersWorldCoinInstaller"
INSTALL_DIR = BASE_DIR / "wallet"
LOCK_FILE = BASE_DIR / ".install_lock"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MWC")

def main():

    if LOCK_FILE.exists():
        raise RuntimeError("Installer already running")

    LOCK_FILE.write_text("locked")

    try:
        key = detect_wallet_key()
        print("Detected:", key)

        state = detect_existing_install(INSTALL_DIR, get_wallet_datadir)

        mode = "fresh"

        if is_valid_install(state):
            print("\nExisting install detected")
            print(state)

            choice = input("\n1 upgrade / 2 repair / 3 fresh: ")

            mode = {"1": "upgrade", "2": "repair", "3": "fresh"}.get(choice, "fresh")

        filename, sha = WALLETS[key]
        url = RELEASE_BASE + filename

        INSTALL_DIR.mkdir(parents=True, exist_ok=True)

        zip_path = INSTALL_DIR / filename

        if mode == "repair":
            write_conf(get_wallet_datadir, CONF_CONTENT)
            return

        if mode == "fresh":
            datadir = get_wallet_datadir()

            if datadir.exists():
                confirm = input("Delete blockchain? y/N: ")
                if confirm == "y":
                    for f in ["blocks", "chainstate"]:
                        p = datadir / f
                        if p.exists():
                            shutil.rmtree(p)

        download_file(url, zip_path)
        verify_sha256(zip_path, sha)
        extract_zip(zip_path, INSTALL_DIR)

        write_conf(get_wallet_datadir(), CONF_CONTENT)
        bootstrap(get_wallet_datadir, BASE_DIR, blockchain_exists)

        print("INSTALL COMPLETE")

    finally:
        LOCK_FILE.unlink(missing_ok=True)

if __name__ == "__main__":
    main()