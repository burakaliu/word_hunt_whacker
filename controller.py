import time
from pynput.mouse import Button, Controller

mouse = Controller()

def click(x, y):
    mouse.position = (x, y)
    mouse.click(Button.left, 1)

def drag(start_x, start_y, end_x, end_y, duration=1):
    mouse.position = (start_x, start_y)
    mouse.press(Button.left)
    time.sleep(0.1)
    mouse.move(end_x - start_x, end_y - start_y)
    time.sleep(duration)
    mouse.release(Button.left)

# Example usage
time.sleep(5)  # Give yourself 2 seconds to switch to the correct window

# Click at (500, 500)
print("started")
click(500, 500)
print("Clicked")
time.sleep(1)  # Wait for 1 second

# Drag from (500, 500) to (600, 600)
drag(700, 500, 700, 400)
print("Dragged")

for int in range(3):
    time.sleep(1)  # Wait for 1 second
    mouse.position = (700, 500)
    time.sleep(1)  # Wait for 1 second
    mouse.position = (700, 400)
