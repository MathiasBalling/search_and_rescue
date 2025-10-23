#!/usr/bin/env python3

from blackboard import BlackBoard
from robot import EV3Robot
from behaviors.line_following.line_following import LineFollowing


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()

    root = LineFollowing(robot, blackboard)

    while True:
        root.tick()

        


if __name__ == "__main__":
    main()
