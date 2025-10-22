#!/usr/bin/env python3

from behaviors.line_following.return_to_line import ReturnToLine
from robot import EV3Robot
from blackboard import BlackBoard
from behavior_tree import Selector, Sequence
from behaviors.line_following.line_following import LineFollowing
from behaviors.can.can_detection import CanDetection
from behaviors.can.can_pickup import CanPickup
from behaviors.can.can_place import CanPlace


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()

    # Leaf Behaviors
    object_detection = CanDetection(robot, blackboard)
    object_pickup = CanPickup(robot, blackboard)
    object_place = CanPlace(robot, blackboard)
    line_following = LineFollowing(robot, blackboard)
    return_to_line = ReturnToLine(robot, blackboard)

    # Sub branches:
    # Follow the line until we find the object and then pick it up
    # TODO: Make these in "behaviors/"
    object_find = Selector(
        [line_following, Sequence([object_detection, object_pickup])]
    )
    # Follow the line until we are back at the start and then place the object
    object_deliver = Sequence(
        [return_to_line, Selector([line_following, object_place])]
    )

    # Top branch:
    # 1. Find the can
    # 2. Deliver the can
    root = Selector([object_find, object_deliver])

    # root = LineFollowing(robot)

    while True:
        root.tick()


if __name__ == "__main__":
    main()
