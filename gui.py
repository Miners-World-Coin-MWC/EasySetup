import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import threading
import logging
import subprocess
import platform
import sys
import os

from pathlib import Path

from main import run_installer
from system import get_wallet_datadir

from install_state import (
    detect_existing_install,
    is_valid_install,
    blockchain_exists
)
CURRENT_VERSION = "1.0.0.1"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)

log = logging.getLogger("MWC_GUI")

# -----------------------------
# THEME
# -----------------------------

BG = "#101820"
CARD = "#18232F"
ACCENT = "#00D4FF"
TEXT = "#FFFFFF"
MUTED = "#9AA7B2"

# -----------------------------
# ASSETS
# -----------------------------
def resource_path(relative):

    try:
        base = sys._MEIPASS

    except Exception:
        base = Path(__file__).parent

    return Path(base) / relative

LOGO_PATH = resource_path(
    "assets/logo.png"
)

ICON_WIN = resource_path(
    "assets/mwc.ico"
)


# -----------------------------
# DEFAULT INSTALL PATH
# -----------------------------

def get_default_install():

    if platform.system() == "Windows":

        return (
            Path(
                os.environ.get(
                    "PROGRAMFILES",
                    "C:\\Program Files"
                )
            )
            /
            "MinersWorldCoin"
        )

    return (
        Path.home()
        /
        ".local"
        /
        "MinersWorldCoin"
    )


# -----------------------------
# LOG HANDLER
# -----------------------------

class TextHandler(logging.Handler):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget


    def emit(self, record):
        msg = self.format(record)
        self.widget.after(
            0,
            self.append,
            msg
        )

    def append(self,msg):
        self.widget.insert(
            tk.END,
            msg + "\n"
        )
        self.widget.see(
            tk.END
        )

