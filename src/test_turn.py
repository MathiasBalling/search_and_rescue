#!/usr/bin/env python3

from robot import EV3Robot


def main():
    robot = EV3Robot()
    robot.turn_deg(360)


if __name__ == "__main__":
    main()
