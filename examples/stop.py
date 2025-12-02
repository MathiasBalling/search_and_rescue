#!/usr/bin/env python3
import time
import ev3dev.ev3 as ev3
import ev3dev2.sound as sound

sound = sound.Sound()
sound.speak("Patte hvad laver du?")

mL = ev3.LargeMotor(ev3.OUTPUT_A)
mR = ev3.LargeMotor(ev3.OUTPUT_D)
gm = ev3.MediumMotor(ev3.OUTPUT_C)
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
gm.run_direct()

mL.duty_cycle_sp = 0
mR.duty_cycle_sp = 0
gm.duty_cycle_sp = 0


# Results:
# Time since last update: 0.019732236862182617
# Min latency: 8.20159912109375e-05
# Max latency: 0.04648089408874512
