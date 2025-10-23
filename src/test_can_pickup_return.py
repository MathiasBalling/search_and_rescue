#!/usr/bin/env python3

from behaviors.line_following.line_following import LineFollowing
from blackboard import BlackBoard
from behaviors.can.can_detection import CanDetection
from behaviors.can.can_pickup import CanPickup
from behaviors.line_following.return_to_line import ReturnToLine
from behavior_tree import Condition, Inverter, Selector, Sequence

from params import setup_blackboard
from robot import EV3Robot


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()
    setup_blackboard(blackboard)

    line_following = LineFollowing(robot, blackboard)
    detection = CanDetection(robot, blackboard)
    pickup = CanPickup(robot, blackboard)
    return_to_line = ReturnToLine(robot, blackboard)

    def returned_to_line():
        return blackboard["returned_to_line"]

    root = Selector(
        [
            Condition(returned_to_line),
            Sequence([Inverter(line_following), detection, pickup, return_to_line]),
        ]
    )

    while True:
        root.tick()


if __name__ == "__main__":
    main()
