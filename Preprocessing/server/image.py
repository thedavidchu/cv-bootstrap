import cv2
from PIL import Image, ImageTk


from Preprocessing.server.label import ImageLabels


class Image:
    def __init__(self, image_path: str, label_path: str = None):
        self.image_path = image_path
        self.label_path = label_path

        # Delete after you're finished; this hogs memory
        # self.image = cv2.imread(self.image_path)
        self.image = Image.open(image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_shape = self.image.size
        self.labels = ImageLabels(self.image_shape)

    # ==================== DEBUGGING TOOLS ==================== #
    def show(self):
        cv2.imshow(self.image_path, self.image)

    # ==================== CONVERSION ==================== #

    # ==================== PREPROCESSING ==================== #
    def resize(self, x, y):
        self.image.resize(x, y)
        raise NotImplementedError('cannot resize shapes yet.')

    def rotate(self, theta):
        raise NotImplementedError('cannot rotate shapes yet.')


class Images:
    def __init__(self):
        pass

