import cv2
import tkinter as tk


def cv2_imshow(image_path: str):
    """
    The image is height*width*channel.

    :param image_path:
    :return:
    """
    img = cv2.imread(image_path)
    cv2.imshow(image_path, img)
    return


def tkinter_imshow(image_path: str):
    window = tk.Tk()

    # Open Image
    image = tk.PhotoImage(file=image_path)
    window.title(image_path)
    background_image = tk.Label(image=image)
    background_image.pack()

    tk.mainloop()

if __name__ == '__main__':
    image_path = '../images/skule/nebu.png'
    # cv2_imshow(image_path)
    tkinter_imshow(image_path)


