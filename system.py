import os
import platform
from pathlib import Path

def get_wallet_datadir():
    sys = platform.system().lower()

    if sys == "windows":
        return Path(os.environ["APPDATA"]) / "MinersWorldCoin"

    if sys == "darwin":
        return Path.home() / "Library/Application Support/MinersWorldCoin"

    return Path.home() / ".minersworldcoin"


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