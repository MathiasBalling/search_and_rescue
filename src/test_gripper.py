#!/usr/bin/env python3

from blackboard import BlackBoard
from behaviors.can.can_place import CanPlace
from robot import EV3Robot
import time


def main():
    robot = EV3Robot()
    # robot.close_gripper()
    # time.sleep(5)
    robot.open_gripper()


if __name__ == "__main__":
    main()
