from sense_hat import SenseHat
import time
import random

sense = SenseHat()
sense.clear()

arrows = {
    "up": [
        0,0,0,1,1,0,0,0,
        0,0,1,1,1,1,0,0,
        0,1,0,1,1,0,1,0,
        1,0,0,1,1,0,0,1,
        0,0,0,1,1,0,0,0,
        0,0,0,1,1,0,0,0,
        0,0,0,1,1,0,0,0,
        0,0,0,1,1,0,0,0
    ],
    "down": [
        0,0,0,1,1,0,0,0,
        0,0,0,1,1,0,0,0,
        0,0,0,1,1,0,0,0,
        0,0,0,1,1,0,0,0,
        1,0,0,1,1,0,0,1,
        0,1,0,1,1,0,1,0,
        0,0,1,1,1,1,0,0,
        0,0,0,1,1,0,0,0
    ],
    "left": [
        0,0,0,1,0,0,0,0,
        0,0,1,0,0,0,0,0,
        0,1,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,
        0,1,0,0,0,0,0,0,
        0,0,1,0,0,0,0,0,
        0,0,0,1,0,0,0,0
    ],
    "right": [
        0,0,0,0,1,0,0,0,
        0,0,0,0,0,1,0,0,
        0,0,0,0,0,0,1,0,
        1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,
        0,0,0,0,0,0,1,0,
        0,0,0,0,0,1,0,0,
        0,0,0,0,1,0,0,0
    ]
}

def draw_arrow(direction, color):
    pixels = []
    for pixel in arrows[direction]:
        if pixel == 1:
            pixels.append(color)
        else:
            pixels.append((0,0,0))
    sense.set_pixels(pixels)

score = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

try:
    while True:
        target_dir = random.choice(list(arrows.keys()))
        color = random.choice(colors)
        draw_arrow(target_dir, color)
        
        event = sense.stick.wait_for_event()
        if event.action == "pressed":
            if event.direction == target_dir:
                score += 1
                sense.clear(0, 255, 0)
            else:
                sense.clear(255, 0, 0)
                time.sleep(1)
                break
        time.sleep(0.2)
except KeyboardInterrupt:
    pass

sense.show_message(f"Score: {score}")
sense.clear()
