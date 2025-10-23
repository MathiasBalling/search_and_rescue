#!/usr/bin/env python3

from blackboard import BlackBoard
from behaviors.can.can_place import CanPlace
from params import setup_blackboard
from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()
    setup_blackboard(blackboard)

    root = CanPlace(robot, blackboard)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
