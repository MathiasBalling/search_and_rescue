#!/usr/bin/env python3

from behaviors.can.can_place import CanPlace
from robot import EV3Robot


def main():
    robot = EV3Robot()

    root = CanPlace(robot)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
