from pathlib import Path

# -----------------------------
# BLOCKCHAIN CHECK
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

# -----------------------------
# INSTALL DETECTION
# -----------------------------
def detect_existing_install(
    install_dir,
    get_wallet_datadir
):
    datadir = get_wallet_datadir()

    return {
        # Program files
        "install_dir": (
            install_dir.exists()
        ),

        # wallet data
        "data_dir": (
            datadir.exists()
        ),

        # config exists
        "conf": (
            datadir
            /
            "minersworldcoin.conf"
        ).exists(),

        # blockchain downloaded
        "blockchain": (
            blockchain_exists(
                datadir
            )
        ),

        # actual wallet executable
        "binary": (
            install_dir.exists()
            and
            any(
                install_dir.glob(
                    "minersworldcoin*"
                )
            )
        )
    }

# -----------------------------
# VALID INSTALL
# -----------------------------
def is_valid_install(state):
    return (
        state["install_dir"]
        and
        state["data_dir"]
        and
        state["conf"]
    )