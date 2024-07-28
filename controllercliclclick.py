import subprocess
import time

def mouse_move(x, y):
    apple_script = f"""
    tell application "System Events"
        do shell script "cliclick m:{x},{y}"
    end tell
    """
    subprocess.run(['osascript', '-e', apple_script])

def mouse_click(x, y):
    apple_script = f"""
    tell application "System Events"
        do shell script "cliclick c:{x},{y}"
    end tell
    """
    subprocess.run(['osascript', '-e', apple_script])

# Example usage
time.sleep(3)  # Time to switch to the screen mirrored phone screen
mouse_move(700, 400)  # Move to (300, 300)
time.sleep(1)
mouse_click(700, 500)  # Click at (300, 300)
