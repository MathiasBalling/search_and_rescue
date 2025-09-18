#!/usr/bin/env python3
from ev3dev2.sound import Sound
import ev3dev.ev3 as ev3
from time import sleep

import signal

# sound = Sound()
# sound.speak("death and destruction to all perkere")

mA = ev3.LargeMotor('outA')
mB = ev3.LargeMotor('outB')

assert mA.connected, "Motor A is not connected to port A"
assert mB.connected, "Motor B is not connected to port B"

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED_FORWARD = 100
BASE_SPEED_BACKWARD = -60
TURN_SPEED = 80

#TouchSensor = ev3.TouchSensor('in3')


mA.run_direct()
mB.run_direct()

while True:
    mA.duty_cycle_sp = BASE_SPEED_FORWARD
    mB.duty_cycle_sp = BASE_SPEED_FORWARD
    sleep(2)
    mA.duty_cycle_sp = BASE_SPEED_BACKWARD
    mB.duty_cycle_sp = BASE_SPEED_BACKWARD
    sleep(2)
    mA.duty_cycle_sp = 0
    mB.duty_cycle_sp = 0
    break
