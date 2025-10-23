#!/usr/bin/env python3

from blackboard import BlackBoard
from behaviors.can.can_detection import CanDetection
from behaviors.can.can_pickup import CanPickup
from behaviors.line_following.return_to_line import ReturnToLine
from behavior_tree import Selector, Sequence

from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()
    detection = CanDetection(robot, blackboard)
    pickup = CanPickup(robot, blackboard)
    return_to_line = ReturnToLine(robot, blackboard)

    root = Sequence([detection, pickup, return_to_line])

    while True:
        root.tick()


if __name__ == "__main__":
    main()
