#!/usr/bin/env python3

from blackboard import BlackBoard
from behaviors.can.can_place import CanPlace
from robot import EV3Robot


def main():
    robot = EV3Robot()
    robot.close_gripper()
    robot.open_gripper()


if __name__ == "__main__":
    main()
