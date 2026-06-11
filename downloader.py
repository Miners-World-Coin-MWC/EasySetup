import requests
import time
import logging

log = logging.getLogger("MWC")

def download_file(url, path, retries=3):
    headers = {"User-Agent": "MWC-Installer/1.0"}

    for attempt in range(retries):
        try:
            log.info(f"Downloading ({attempt+1}/{retries})")

            with requests.get(url, stream=True, timeout=60, headers=headers) as r:
                r.raise_for_status()

                total = int(r.headers.get("content-length", 0))
                downloaded = 0

                with open(path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if not chunk:
                            continue

                        f.write(chunk)
                        downloaded += len(chunk)

                        if total:
                            percent = (downloaded * 100) // total
                            print(f"\rDownloading... {percent}%", end="", flush=True)

                print()

            return

        except Exception as e:
            log.warning(f"Download failed: {e}")
            time.sleep(2)

    raise RuntimeError("Download failed after retries")