#!/usr/bin/env python3

from blackboard import BlackBoard
from behaviors.can.can_pickup import CanPickup
from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()

    root = CanPickup(robot, blackboard)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
