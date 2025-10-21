#!/usr/bin/env python3

from behavior_tree import BlackBoard
from behaviors.can.can_place import CanPlace
from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()

    root = CanPlace(robot, blackboard)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
