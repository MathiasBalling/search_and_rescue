#!/usr/bin/env python3
import time
import ev3dev.ev3 as ev3
import ev3dev2.sound as sound

sound = sound.Sound()
sound.speak("Patte hvad laver du?")

mL = ev3.LargeMotor(ev3.OUTPUT_A)
mR = ev3.LargeMotor(ev3.OUTPUT_D)
# gm = ev3.MediumMotor(ev3.OUTPUT_C)
us = ev3.UltrasonicSensor(ev3.INPUT_2)
us.mode = "US-DIST-CM"

cl_sensor_left = ev3.ColorSensor(ev3.INPUT_1)
cl_sensor_left.mode = ev3.ColorSensor.MODE_COL_REFLECT

cl_sensor_right = ev3.ColorSensor(ev3.INPUT_4)
cl_sensor_right.mode = ev3.ColorSensor.MODE_COL_REFLECT


assert mL.connected, "Motor A is not connected to port A"
assert mR.connected, "Motor B is not connected to port D"

assert cl_sensor_left.connected, "Color sensor is not connected to port 1"
assert cl_sensor_right.connected, "Color sensor is not connected to port 4"
assert us.connected, "Ultrasonic sensor is not connected to port 2"


mL.run_direct()
mR.run_direct()

min_lat, max_lat = 99, 0

last = time.time()
while True:
    now = time.time()
    diff = now - last
    print("Time since last update:", diff)
    print("Min latency:", min_lat)
    print("Max latency:", max_lat)
    last = now
    if diff < min_lat:
        min_lat = diff
    if diff > max_lat:
        max_lat = diff

# Results:
# Time since last update: 0.019732236862182617
# Min latency: 8.20159912109375e-05
# Max latency: 0.04648089408874512
