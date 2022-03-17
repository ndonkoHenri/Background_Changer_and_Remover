import os
import cv2 as cv
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import mediapipe as mp
import numpy as np

cap = cv.VideoCapture(0)
cap.set(3, 640)  # Values are set because of the image format(640x480)
cap.set(4, 480)
segmentor = SelfiSegmentation()


def empty(x):
    pass


cv.namedWindow("tb")
cv.resizeWindow("tb", 400, 80)
cv.createTrackbar("threshold", "tb", 15, 100, empty)
images_location = "bg_images"
img_files_bg = os.listdir(images_location)
fpsReader = cvzone.FPS()
bg_index = 0
img_bg_read = []
for img_bg in img_files_bg:
    bg_read = cv.imread(f"{images_location}/{img_bg}")
    img_bg_read.append(bg_read)
while True:
    success, image = cap.read()
    threshold = cv.getTrackbarPos("threshold", 'tb')

    imgOut = segmentor.removeBG(image, imgBg=img_bg_read[bg_index], threshold=threshold / 100)

    # fps_imgOut, imgOut = fpsReader.update(imgOut)
    img_stack = cvzone.stackImages([image, imgOut], cols=2, scale=0.5)
    fps_image, img_stack = fpsReader.update(img_stack)
    cv.imshow("Image", img_stack)
    key = cv.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('n'):
        bg_index = bg_index + 1 if 0 <= bg_index < len(img_files_bg) - 1 else 0
    elif key == ord('p'):
        bg_index = bg_index - 1 if 0 <= bg_index < len(img_files_bg) - 1 else 0


cv.destroyAllWindows()
