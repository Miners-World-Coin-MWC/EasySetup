from utils import get_logger, confirm
log = get_logger("MWC_CONFIG")

CONF_CONTENT = None

def write_conf(
    datadir,
    CONF_CONTENT,
    overwrite=None
):

    datadir.mkdir(
        parents=True,
        exist_ok=True
    )

    path = datadir / "minersworldcoin.conf"

    # Existing config
    if path.exists():
        # GUI / installer mode
        if overwrite is not None:
            if not overwrite:
                log.info(
                    "Keeping existing config"
                )

                return False

        # Terminal mode
        else:
            if not confirm(
                "Config exists. Overwrite?"
            ):

                log.info(
                    "Keeping existing config"
                )

                return False

    log.info(
        "Writing config"
    )

    path.write_text(
        CONF_CONTENT
    )

    return True