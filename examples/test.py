from ev3dev2.sound import Sound
import ev3dev.ev3 as ev3
from time import sleep

import signal

# sound = Sound()
# sound.speak("death and destruction to all perkere")

mA = ev3.LargeMotor(ev3.OUTPUT_A)
mB = ev3.LargeMotor(ev3.OUTPUT_B)

assert mA.connected, "Motor A is not connected to port A"
assert mB.connected, "Motor B is not connected to port B"

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED_FORWARD = 100
BASE_SPEED_BACKWARD = -60
TURN_SPEED = 80

# TouchSensor = ev3.TouchSensor(ev3.INPUT_3)
color_sensor1 = ev3.ColorSensor(ev3.INPUT_1)
color_sensor2 = ev3.ColorSensor(ev3.INPUT_2)

color_sensor1.mode = "COL-COLOR"
color_sensor2.mode = "COL-COLOR"

# assert TouchSensor.connected, "Touch sensor is not connected to port 3"
assert color_sensor1.connected, "Color sensor 1 is not connected to port 1"
assert color_sensor2.connected, "Color sensor 2 is not connected to port 2"

mA.run_direct()
mB.run_direct()

colors = ["unknown", "black", "blue", "green", "yellow", "red", "white", "brown"]

while True:
    mA.duty_cycle_sp = BASE_SPEED_FORWARD
    mB.duty_cycle_sp = BASE_SPEED_FORWARD
    tou_val = TouchSensor.value()
    if tou_val == 1:
        mA.duty_cycle_sp = 0
        mB.duty_cycle_sp = 0
        break
    if (
        colors[color_sensor1.value()] == "white"
        and colors[color_sensor2.value()] == "white"
    ):
        mA.duty_cycle_sp = BASE_SPEED_FORWARD
        mB.duty_cycle_sp = BASE_SPEED_FORWARD
    elif colors[color_sensor1.value()] == "black":
        mA.duty_cycle_sp = BASE_SPEED_BACKWARD
        mB.duty_cycle_sp = TURN_SPEED
    elif colors[color_sensor2.value()] == "black":
        mA.duty_cycle_sp = TURN_SPEED
        mB.duty_cycle_sp = BASE_SPEED_BACKWARD

exit()
