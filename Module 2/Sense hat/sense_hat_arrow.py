from sense_hat import SenseHat
import time
import random

sense = SenseHat()
sense.clear()

# Define the green arrow (pointing up in its base matrix definition)
G = (0, 255, 0)
O = (0, 0, 0)
green_arrow = [
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O,
    O, G, O, G, G, O, G, O,
    G, O, O, G, G, O, O, G,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O
]

def is_pointing_down(angle):
    accel = sense.get_accelerometer_raw()
    x = accel['x']
    y = accel['y']
    
    # When angle=0, arrow points to top edge. Top edge down -> y ≈ -1
    if angle == 0 and y < -0.5:
        return True
    # When angle=180, arrow points to bottom edge. Bottom edge down -> y ≈ 1
    elif angle == 180 and y > 0.5:
        return True
    # When angle=90, arrow points to right edge. Right edge down -> x ≈ 1
    elif angle == 90 and x > 0.5:
        return True
    # When angle=270, arrow points to left edge. Left edge down -> x ≈ -1
    elif angle == 270 and x < -0.5:
        return True
        
    return False

sense.show_message("Game Start", text_colour=(0, 255, 0), scroll_speed=0.05)

score = 0
angles = [0, 90, 180, 270]

try:
    while True:
        target_angle = random.choice(angles)
        sense.set_rotation(target_angle)
        sense.set_pixels(green_arrow)
        
        start_time = time.time()
        success = False
        
        while time.time() - start_time < 3:
            if is_pointing_down(target_angle):
                success = True
                break
            time.sleep(0.1)
            
        sense.set_rotation(0) # Reset rotation for messages
        
        if success:
            score += 1
            sense.show_message("Correct", text_colour=(0, 255, 0), scroll_speed=0.05)
        else:
            sense.show_message("Game Ends", text_colour=(255, 0, 0), scroll_speed=0.05)
            break

except KeyboardInterrupt:
    sense.set_rotation(0)
    pass

sense.set_rotation(0)
sense.show_message(f"Score: {score}", text_colour=(255, 255, 255), scroll_speed=0.05)
sense.clear()
