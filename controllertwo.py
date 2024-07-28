import pyautogui
import time

time.sleep(5)  # Give yourself 5 seconds to switch to the correct window
print("started")
# Move the mouse to a specific position on the screen
pyautogui.moveTo(700, 500, duration=1)  # Move to (100, 100) over 1 second

pyautogui.moveTo(800, 400, duration=0.5)  # Move to (2