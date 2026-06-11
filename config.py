RELEASE_BASE = "https://github.com/Miners-World-Coin-MWC/MinersWorldCoin/releases/download/1.0.0.1/"

WALLETS = {
    "windows_64": ("minersworldcoin-x86_64-win.zip", "cd794d0b060840bc638dde79ff9de71ed7d4f6c681c1e4a168045eaa6a6d07cf"),
    "windows_32": ("minersworldcoin-i686-win.zip", "87f087a921db3a322c16b13adcb20920b15d0586dc1c6482c8913bc0b8e9ffcc"),
    "linux_64": ("minersworldcoin-x86_64-linux.zip", "4427a9d5d718873d77e3fef264fb29074e0b273d2c7d5d9cd52760093c95a04f"),
    "linux_32": ("minersworldcoin-i686-linux.zip", "d237fcc2fa9f9abd2fd2a35801a0aeedf2fbe7acdaf593ad2c607478a83be8d2"),
    "linux_arm64": ("minersworldcoin-aarch64-linux.zip", "70d827b3f2f8b340144cb40f50a8a201070ec156e71da89d4f4c974de38a6b3e"),
    "linux_arm": ("minersworldcoin-armhf-linux.zip", "01da4361e28435273f4b1591c6cf0244bcfe7416f597d97be0b90cb70b896b35"),
    "mac_64": ("minersworldcoin-x86_64-macos.zip", "969740cb536f13237dbcf515cc7b2dcbf0bb08a2cd3e6a9f7ed042b32c33e963"),
}

CONF_CONTENT = """server=1
daemon=1
txindex=1
addressindex=1
rpcuser=user
rpcpassword=x
rpcport=5579
rpcallowip=127.0.0.1
rpcbind=127.0.0.1
bind=0.0.0.0
rpcworkqueue=512
maxconnections=256
addnode=51.15.16.47
"""

BOOTSTRAP_FILE = "bootstrap.zip"

BOOTSTRAP_SHA256 = "2e64d902d5b2db8f35f13e7103678bf201bbe99edc99f81aced99392f174020f"