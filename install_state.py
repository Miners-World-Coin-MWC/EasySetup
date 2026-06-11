def blockchain_exists(datadir):
    blocks = datadir / "blocks"
    chainstate = datadir / "chainstate"

    return (
        blocks.exists()
        and chainstate.exists()
        and any(blocks.iterdir())
        and any(chainstate.iterdir())
    )


def detect_existing_install(INSTALL_DIR, get_wallet_datadir):
    datadir = get_wallet_datadir()

    return {
        "wallet_dir": INSTALL_DIR.exists(),
        "data_dir": datadir.exists(),
        "conf": (datadir / "minersworldcoin.conf").exists(),
        "blockchain": blockchain_exists(datadir),
        "binary": INSTALL_DIR.exists() and any(INSTALL_DIR.glob("*"))
    }


def is_valid_install(state):
    return state["data_dir"] and state["conf"] and state["blockchain"]