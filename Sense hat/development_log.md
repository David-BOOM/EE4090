# Sense HAT Development Log Book

**Total Expected Working Hours:** 9 hours

## Hour 1-2: Environment Setup & Planning
* Researched official Raspberry Pi Sense HAT library API documentation
* Verified package requirements (avoiding deprecated modules)
* Executed environment setup (`sudo apt-get update && sudo apt-get install -y sense-hat`)
* Validated basic LED matrix and sensor accessibility

## Hour 3-5: Snake Game Development (`sense_hat_snake.py`)
* Initialized `SenseHat()` instance and matrix rendering logic
* Designed data structures for Snake segments (tuple coordinates) and Apple generation
* Implemented `handle_joystick(event)` using `sense.stick.direction_any` for responsive movement mapping
* Coded collision detection (walls, self-collision) logic
* Handled game loop timing with `time.sleep()` for pacing
* Ensured graceful exit on execution interruption (`KeyboardInterrupt` -> `sense.clear()`)
* Conducted functional testing & code review

## Hour 6-7: Random Arrow Game Development (`sense_hat_arrow.py`)
* Created specific 8x8 pixel mappings (1s and 0s) for cardinal directional arrows (Up, Down, Left, Right)
* Added logic to randomly select arrow direction and display colors dynamically
* Programmed blocking input wait (`sense.stick.wait_for_event()`) for user response loop
* Created score increment logic and visual success (Green screen) / failure (Red screen) indicators
* Show final score natively on LED matrix using `sense.show_message`
* Verified logic boundaries and code safety

## Hour 8-9: Compass Application Development & Finalization (`sense_hat_compass.py`)
* Interfaced with hardware magnetometer via `sense.set_imu_config(False, True, False)` to isolate compass readings and prevent drift calculation overlaps
* Pulled heading data (0-360 degrees) using `sense.get_compass()`
* Implemented range-mapping logic to translate degrees into abbreviated cardinal direction strings (N, NE, E, SE, etc.)
* Mapped output to display single initial character on matrix (`sense.show_letter`)
* Standardized graceful shutdown operations across all three applications
* Performed deep final review to verify no bugs existed prior to shipping

