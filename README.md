# MinersWorldCoin EasySetup

Official desktop wallet installer for MinersWorldCoin.

## Features

-   Windows, Linux and macOS builds
-   GUI based wallet installer
-   Automatic wallet detection
-   Wallet configuration repair
-   Safe wallet backup handling
-   Blockchain refresh support
-   Protects wallet.dat during repair/reinstall

## Requirements

Python 3.8+

Install dependencies:

``` bash
pip install -r requirements.txt
```

## Running From Source

Start the installer:

``` bash
python gui.py
```

## Building

Build the installer using:

``` bash
python build.py
```

The build script uses PyInstaller and creates a platform specific
executable.

Outputs are created in:

    dist/

## Supported Platforms

-   Windows
-   Linux
-   macOS

## Project Structure

    EasySetup/
    │
    ├── gui.py              # Tkinter installer interface
    ├── main.py             # Installer engine
    ├── build.py            # PyInstaller build script
    ├── config.py           # Wallet configuration
    ├── config_writer.py    # Config handling
    ├── downloader.py       # Wallet downloader
    ├── verify.py           # SHA256 verification
    ├── extractor.py        # Archive extraction
    ├── bootstrap.py        # Blockchain bootstrap handling
    ├── backup.py           # Wallet backup
    └── assets/             # Icons and images

## Security

The installer does not delete:

-   wallet.dat
-   private keys
-   user wallet data

Blockchain data can be refreshed during reinstall if selected.

## License

MinersWorldCoin © 2026
