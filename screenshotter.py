import pyautogui
import pygetwindow
from PIL import Image
import pyscreenshot as ImageGrab

def take_screenshot():
    # Define the region to capture (left, top, right, bottom)
    region = (60, 450, 380, 770)
    im = ImageGrab.grab(bbox=region)
    #im.show()
    im = im.convert('RGB')
    im.save("screenshot.jpg")
    print('Screenshot taken')
    

