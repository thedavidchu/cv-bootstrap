import cv2


def cv2_imshow(file_path: str):
    img = cv2.imread(file_path)
    cv2.imshow(file_path, img)
    return


if __name__ == '__main__':
    cv2_imshow('images/nebu.png')


