import hashlib
import os
import logging

log = logging.getLogger("MWC")

def verify_sha256(file_path, expected_hash):
    log.info("Verifying SHA256...")

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)

    if sha.hexdigest() != expected_hash:
        try:
            os.remove(file_path)
        except:
            pass

        raise RuntimeError("SHA256 mismatch")

    log.info("SHA256 OK")