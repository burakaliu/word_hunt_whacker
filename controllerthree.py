import Quartz
import time

def create_touch_event(event_type, touches):
    event = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
        event_type,  # NSEventTypeGesture
        (0, 0),  # Location
        0,  # Modifier flags
        0,  # Timestamp
        0,  # Window number
        None,  # Graphics context
        0,  # Subtype
        touches,  # Data1 (number of touches)
        0  # Data2
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event.CGEvent())

def touch_down(x, y, finger_id=0):
    event = Quartz.CGEventCreateTouchEvent(
        Quartz.kCGEventLeftMouseDown,
        (x, y),
        finger_id,
        1  # Touch down
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def touch_up(x, y, finger_id=0):
    event = Quartz.CGEventCreateTouchEvent(
        Quartz.kCGEventLeftMouseUp,
        (x, y),
        finger_id,
        0  # Touch up
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def touch_move(x, y, finger_id=0):
    event = Quartz.CGEventCreateTouchEvent(
        Quartz.kCGEventMouseMoved,
        (x, y),
        finger_id,
        1  # Touch down and move
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

# Example usage
time.sleep(3)  # Time to switch to the screen mirrored phone screen
touch_down(700, 400)  # Touch down at (300, 300)
time.sleep(0.1)
touch_move(700, 500)  # Move to (400, 400)
time.sleep(0.1)
touch_up(700, 500)  # Lift touch at (400, 400)
