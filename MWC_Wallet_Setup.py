import os
import platform
import requests
import zipfile
import hashlib
import shutil
import logging
import time
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
RELEASE_BASE = "https://github.com/Miners-World-Coin-MWC/MinersWorldCoin/releases/download/1.0.0.1/"

WALLETS = {
    "windows_64": ("minersworldcoin-x86_64-win.zip", "cd794d0b060840bc638dde79ff9de71ed7d4f6c681c1e4a168045eaa6a6d07cf"),
    "windows_32": ("minersworldcoin-i686-win.zip", "87f087a921db3a322c16b13adcb20920b15d0586dc1c6482c8913bc0b8e9ffcc"),
    "linux_64": ("minersworldcoin-x86_64-linux.zip", "4427a9d5d718873d77e3fef264fb29074e0b273d2c7d5d9cd52760093c95a04f"),
    "linux_32": ("minersworldcoin-i686-linux.zip", "d237fcc2fa9f9abd2fd2a35801a0aeedf2fbe7acdaf593ad2c607478a83be8d2"),
    "linux_arm64": ("minersworldcoin-aarch64-linux.zip", "70d827b3f2f8b340144cb40f50a8a201070ec156e71da89d4f4c974de38a6b3e"),
    "linux_arm": ("minersworldcoin-armhf-linux.zip", "01da4361e28435273f4b1591c6cf0244bcfe7416f597d97be0b90cb70b896b35"),
    "mac_64": ("minersworldcoin-x86_64-macos.zip", "969740cb536f13237dbcf515cc7b2dcbf0bb08a2cd3e6a9f7ed042b32c33e963"),
}

CONF_CONTENT = """server=1
daemon=1
txindex=1
addressindex=1
rpcuser=user
rpcpassword=x
rpcport=5579
rpcallowip=127.0.0.1
rpcbind=127.0.0.1
bind=0.0.0.0
rpcworkqueue=512
maxconnections=256
addnode=51.15.16.47
"""

BOOTSTRAP_FILE = "bootstrap.zip"

BOOTSTRAP_URL = (
    RELEASE_BASE + BOOTSTRAP_FILE
)

BOOTSTRAP_SHA256 = (
    "2e64d902d5b2db8f35f13e7103678bf201bbe99edc99f81aced99392f174020f"
)

# -----------------------------
# WALLET DATA DIR (SINGLE SOURCE OF TRUTH)
# -----------------------------
def get_wallet_datadir():
    sys = platform.system().lower()

    if sys == "windows":
        return Path(os.environ["APPDATA"]) / "MinersWorldCoin"

    if sys == "darwin":
        return Path.home() / "Library/Application Support/MinersWorldCoin"

    return Path.home() / ".minersworldcoin"


BASE_DIR = Path.home() / "MinersWorldCoinInstaller"
INSTALL_DIR = BASE_DIR / "wallet"
LOCK_FILE = BASE_DIR / ".install_lock"

BASE_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(BASE_DIR / "installer.log", encoding="utf-8")
    ]
)

log = logging.getLogger("MWC_INSTALLER")

# -----------------------------
# DETECT OS
# -----------------------------
def detect_wallet_key():
    sys = platform.system().lower()
    arch = platform.machine().lower()

    if sys == "windows":
        return "windows_64" if "64" in arch else "windows_32"

    if sys == "darwin":
        return "mac_64"

    if sys == "linux":
        if "aarch64" in arch or "arm64" in arch:
            return "linux_arm64"
        if "arm" in arch:
            return "linux_arm"
        return "linux_64" if "64" in arch else "linux_32"

    raise RuntimeError("Unsupported OS")

# -----------------------------
# INSTALL DETECTION (FIXED)
# -----------------------------
def blockchain_exists(datadir):
    blocks = datadir / "blocks"
    chainstate = datadir / "chainstate"

    return (
        blocks.exists()
        and chainstate.exists()
        and any(blocks.iterdir())
        and any(chainstate.iterdir())
    )

def detect_existing_install():
    datadir = get_wallet_datadir()

    return {
        "wallet_dir": INSTALL_DIR.exists(),
        "data_dir": datadir.exists(),
        "conf": (datadir / "minersworldcoin.conf").exists(),
        "blockchain": blockchain_exists(datadir),
        "binary": INSTALL_DIR.exists() and any(INSTALL_DIR.glob("*"))
    }

def is_valid_install(state):
    return (
        state["data_dir"]
        and state["conf"]
        and state["blockchain"]
    )
# -----------------------------
# DOWNLOAD
# -----------------------------
def download_file(url, path, retries=3):
    headers = {"User-Agent": "MWC-Installer/1.0"}

    for attempt in range(retries):

        try:
            log.info(f"Downloading ({attempt+1}/{retries})")

            with requests.get(
                url,
                stream=True,
                timeout=60,
                headers=headers
            ) as r:

                r.raise_for_status()

                total = int(
                    r.headers.get("content-length", 0)
                )

                downloaded = 0

                with open(path, "wb") as f:

                    for chunk in r.iter_content(
                        chunk_size=1024 * 1024
                    ):

                        if not chunk:
                            continue

                        f.write(chunk)

                        downloaded += len(chunk)

                        if total:
                            percent = (
                                downloaded * 100
                            ) // total

                            print(
                                f"\rDownloading... {percent}%",
                                end="",
                                flush=True
                            )

                print()

            return

        except Exception as e:

            log.warning(f"Download failed: {e}")
            time.sleep(2)

    raise RuntimeError(
        "Download failed after retries"
    )

