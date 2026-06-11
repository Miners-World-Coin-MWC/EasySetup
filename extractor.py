import zipfile
import shutil
import logging

log = logging.getLogger("MWC")

def extract_zip(zip_path, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)

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