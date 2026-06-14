import logging
import shutil
from pathlib import Path

from config import *
from system import (
    get_wallet_datadir,
    detect_wallet_key
)

from install_state import (
    detect_existing_install,
    is_valid_install,
    blockchain_exists
)

from downloader import download_file
from verify import verify_sha256
from extractor import extract_zip
from config_writer import write_conf
from bootstrap import bootstrap
from backup import backup_wallets


# -----------------------------
# PATHS
# -----------------------------

BASE_DIR = (
    Path.home()
    /
    "MinersWorldCoinInstaller"
)

INSTALL_DIR = (
    BASE_DIR
    /
    "wallet"
)

LOCK_FILE = (
    BASE_DIR
    /
    ".install_lock"
)


# -----------------------------
# LOGGING
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)

log = logging.getLogger("MWC")


# -----------------------------
# SAFE BLOCKCHAIN REMOVE
# NEVER TOUCH wallet.dat
# -----------------------------

def remove_blockchain(datadir, progress=None):

    folders = [
        "blocks",
        "chainstate"
    ]

    for folder in folders:

        target = datadir / folder

        if target.exists():

            if progress:
                progress(
                    f"Removing {folder}..."
                )

            log.info(
                f"Removing blockchain data: {target}"
            )

            shutil.rmtree(
                target
            )


# -----------------------------
# INSTALL ENGINE
# -----------------------------

def run_installer(
    mode="fresh",
    delete_chain=False,
    progress=None
):

    BASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    def update(message):

        log.info(
            message
        )

        if progress:
            progress(
                message
            )


    if LOCK_FILE.exists():

        raise RuntimeError(
            "Installer already running"
        )


    LOCK_FILE.write_text(
        "locked"
    )


    try:

        update(
            "Starting MinersWorldCoin installer..."
        )


        key = detect_wallet_key()

        update(
            f"Detected system: {key}"
        )


        datadir = get_wallet_datadir()


        state = detect_existing_install(
            INSTALL_DIR,
            get_wallet_datadir
        )


        if is_valid_install(state):

            update(
                "Existing wallet installation detected"
            )


        filename, sha = WALLETS[key]

        url = (
            RELEASE_BASE
            +
            filename
        )


        INSTALL_DIR.mkdir(
            parents=True,
            exist_ok=True
        )


        zip_path = (
            INSTALL_DIR
            /
            filename
        )


        # -------------------------
        # REPAIR
        # -------------------------

        if mode == "repair":

            update(
                "Repairing configuration..."
            )


            write_conf(
                datadir,
                CONF_CONTENT
            )


            return (
                "Configuration repaired"
            )


        # -------------------------
        # BACKUP WALLET
        # -------------------------

        if datadir.exists():

            update(
                "Creating wallet backup..."
            )


            backup = backup_wallets(
                datadir
            )


            if backup:

                update(
                    f"Backup created:\n{backup}"
                )


        # -------------------------
        # DELETE BLOCKCHAIN ONLY
        # -------------------------

        if delete_chain:

            update(
                "Removing old blockchain data..."
            )


            remove_blockchain(
                datadir,
                progress
            )


        # -------------------------
        # DOWNLOAD
        # -------------------------

        update(
            "Downloading wallet..."
        )


        download_file(
            url,
            zip_path
        )


        update(
            "Verifying download..."
        )


        verify_sha256(
            zip_path,
            sha
        )


        update(
            "Extracting wallet files..."
        )


        extract_zip(
            zip_path,
            INSTALL_DIR
        )


        zip_path.unlink(
            missing_ok=True
        )


        # -------------------------
        # CONFIG
        # -------------------------

        update(
            "Writing configuration..."
        )


        write_conf(
            datadir,
            CONF_CONTENT
        )


        # -------------------------
        # BOOTSTRAP
        # -------------------------

        update(
            "Checking blockchain bootstrap..."
        )


        bootstrap(
            datadir,
            BASE_DIR,
            blockchain_exists
        )


        update(
            "Installation complete"
        )


        return (
            "MinersWorldCoin installed successfully"
        )


    finally:

        LOCK_FILE.unlink(
            missing_ok=True
        )



# -----------------------------
# TEST MODE
# -----------------------------

if __name__ == "__main__":

    run_installer(
        mode="fresh",
        delete_chain=False
    )