import tkinter as tk
import tkinter.filedialog as fd


class Application:
    def __init__(self, window):
        self.window = window

    def open_dir(self):
        self.window.withdraw()
        dir = tk.filedialog.askdirectory(initialdir='../../')
        return dir


if __name__ == '__main__':
    window = tk.Tk()
    app = Application(window)
    dir = app.open_dir()
    tk.mainloop()