# Sense HAT Development Log Book

**Total Expected Working Hours:** 9 hours

## Hour 1-2: Environment Setup & Planning
* Set up the Sense HAT environment
* Installed `sense-hat`
* Checked basic LED matrix and sensor access

## Hour 3-5: Snake Game Development (`sense_hat_snake.py`)
* Created the `SenseHat()` instance and snake data
* Added joystick controls for movement
* Handled wrap-around movement, apple collection, and self-collision
* Added game over handling and screen clear

## Hour 6-7: Arrow Orientation Game Development (`sense_hat_arrow.py`)
* Created the arrow sprite and rotated it on the LED matrix
* Randomly selected a target direction
* Used accelerometer data to check the tilt
* Added score updates and success or failure messages
* Displayed the final score

## Hour 8-9: Compass Application Development & Finalization (`sense_hat_compass.py`)
* Enabled compass-only readings
* Read raw magnetometer data and converted it to a heading
* Mapped the heading to N, E, S, and W
* Added real time update for the direction letter
* Increased tick rate to get a faster response

