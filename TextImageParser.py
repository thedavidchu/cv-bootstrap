import cv2
import json
import numpy as np
import os

'''
Basic Process:
If mode is line, then draw lines connecting the points and then draw a circle with center at each of those
and with radius equal to the width.

If mode is polygon, then use draw polygon fill the polygon.

TODO: Add os iteration for text in folders
'''

if __name__ == "__main__":
    file_path = # Put the path to the image file
    read_file = open(file_path,"r")

    data = json.load(read_file)
    labels = data["labels"]
    size = data["image_size"]

    # print(len(labels))
    img_mask = np.zeros((size[0],size[1]))
    for lbl in labels:
        if (lbl["mode"] == "POLYGON"):
            pts = np.array(lbl["geometry"],np.int32)
            pts = pts.reshape((-1,1,2))

            img_mask = cv2.polylines(img_mask,[pts],True,255,3)
            img_mask = cv2.fillPoly(img_mask,[pts],255)

        elif (lbl["mode"] == "LINE"):
            pts = np.array(lbl["geometry"],np.int32)
            l_width = lbl["width"]

            for i in range(0,len(pts)-1):
                img_mask = cv2.circle(img_mask,(pts[i][0],pts[i][1]),l_width,255,-1)
                img_mask = cv2.circle(img_mask,(pts[i+1][0],pts[i+1][1]),l_width,255,-1)
                img_mask = cv2.line(img_mask,(pts[i][0],pts[i][1]),(pts[i+1][0],pts[i+1][1]),255,l_width)

    cv2.imwrite("/Your Save Directory/Test_img.png",img_mask)
