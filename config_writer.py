from utils import get_logger, confirm

log = get_logger("MWC_CONFIG")

CONF_CONTENT = None  # imported from config.py


def write_conf(datadir, CONF_CONTENT):
    datadir.mkdir(parents=True, exist_ok=True)

    path = datadir / "minersworldcoin.conf"

    if path.exists():
        if not confirm("Config exists. Overwrite?"):
            log.info("Keeping existing config")
            return

    log.info("Writing config")
    path.write_text(CONF_CONTENT)