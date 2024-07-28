# Install opencv-python library using pip
# pip install opencv-python

import time
import cv2
from PIL import Image
import pytesseract
import pickle
from trie_tree import Trie
import screenshotter

img_path = 'single_letter.jpg'

def postprocessing(image_path):

    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to make the image binary
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Display the modified image
    #cv2.imshow('Modified Image', binary)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Convert the binary image back to PIL format
    binary_pil = Image.fromarray(binary)
    return binary

def split_into_parts(img_path):
    
    img = cv2.imread(img_path)
    
    x = 0 #190
    y = 0 #1150
    width = 150;
    height = 150;
    
    for i in range(4):
        for j in range(4):
            cropped_img = img[y:y+height, x:x+width]
            # Convert the image to grayscale
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            # Apply thresholding to make the image binary
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite('cropped_image'+str(i)+str(j)+'.jpg', binary)
            x += 210
        y += 210
        x = 190

    # Display the cropped image (optional)
    cv2.imshow('Cropped Image', cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
#Split the screenshot into the 16 letters
screenshotter.take_screenshot()
time.sleep(1)
#full.png
split_into_parts("screenshot.jpg")