# -----------------------------
# GUI
# -----------------------------
class InstallerGUI:

    def __init__(self,root):
        self.root = root
        self.install_path = tk.StringVar(
            value=str(
                get_default_install()
            )
        )
        self.data_path = tk.StringVar(
            value=str(
                get_wallet_datadir()
            )
        )
        self.status_text = tk.StringVar(
            value="Checking..."
        )

        root.title(
            "MinersWorldCoin Wallet"
        )
        root.geometry(
            "760x650"
        )
        root.configure(
            bg=BG
        )

        # -------------------------
        # PROGRESS STYLE
        # -------------------------
        progress_style = ttk.Style(root)
        try:
            progress_style.theme_use("clam")
        except:
            pass

        progress_style.configure(
            "MWC.Horizontal.TProgressbar",
            troughcolor="#05090D",
            background=ACCENT,
            bordercolor=BG,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
            thickness=14
        )

        # ICON
        try:
            if platform.system()=="Windows":
                root.iconbitmap(
                    ICON_WIN
                )
            else:
                root.iconphoto(
                    True,
                    tk.PhotoImage(
                        file=LOGO_PATH
                    )
                )

        except Exception as e:

            log.warning(
                f"Icon failed: {e}"
            )


        # HEADER

        header = tk.Frame(
            root,
            bg=BG
        )

        header.pack(
            pady=8
        )


        try:

            self.logo = tk.PhotoImage(
                file=LOGO_PATH
            )

            tk.Label(
                header,
                image=self.logo,
                bg=BG
            ).pack()

        except Exception as e:

            log.warning(
                f"Logo missing: {e}"
            )


        tk.Label(
            header,
            text="MinersWorldCoin",
            font=("Arial",24,"bold"),
            fg=ACCENT,
            bg=BG
        ).pack()


        tk.Label(
            header,
            text="Official Desktop Wallet Installer",
            font=("Arial",11),
            fg=MUTED,
            bg=BG
        ).pack()


        tk.Label(
            header,
            text=f"Version {CURRENT_VERSION}",
            font=("Arial",9),
            fg=MUTED,
            bg=BG
        ).pack()

        # STATUS CARD
        card = tk.Frame(
            root,
            bg=CARD
        )

        card.pack(
            fill="x",
            padx=30,
            pady=5
        )

        self.status = tk.Label(
            card,
            textvariable=self.status_text,
            font=("Arial",13,"bold"),
            fg=TEXT,
            bg=CARD
        )

        self.status.pack(
            pady=8
        )

        tk.Label(
            card,
            text=
            "wallet.dat is protected.\n"
            "Blockchain files may be refreshed during reinstall.",
            fg=MUTED,
            bg=CARD
        ).pack()

        # LOCATIONS

        location = tk.Frame(
            root,
            bg=BG
        )

        location.pack(
            pady=10
        )
        tk.Label(
            location,
            text="Install Location",
            fg=TEXT,
            bg=BG,
            font=("Arial",10,"bold")
        ).pack()
        row=tk.Frame(
            location,
            bg=BG
        )

        row.pack()
        tk.Entry(
            row,
            textvariable=self.install_path,
            width=55
        ).pack(
            side="left"
        )
        tk.Button(
            row,
            text="Browse",
            command=self.choose_install_location,
            bg=CARD,
            fg=TEXT
        ).pack(
            side="left",
            padx=5
        )
        tk.Label(
            location,
            text="Wallet Data Directory",
            fg=TEXT,
            bg=BG,
            font=("Arial",10,"bold")
        ).pack(
            pady=(10,0)
        )

        tk.Label(
            location,
            textvariable=self.data_path,
            fg=MUTED,
            bg=BG
        ).pack()

        # PROGRESS
        self.progress = ttk.Progressbar(
            root,
            length=600,
            mode="indeterminate",
            style="MWC.Horizontal.TProgressbar"
        )
        self.progress.pack(
            pady=8
        )
        # LOG
        self.log_box=tk.Text(
            root,
            height=10,
            bg="#05090D",
            fg=TEXT
        )
        self.log_box.pack(
            padx=30,
            pady=10,
            fill="both"
        )
        logging.getLogger().addHandler(
            TextHandler(
                self.log_box
            )
        )
        # BUTTONS
        buttons=tk.Frame(
            root,
            bg=BG
        )
        buttons.pack(
            pady=8
        )
        style={
            "width":22,
            "height":2,
            "font":("Arial",10,"bold"),
            "bg":CARD,
            "fg":TEXT
        }
        self.install_button=tk.Button(
            buttons,
            text="Install / Update",
            command=self.start_install,
            **style
        )
        self.install_button.grid(
            row=0,
            column=0,
            padx=8
        )
        self.folder_button=tk.Button(
            buttons,
            text="Open Wallet Folder",
            command=self.open_wallet_folder,
            **style
        )
        self.folder_button.grid(
            row=0,
            column=1,
            padx=8
        )
        self.launch_button=tk.Button(
            buttons,
            text="Launch Wallet",
            state="disabled",
            command=self.launch_wallet,
            **style
        )
        self.launch_button.grid(
            row=1,
            column=0,
            padx=8
        )
        self.repair_button=tk.Button(
            buttons,
            text="Repair Wallet",
            command=self.repair_wallet,
            **style
        )
        self.repair_button.grid(
            row=1,
            column=1,
            padx=8
        )
        tk.Button(
            buttons,
            text="Exit",
            command=root.destroy,
            **style
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=5
        )
        # FOOTER
        tk.Label(
            root,
            text="MinersWorldCoin © 2026 | Secure Desktop Wallet Installer",
            font=("Arial",9),
            fg=MUTED,
            bg=BG
        ).pack(
            pady=5
        )
        self.refresh_status()
    # STATUS
    def refresh_status(self):

        try:

            install_dir = Path(
                self.install_path.get()
            )

            state = detect_existing_install(
                install_dir,
                get_wallet_datadir
            )


            wallet_exists = is_valid_install(
                state
            )


            chain_exists = blockchain_exists(
                get_wallet_datadir()
            )


            if wallet_exists and chain_exists:

                self.status_text.set(
                    "✅ Wallet Installed"
                )

                self.status.config(
                    fg="#00FF88"
                )


            elif wallet_exists and not chain_exists:

                self.status_text.set(
                    "⚠️ Missing Blockchain"
                )

                self.status.config(
                    fg="#FFD700"
                )


            else:

                self.status_text.set(
                    "❌ Not Installed"
                )

                self.status.config(
                    fg="#FF5555"
                )


        except Exception as e:

            log.warning(
                f"Status check failed: {e}"
            )

            self.status_text.set(
                "⚠️ Status Unknown"
            )

            self.status.config(
                fg="#FFD700"
            )
    # -----------------------------
    # INSTALL
    # -----------------------------
    def choose_install_location(self):
        folder=filedialog.askdirectory()
        if folder:
            self.install_path.set(
                folder
            )
            self.refresh_status()
    def start_install(self):
        self.install_button.config(
            state="disabled"
        )
        self.progress.start(10)
        threading.Thread(
            target=self.install,
            args=("fresh",False),
            daemon=True
        ).start()

    def install(self,mode,delete_chain):
        try:
            result=run_installer(
                mode=mode,
                delete_chain=delete_chain,
                install_path=Path(
                    self.install_path.get()
                ),
                progress=lambda x:logging.info(x)
            )
            self.root.after(
                0,
                self.refresh_status
            )
            self.root.after(
                0,
                lambda:
                messagebox.showinfo(
                    "Complete",
                    result
                )
            )
            self.launch_button.config(
                state="normal"
            )

        except Exception as e:
            logging.exception(
                "Installer failed"
            )
            self.root.after(
                0,
                lambda:
                messagebox.showerror(
                    "Installer Error",
                    str(e)
                )
            )

        finally:
            self.progress.stop()
            self.install_button.config(
                state="normal"
            )
    # -----------------------------
    # REPAIR
    # -----------------------------
    def repair_wallet(self):
        threading.Thread(
            target=self.repair,
            daemon=True
        ).start()

    def repair(self):
        try:
            result=run_installer(
                mode="repair",
                install_path=Path(
                    self.install_path.get()
                ),
                progress=lambda x:logging.info(x)
            )
            self.root.after(
                0,
                self.refresh_status
            )
            self.root.after(
                0,
                lambda:
                messagebox.showinfo(
                    "Repair Complete",
                    result
                )
            )
        except Exception as e:
            self.root.after(
                0,
                lambda:
                messagebox.showerror(
                    "Repair Failed",
                    str(e)
                )
            )
    # -----------------------------
    # WALLET
    # -----------------------------
    def open_wallet_folder(self):
        path=get_wallet_datadir()
        subprocess.Popen(
            [
                "explorer",
                str(path)
            ]
        )

    def launch_wallet(self):
        install=Path(
            self.install_path.get()
        )

        wallet=install / "minersworldcoin-qt.exe"
        if wallet.exists():
            subprocess.Popen(
                [
                    str(wallet)
                ]
            )
        else:
            messagebox.showwarning(
                "Missing",
                "Wallet executable not found"
            )

if __name__=="__main__":
    root=tk.Tk()
    InstallerGUI(
        root
    )
    root.mainloop()