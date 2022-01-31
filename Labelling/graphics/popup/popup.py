import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox

import warnings


def show_prompt(title: str, prompt: str):
    x = simpledialog.askstring(title, prompt)
    return x


def show_info(title: str, message: str):
    messagebox.showinfo(title, message)


def show_warning(title: str, message: str):
    messagebox.showwarning(title, message)
    warnings.warn(message)


def show_error(title: str, message: str):
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


# #Import the required Libraries
# from tkinter import *
# from tkinter import ttk
# #Create an instance of Tkinter frame
# win = Tk()
# #Set the geometry of Tkinter frame
# win.geometry("750x270")
#
# def open_popup():
#    top= Toplevel(win)
#    top.geometry("750x250")
#    top.title("Child Window")
#    Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y=80)
#
# Label(win, text=" Click the Below Button to Open the Popup Window", font=('Helvetica 14 bold')).pack(pady=20)
# #Create a button in the main Window to open the popup
# ttk.Button(win, text= "Open", command= open_popup).pack()
# win.mainloop()