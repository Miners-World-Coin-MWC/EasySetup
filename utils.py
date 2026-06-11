import logging
from pathlib import Path

# -----------------------------
# LOGGING SETUP (shared)
# -----------------------------
def get_logger(name="MWC_INSTALLER"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


# -----------------------------
# DOWNLOADS CHECK (UX ONLY)
# -----------------------------
def check_downloads_hint():
    downloads = Path.home() / "Downloads"
    return any(downloads.glob("minersworldcoin*.zip"))


# -----------------------------
# SAFE PROMPT HELPERS
# -----------------------------
def confirm(prompt: str, default: bool = False) -> bool:
    """
    Simple yes/no prompt helper.
    """
    suffix = " [Y/n]: " if default else " [y/N]: "

    ans = input(prompt + suffix).strip().lower()

    if not ans:
        return default

    return ans in ("y", "yes")