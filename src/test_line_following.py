#!/usr/bin/env python3

from time import time
from blackboard import BlackBoard
from params import setup_blackboard
from robot import EV3Robot
from behaviors.line_following.line_following import LineFollowing


def main():
    robot = EV3Robot()
    blackboard = BlackBoard()
    setup_blackboard(blackboard)

    root = LineFollowing(robot, blackboard)

    while True:
        blackboard["last_time_line_seen"] = time()
        root.tick()



if __name__ == "__main__":
    main()
