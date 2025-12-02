#!/usr/bin/env python3
import time
import ev3dev.ev3 as ev3
import ev3dev2.sound as sound


cl_sensor_left = ev3.ColorSensor(ev3.INPUT_1)
cl_sensor_left.mode = ev3.ColorSensor.MODE_COL_REFLECT

cl_sensor_right = ev3.ColorSensor(ev3.INPUT_4)
cl_sensor_right.mode = ev3.ColorSensor.MODE_COL_REFLECT

light_sensor = ev3.LightSensor(ev3.INPUT_3)
light_sensor.mode = ev3.LightSensor.MODE_REFLECT

assert cl_sensor_left.connected, "Color sensor is not connected to port 1"
assert cl_sensor_right.connected, "Color sensor is not connected to port 4"
assert light_sensor.connected, "Light sensor is not connected to port 3"


min_left, max_left = 100, 0
min_middle, max_middle = 100, 0
min_right, max_right = 100, 0

while True:
    print(
        "middle:",
        light_sensor.value(),
        "left:",
        cl_sensor_left.value(),
        "right:",
        cl_sensor_right.value(),
    )


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
