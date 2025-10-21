#!/usr/bin/env python3

from behavior_tree import BlackBoard
from behaviors.can.can_detection import CanDetection
from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()

    root = CanDetection(robot, blackboard)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
