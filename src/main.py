from robot import EV3Robot
from behavior_tree import Selector, Sequence
from behaviors.line_following.line_following import LineFollowing
from behaviors.can.can_detection import CanDetection
from behaviors.can.can_pickup import CanPickup
from behaviors.can.can_place import CanPlace


def main():
    robot = EV3Robot()

    # Leaf Behaviors
    # object_detection = CanDetection(robot)
    # object_pickup = CanPickup(robot)
    # object_place = CanPlace(robot)
    line_following = LineFollowing(robot)

    # Sub branches:
    # Follow the line until we find the object and then pick it up
    # TODO: Make these in "behaviors/"
    # object_find = Selector(
    #     [Sequence([object_detection, object_pickup]), line_following]
    # )
    # Follow the line until we are back at the start and then place the object
    # object_deliver = Selector([line_following, object_place])

    # Top branch:
    # 1. Find the can
    # 2. Deliver the can
    # root = Selector([object_find, object_deliver])

    root = line_following

    while True:
        root.tick()


if __name__ == "__main__":
    main()
