from math import atan2, degrees
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()
sense.set_imu_config(True, False, False)  # Enable compass only

def get_dir_string(heading):
    if heading < 45 or heading > 315:
        return "N"
    elif heading < 135 and heading >= 45:
        return "E"
    elif heading < 225 and heading >= 135:
        return "S"
    elif heading < 315 and heading >= 225:
        return "W"


def get_heading():
    raw = sense.get_compass_raw()
    heading = degrees(atan2(raw["y"], raw["x"]))
    if heading < 0:
        heading += 360
    return heading

try:
    while True:
        heading = get_heading()
        dir_str = get_dir_string(heading)
        sense.show_letter(dir_str[0], text_colour=[255, 0, 0])
        print(f"Heading: {heading:.2f} -> {dir_str}")
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

sense.clear()
