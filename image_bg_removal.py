import os
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# -------------------------------- #
dark = cv2.imread("bg_images/img_dark.png")  # Reads the image with the dark background
cv2.putText(dark, "COMMANDS: ", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (0, 255, 0), 1)
cv2.putText(dark, "In your Program use the following...", (20, 40), cv2.FONT_HERSHEY_PLAIN, 0.95, (0, 255, 0), 1)
cv2.putText(dark, "Press 'P' to Display the previous background-image!", (20, 60), cv2.FONT_HERSHEY_PLAIN, 0.95,
            (0, 255, 0), 1)
cv2.putText(dark, "Press 'N' to Display the Next background-image!", (20, 80), cv2.FONT_HERSHEY_PLAIN, 0.95,
            (0, 255, 0), 1)
cv2.putText(dark, "Press 'F' to Display the foreground-image forward!", (20, 100), cv2.FONT_HERSHEY_PLAIN, 0.95,
            (0, 255, 0), 1)
cv2.putText(dark, "Press 'B' to Display the foreground-image backward!", (20, 140), cv2.FONT_HERSHEY_PLAIN, 0.95,
            (0, 255, 0), 1)
cv2.putText(dark, "Press 'Q' to quit the BackGroundRemover Program!", (20, 120), cv2.FONT_HERSHEY_PLAIN, 0.95,
            (0, 255, 0), 1)
cv2.putText(dark, "Press any key to close this window and launch your program!", (20, 200), cv2.FONT_HERSHEY_PLAIN, 1.1,
            (10, 255, 10), 1)

cv2.imshow("Commands", dark)
# IF a key is pressed, close the window and start the program
key = cv2.waitKey(0)
if key:
    cv2.destroyWindow("Commands")
# -------------------------------- #
segmentor = SelfiSegmentation()  # Create an Instance of the Segmentation Class


def empty(x):
    """An empty function, defined for the trackbar window"""
    pass


cv2.namedWindow("tb")  # Creation of the Trackbar Window
cv2.resizeWindow("tb", 400, 80)  # Resizing of the window to a particular width and height
cv2.createTrackbar("threshold", "tb", 15, 100, empty)  # Creation of the threshold trackbar with initial value 15

# -------------------------------- #

images_location = "bg_images"  # The location of the Background Images
img_files_bg = os.listdir(images_location)  # Returns a list containing the name of the files in the 'images_location'
bg_index = 0  # an index number to keep track of our actual position(on which bg_image are we)
img_bg_read = []  # will contain all the images(already read) from the list 'img_files_bg'
for img_bg in img_files_bg:
    """Iteration over each background image"""
    bg_read = cv2.imread(f"{images_location}/{img_bg}")  # The image is being read
    img_bg_read.append(bg_read)  # And stored in a new list

# -------------------------------- #

images_location = "test_images"  # The location of the Background Images
img_test_files = os.listdir(images_location)  # Returns a list containing the name of the files in the 'images_location'

img_index = 0  # an index number to keep track of our actual position(on which bg_image are we)
all_img_read = []  # will contain all the images(already read) from the list 'img_test_files'
for img in img_test_files:
    """Iteration over each background image"""
    img_read = cv2.imread(f"{images_location}/{img}")  # The image is being read
    all_img_read.append(img_read)  # And stored in a new list

# -------------------------------- #

while True:
    threshold = cv2.getTrackbarPos("threshold", 'tb')  # Getting of the "threshold" Trackbar's actual Position

    imgOut = segmentor.removeBG(all_img_read[img_index], imgBg=img_bg_read[bg_index], threshold=threshold / 100)
    img_stack = cvzone.stackImages([all_img_read[img_index], imgOut], cols=2,
                                   scale=0.5)  # Using the cvzone image stacking function to stack

    cv2.imshow("Image", img_stack)  # Showing up our stacked images
    key = cv2.waitKey(1)  # Gets any key pressed
    if key == ord('q'):  # Checks if the key pressed was 'q' (To quit the program)
        break  # Breaks out and exits the program
    elif key == ord('n'):  # Checks if the key pressed was 'n' (for the <<Next>> image)
        # checks the index and moves to the "N"ext Background
        bg_index = bg_index + 1 if 0 <= bg_index < len(img_files_bg) - 1 else 0
    elif key == ord('p'):  # Checks if the key pressed was 'p' (for the <<Previous>> image)
        # checks the index and moves to the "P"revious Background
        bg_index = bg_index - 1 if 0 <= bg_index < len(img_files_bg) - 1 else 0
    elif key == ord('f'):  # Checks if the key pressed was 'f' (takes the next image <<Forward>> )
        # checks the index and moves to the "F"orward image
        img_index = img_index + 1 if 0 <= img_index < len(img_test_files) - 1 else 0
    elif key == ord('b'):  # Checks if the key pressed was 'p' (takes the next image <<Backward>> )
        # checks the index and moves to the "B"ackward image
        img_index = img_index - 1 if 0 <= img_index < len(img_test_files) - 1 else 0
    else:
        pass

cv2.destroyAllWindows()  # Destroys all opened windows present (Trackbars, webcam Output..)
