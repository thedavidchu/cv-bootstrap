def get_mouse_movement():
    import tkinter as tk
    root = tk.Tk()

    def mmove(event):
        print(event.x, event.y)

    root.bind('<Motion>', mmove)
    root.mainloop()


def canvas_drawing():
    import tkinter as tk

    canvas_width = 500
    canvas_height = 500


    def paint(event):
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        w.create_oval(x1, y1, x2, y2, fill=python_green)



    master = tk.Tk()
    master.title("Points")
    w = tk.Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack(expand=tk.YES, fill=tk.BOTH)
    w.bind("<B1-Motion>", paint)

    message = tk.Label(master, text="Press and Drag the mouse to draw")
    message.pack(side=tk.BOTTOM)

    tk.mainloop()


if __name__ == '__main__':
    canvas_drawing()