# -----------------------------
# SHA256 VERIFY
# -----------------------------
def verify_sha256(file_path, expected_hash):
    log.info("Verifying SHA256...")

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)

    result = sha.hexdigest()

    if result != expected_hash:
        try:
            os.remove(file_path)
        except:
            pass
        raise RuntimeError("SHA256 mismatch")

    log.info("SHA256 OK")

# -----------------------------
# SAFE EXTRACT
# -----------------------------
def extract_zip(zip_path, target_dir):

    target_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    temp = target_dir / "_tmp_extract"

    if temp.exists():
        shutil.rmtree(temp)

    temp.mkdir(parents=True, exist_ok=True)

    log.info("Extracting...")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(temp)

    for item in temp.iterdir():
        dest = target_dir / item.name

        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()

        shutil.move(str(item), str(dest))

    shutil.rmtree(temp)

# -----------------------------
# CONF WRITE
# -----------------------------
def write_conf(datadir):
    datadir.mkdir(parents=True, exist_ok=True)

    path = datadir / "minersworldcoin.conf"

    if path.exists():

        answer = input(
            "\nminersworldcoin.conf already exists. Overwrite it? [y/N]: "
        ).strip().lower()

        if answer != "y":
            log.info("Keeping existing config")
            return

    log.info("Writing config")
    path.write_text(CONF_CONTENT)

# -----------------------------
# DOWNLOADS CHECK (UX ONLY)
# -----------------------------
def check_downloads_hint():
    downloads = Path.home() / "Downloads"
    return any(downloads.glob("minersworldcoin*.zip"))

# -----------------------------
# BOOTSTRAP HOOK
# -----------------------------
def bootstrap(datadir):

    if blockchain_exists(datadir):
        log.info(
            "Existing blockchain detected - bootstrap skipped"
        )
        return

    answer = input(
        "\nDownload blockchain bootstrap (~123MB)? [Y/n]: "
    ).strip().lower()

    if answer == "n":
        log.info("Bootstrap skipped by user")
        return

    bootstrap_zip = BASE_DIR / BOOTSTRAP_FILE

    download_file(
        BOOTSTRAP_URL,
        bootstrap_zip
    )

    verify_sha256(
        bootstrap_zip,
        BOOTSTRAP_SHA256
    )
    
    extract_zip(
        bootstrap_zip,
        datadir
    )

    try:
        bootstrap_zip.unlink()
    except Exception:
        pass

    log.info("Bootstrap installed successfully")

# -----------------------------
# MAIN
# -----------------------------
def main():
    log.info("=== MinersWorldCoin Installer ===")

    if LOCK_FILE.exists():
        raise RuntimeError("Installer already running or crashed previously")

    LOCK_FILE.write_text("locked")

    try:
        key = detect_wallet_key()
        log.info(f"Detected OS build: {key}")

        state = detect_existing_install()

        mode = "fresh"

        if is_valid_install(state):
            log.warning("Existing wallet detected")

            print("\nExisting install detected:")
            for k, v in state.items():
                print(f" - {k}: {v}")

            if check_downloads_hint():
                print("\nNote: Installer files found in Downloads folder")

            print("\n1 - Upgrade")
            print("2 - Repair config only")
            print("3 - Fresh reinstall")

            choice = input("\nSelect option: ").strip()

            mode = {
                "1": "upgrade",
                "2": "repair",
                "3": "fresh"
            }.get(choice, "fresh")

        filename, sha = WALLETS[key]
        url = RELEASE_BASE + filename

        INSTALL_DIR.mkdir(parents=True, exist_ok=True)

        zip_path = INSTALL_DIR / filename

        if mode == "repair":
            write_conf(get_wallet_datadir())
            return

        if mode in ["fresh", "upgrade"]:
            if mode == "fresh":

                datadir = get_wallet_datadir()

                if datadir.exists():

                    answer = input(
                        "\nFresh reinstall will delete local blockchain data (blocks and chainstate) but keep wallet.dat. Continue? [y/N]: "
                    ).strip().lower()

                    if answer != "y":
                        raise RuntimeError(
                            "Fresh reinstall cancelled"
                        )

                    log.info(
                        "Removing existing blockchain data..."
                    )

                    for folder in ["blocks", "chainstate"]:
                        target = datadir / folder

                        if target.exists():
                            shutil.rmtree(target)

            download_file(url, zip_path)
            verify_sha256(zip_path, sha)
            extract_zip(zip_path, INSTALL_DIR)

            try:
                zip_path.unlink()
            except Exception:
                pass

        write_conf(get_wallet_datadir())
        bootstrap(get_wallet_datadir())

        log.info("INSTALL COMPLETE")
        log.info(f"Wallet: {INSTALL_DIR}")
        log.info(f"Data: {get_wallet_datadir()}")

    finally:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

if __name__ == "__main__":
    main()