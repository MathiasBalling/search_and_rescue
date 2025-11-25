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

gyro = ev3.GyroSensor(ev3.INPUT_3)

assert mL.connected, "Motor A is not connected to port A"
assert mR.connected, "Motor B is not connected to port D"

assert cl_sensor_left.connected, "Color sensor is not connected to port 1"
assert cl_sensor_right.connected, "Color sensor is not connected to port 4"
assert us.connected, "Ultrasonic sensor is not connected to port 2"
assert gyro.connected, "Gyro sensor is not connected to port 3"


mL.run_direct()
mR.run_direct()

min_left, max_left = 100, 0
min_right, max_right = 100, 0

while True:
    print("left:", cl_sensor_left.value(), "right:", cl_sensor_right.value())
    if cl_sensor_left.value() < min_left:
        min_left = cl_sensor_left.value()
    if cl_sensor_left.value() > max_left:
        max_left = cl_sensor_left.value()
    if cl_sensor_right.value() < min_right:
        min_right = cl_sensor_right.value()
    if cl_sensor_right.value() > max_right:
        max_right = cl_sensor_right.value()
    print("min_left:", min_left, "max_left:", max_left)
    print("min_right:", min_right, "max_right:", max_right)
    time.sleep(0.5)
