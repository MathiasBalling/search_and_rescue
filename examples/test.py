#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep
import ev3dev2.sound as sound
import signal

sound = sound.Sound()
sound.speak("Patte hvad laver du?")

mA = ev3.LargeMotor(ev3.OUTPUT_A)
mB = ev3.LargeMotor(ev3.OUTPUT_B)
# gm = ev3.MediumMotor(ev3.OUTPUT_C)
us = ev3.UltrasonicSensor(ev3.INPUT_2)
cl_sensor_right = ev3.ColorSensor(ev3.INPUT_4)
cl_sensor_left = ev3.ColorSensor(ev3.INPUT_3)
us.mode = "US-DIST-CM"

assert mA.connected, "Motor A is not connected to port A"
assert mB.connected, "Motor B is not connected to port B"
# assert gm.connected, "Gripper motor is not connected to port C"
assert us.connected, "Ultrasonic sensor is not connected to port 2"
assert cl_sensor_right.connected, "Color sensor right is not connected to port 4"
assert cl_sensor_left.connected, "Color sensor left is not connected to port 3"

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED_FORWARD = -100
SLOWER_SPEED_FORWARD = -50
BASE_SPEED_BACKWARD = 60
TURN_SPEED = 80


mA.run_direct()
mB.run_direct()
# gm.run_direct()

cl_sensor_left.mode = ev3.ColorSensor.MODE_COL_REFLECT
cl_sensor_right.mode = ev3.ColorSensor.MODE_COL_REFLECT

while True:
    # mA.duty_cycle_sp = BASE_SPEED_FORWARD
    # mB.duty_cycle_sp = BASE_SPEED_FORWARD
    distance = us.value() / 10
    print(
        "Can detected at distance:",
        distance,
        "cm",
        "Left color sensor:",
        cl_sensor_left.value(),
        "Right color sensor:",
        cl_sensor_right.value(),
    )
    # if distance < 20:
    # mA.duty_cycle_sp = SLOWER_SPEED_FORWARD
    # mB.duty_cycle_sp = SLOWER_SPEED_FORWARD
    # if distance < 5:
    #     mA.duty_cycle_sp = 0
    #     mB.duty_cycle_sp = 0

    #     sleep(1)
    #     print("done")
    #     break
    # else:
    #     mA.duty_cycle_sp = 20
    #     mB.duty_cycle_sp = -20


exit()
