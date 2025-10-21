#!/usr/bin/env python3

from behaviors.can.can_pickup import CanPickup
from robot import EV3Robot


def main():
    robot = EV3Robot()

    root = CanPickup(robot)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
