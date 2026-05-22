from sense_hat import SenseHat
import time
import random

sense = SenseHat()
sense.clear()

snake = [(3, 3)]
direction = "right"
apple = (random.randint(0, 7), random.randint(0, 7))

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

def draw():
    sense.clear()
    sense.set_pixel(apple[0], apple[1], RED)
    for segment in snake:
        sense.set_pixel(segment[0], segment[1], GREEN)

def move():
    global apple
    head = snake[0]
    
    if direction == "up":
        new_head = (head[0], (head[1] - 1) % 8)
    elif direction == "down":
        new_head = (head[0], (head[1] + 1) % 8)
    elif direction == "left":
        new_head = ((head[0] - 1) % 8, head[1])
    elif direction == "right":
        new_head = ((head[0] + 1) % 8, head[1])
        
    snake.insert(0, new_head)
    
    if new_head == apple:
        apple = (random.randint(0, 7), random.randint(0, 7))
    else:
        snake.pop()
        
    if new_head in snake[1:]:
        return False
    return True

def handle_joystick(event):
    global direction
    if event.action == "pressed":
        if event.direction == "up" and direction != "down":
            direction = "up"
        elif event.direction == "down" and direction != "up":
            direction = "down"
        elif event.direction == "left" and direction != "right":
            direction = "left"
        elif event.direction == "right" and direction != "left":
            direction = "right"

sense.stick.direction_any = handle_joystick

running = True
try:
    while running:
        draw()
        running = move()
        time.sleep(0.3)
except KeyboardInterrupt:
    pass

sense.show_message("Game Over")
sense.clear()
