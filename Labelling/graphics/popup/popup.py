import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox

import warnings


def show_prompt(title: str, prompt: str):
    x = simpledialog.askstring(title, prompt)
    return x


def show_info(title: str, message: str = None):
    if message is None:
        message = title
    messagebox.showinfo(title, message)


def show_warning(title: str, message: str = None):
    if message is None:
        message = title
    messagebox.showwarning(title, message)
    warnings.warn(message)


def show_error(title: str, message: str = None):
    if message is None:
        message = title
    messagebox.showerror(title, message)
    raise Exception(message)


def open_popup(window, title: str = "TITLE HERE", text: str = "TEXT", action: callable = None) -> None:
    top = tk.Toplevel(window)
    top.geometry("50x50")
    top.title(f"{title}")
    tk.Label(top, text=f"{text}").pack()


def create_popup(window, title: str = "TITLE HERE", text: str = "TEXT", action: callable = None) -> callable:
    def open_popup_():
        top = tk.Toplevel(window)
        top.geometry("50x50")
        top.title(f"{title}")
        tk.Label(top, text=f"{text}").pack()

    return open_popup_
