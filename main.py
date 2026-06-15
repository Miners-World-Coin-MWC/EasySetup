import logging
import shutil
import platform
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
def get_default_install_base():
    if platform.system() == "Windows":
        return (
            Path("C:/Program Files")
            /
            "MinersWorldCoin"
        )
    else:
        return (
            Path.home()
            /
            ".minersworldcoin"
        )

INSTALL_DIR = get_default_install_base()

def set_install_dir(path):
    global INSTALL_DIR
    INSTALL_DIR = Path(path)

def get_install_dir(filename):
    global INSTALL_DIR
    if INSTALL_DIR == get_default_install_base():
        folder_name = Path(
            filename
        ).stem
        INSTALL_DIR = (
            INSTALL_DIR
            /
            folder_name
        )

    return INSTALL_DIR

BASE_DIR = get_default_install_base()

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
def remove_blockchain(
    datadir,
    progress=None
):
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
    install_path=None,
    progress=None
):

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

    LOCK_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
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

        # -------------------------
        # DOWNLOAD INFO
        # -------------------------
        filename, sha = WALLETS[key]
        url = (
            RELEASE_BASE
            +
            filename
        )

        # -------------------------
        # INSTALL LOCATION
        # -------------------------
        if install_path:
            set_install_dir(
                install_path
            )

        install_dir = get_install_dir(
            filename
        )

        install_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        update(
            f"Install location: {install_dir}"
        )

        state = detect_existing_install(
            install_dir,
            get_wallet_datadir
        )

        if is_valid_install(state):
            update(
                "Existing wallet installation detected"
            )

        zip_path = (
            install_dir
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

        # -------------------------
        # EXTRACT
        # -------------------------
        update(
            "Extracting wallet files..."
        )

        extract_zip(
            zip_path,
            install_dir
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
            install_dir,
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