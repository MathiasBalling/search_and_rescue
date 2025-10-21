#!/usr/bin/env python3

from robot import EV3Robot
from behaviors.line_following.line_following import LineFollowing


def main():
    robot = EV3Robot()

    root = LineFollowing(robot)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
