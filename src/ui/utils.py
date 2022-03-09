#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT

import tkinter as tk
from tkinter import filedialog, messagebox


def uiFileSearch(title: str):
    ui = tk.Tk()
    ui.withdraw()

    try:
        return filedialog.askopenfile(title=title).name
    except:
        return None


def errorMsgBox(msg):
    messagebox.showerror(title='ERROR', message=msg)


def infoMsgBox(msg):
    messagebox.showinfo(title='INFO', message=msg)


def warningMsgBox(msg):
    messagebox.showwarning(title='WARNING', message=msg)
