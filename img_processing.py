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

def postprocessing(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a simple binary threshold
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Convert the binary image back to PIL format
    binary_pil = Image.fromarray(binary)
    return binary_pil

def split_into_parts(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Unable to load image at {img_path}")
        return

    img_height, img_width, _ = img.shape
    print(f"Image dimensions: {img_width}x{img_height}")

    
    x = 10 #190
    y = 10 #1150
    width = 64;
    height = 64;
    
    for i in range(4):
        for j in range(4):
            cropped_img = img[y:y+height, x:x+width]
            # Apply postprocessing to clean up the image
            processed_img = postprocessing(cropped_img)
            processed_img.save('cropped_image'+str(i)+str(j)+'.jpg')
            x += 78  # move to the next column
        y += 79  # move to the next row
        x = 10  # reset x to the starting position


    # Display the cropped image (optional)
    #cv2.imshow('Cropped Image', cropped_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
#Split the screenshot into the 16 letters

def extract_letters():
    letters = [['' for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            image_path = "cropped_image"+str(i)+str(j)+".jpg"
            letter = pytesseract.image_to_string(Image.open(image_path), config="--psm 10")
            letter = letter.replace('\n', '').replace('\r', '').strip()
            if letter == '|':
                letter = 'I'
            if letter == '0':
                letter = 'O'
            letter = letter[0]
            letters[i][j] = letter.lower()

    return letters

def img_complete_processing():
    screenshotter.take_screenshot()
    time.sleep(0.5)
    #full.png
    split_into_parts("screenshot.jpg")
    return extract_letters()
    
print(img_complete_processing())

