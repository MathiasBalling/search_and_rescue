#!/usr/bin/env python3
from math import pi
import math
import time
import ev3dev.ev3 as ev3
import ev3dev2.sound as sound

from params import WHEEL_RADIUS

sound = sound.Sound()
sound.speak("What the hell Claudia Claudia Claudia")

mL = ev3.LargeMotor(ev3.OUTPUT_A)
mR = ev3.LargeMotor(ev3.OUTPUT_D)
# gm = ev3.MediumMotor(ev3.OUTPUT_C)

cl_sensor_left = ev3.ColorSensor(ev3.INPUT_1)
cl_sensor_left.mode = ev3.ColorSensor.MODE_COL_REFLECT

cl_sensor_right = ev3.ColorSensor(ev3.INPUT_4)
cl_sensor_right.mode = ev3.ColorSensor.MODE_COL_REFLECT


assert mL.connected, "Motor A is not connected to port A"
assert mR.connected, "Motor B is not connected to port D"

assert cl_sensor_left.connected, "Color sensor is not connected to port 1"
assert cl_sensor_right.connected, "Color sensor is not connected to port 4"

mL.run_forever()
mL.stop_action = ev3.LargeMotor.STOP_ACTION_BRAKE
mR.run_forever()
mR.stop_action = ev3.LargeMotor.STOP_ACTION_BRAKE


def dps_to_mps(dps):
    return dps * math.pi / 180 * 0.0275


def mps_to_dps(mps):
    dps = mps * 180 / math.pi / 0.0275
    return round(max(0, min(dps, mL.max_speed)))


mL.speed_sp = mps_to_dps(0.1)
mR.speed_sp = mps_to_dps(0.1)

print("Max speed (deg/s):", mL.max_speed, "Max speed (m/s):", dps_to_mps(mL.max_speed))

for i in range(10):
    time.sleep(0.1)
    print("ang speed L:", mL.speed, "linear speed:", dps_to_mps(mL.speed))
    print("ang speed R:", mR.speed, "linear speed:", dps_to_mps(mR.speed))


print("Stopping")
mL.stop()
mR.stop()


time.sleep(2.0)


print("Setpoint after stop")
print(mL.speed_sp, mR.speed_sp)
mL.speed_sp = mps_to_dps(0.1)
mR.speed_sp = mps_to_dps(0.1)
print(mL.speed_sp, mR.speed_sp)

time.sleep(2.0)

print("Run forever")
mL.run_forever()
mR.run_forever()
print(mL.speed_sp, mR.speed_sp)

time.sleep(2.0)

print("Stop action brake")
mL.stop()
mR.stop()
