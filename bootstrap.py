from config import BOOTSTRAP_FILE, BOOTSTRAP_SHA256, RELEASE_BASE
from downloader import download_file
from verify import verify_sha256
from extractor import extract_zip
from utils import get_logger, confirm

log = get_logger("MWC_BOOTSTRAP")


def bootstrap(datadir, BASE_DIR, blockchain_exists):

    if blockchain_exists(datadir):
        log.info("Bootstrap skipped - blockchain exists")
        return

    if not confirm("Download bootstrap?"):
        log.info("Bootstrap skipped by user")
        return

    url = RELEASE_BASE + BOOTSTRAP_FILE
    zip_path = BASE_DIR / BOOTSTRAP_FILE

    log.info("Downloading bootstrap...")
    download_file(url, zip_path)

    verify_sha256(zip_path, BOOTSTRAP_SHA256)
    extract_zip(zip_path, datadir)

    zip_path.unlink(missing_ok=True)

    log.info("Bootstrap installed")