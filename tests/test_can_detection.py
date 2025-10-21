#!/usr/bin/env python3

from behaviors.can.can_detection import CanDetection
from robot import EV3Robot


def main():
    robot = EV3Robot()

    root = CanDetection(robot)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
