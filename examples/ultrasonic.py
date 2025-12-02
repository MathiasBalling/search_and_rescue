#!/usr/bin/env python3
import time
import ev3dev.ev3 as ev3


mL = ev3.LargeMotor(ev3.OUTPUT_A)
mR = ev3.LargeMotor(ev3.OUTPUT_D)
us = ev3.UltrasonicSensor(ev3.INPUT_2)
us.mode = ev3.UltrasonicSensor.MODE_US_DIST_CM
# us.mode = ev3.UltrasonicSensor.MODE_US_SI_CM

assert mL.connected, "Motor A is not connected to port A"
assert mR.connected, "Motor B is not connected to port D"

assert us.connected, "Ultrasonic sensor is not connected to port 2"


mL.run_direct()
mR.run_direct()


last = time.time()
while True:
    print(us.distance_centimeters)
