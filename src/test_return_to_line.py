#!/usr/bin/env python3

from behavior_tree import BlackBoard
from behaviors.line_following.return_to_line import ReturnToLine
from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()

    root = ReturnToLine(robot, blackboard)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
