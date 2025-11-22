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
mL.duty_cycle_sp = 20


for i in range(100):
    print(mL.count_per_rot, mL.position, mL.speed)
