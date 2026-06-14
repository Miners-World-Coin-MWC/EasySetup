import shutil
import logging
from datetime import datetime


log = logging.getLogger("MWC")


def backup_wallets(datadir):

    """
    Backup wallet files only.
    Never backs up or deletes blockchain data.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    backup_root = (
        datadir
        /
        "wallet_backups"
        /
        timestamp
    )


    wallets_found = []


    # -------------------------
    # New wallet layout
    # -------------------------

    wallets_dir = datadir / "wallets"


    if wallets_dir.exists():

        for item in wallets_dir.iterdir():

            if (
                item.name.endswith(".dat")
                or item.name == "wallet.dat"
            ):
                wallets_found.append(
                    item
                )


    # -------------------------
    # Legacy wallet layout
    # -------------------------

    old_wallet = (
        datadir
        /
        "wallet.dat"
    )


    if old_wallet.exists():

        wallets_found.append(
            old_wallet
        )


    if not wallets_found:

        log.info(
            "No wallet files found to backup"
        )

        return None


    backup_root.mkdir(
        parents=True,
        exist_ok=True
    )


    for wallet in wallets_found:

        destination = (
            backup_root
            /
            wallet.name
        )


        if wallet.is_dir():

            shutil.copytree(
                wallet,
                destination
            )

        else:

            shutil.copy2(
                wallet,
                destination
            )


    log.info(
        f"Wallet backup created: {backup_root}"
    )


    return backup_root