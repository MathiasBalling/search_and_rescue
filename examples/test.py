#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep

import signal

# sound = Sound()
# sound.speak("death and destruction to all perkere")

mA = ev3.LargeMotor(ev3.OUTPUT_A)
mB = ev3.LargeMotor(ev3.OUTPUT_B)
# gm = ev3.MediumMotor(ev3.OUTPUT_C)
us = ev3.UltrasonicSensor(ev3.INPUT_4)
us.mode = 'US-DIST-CM'

assert mA.connected, "Motor A is not connected to port A"
assert mB.connected, "Motor B is not connected to port B"
# assert gm.connected, "Gripper motor is not connected to port C"

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED_FORWARD = -100
SLOWER_SPEED_FORWARD = -50
BASE_SPEED_BACKWARD = 60
TURN_SPEED = 80


mA.run_direct()
mB.run_direct()
# gm.run_direct()

while True:
    # mA.duty_cycle_sp = BASE_SPEED_FORWARD
    # mB.duty_cycle_sp = BASE_SPEED_FORWARD
    distance = us.value() / 10
    print("Can detected at distance:", distance, "cm")
    if distance < 20:
        mA.duty_cycle_sp = SLOWER_SPEED_FORWARD
        mB.duty_cycle_sp = SLOWER_SPEED_FORWARD
        if distance < 5:
            mA.duty_cycle_sp = 0
            mB.duty_cycle_sp = 0
            # gm.duty_cycle_sp = 50
            # sleep(3)
            # gm.duty_cycle_sp = -50
            # sleep(5)
            # gm.duty_cycle_sp = 0
            # sleep(1)
            # gm.duty_cycle_sp = 50
            # sleep(1)
            # gm.duty_cycle_sp = 0
            # sleep(1)
            # mA.duty_cycle_sp = BASE_SPEED_BACKWARD
            # mB.duty_cycle_sp = BASE_SPEED_BACKWARD
            sleep(1)
            print("done")
            break
    else:
        mA.duty_cycle_sp = 20
        mB.duty_cycle_sp = -20
  

exit()
