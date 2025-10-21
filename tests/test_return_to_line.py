#!/usr/bin/env python3

from behaviors.line_following.return_to_line import ReturnToLine
from robot import EV3Robot


def main():
    robot = EV3Robot()

    root = ReturnToLine(robot)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
