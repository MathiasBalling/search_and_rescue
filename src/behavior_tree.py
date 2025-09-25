from abc import ABC, abstractmethod
from typing import override

from enum import Enum, auto


class BTStatus(Enum):
    """
    Enumeration representing the possible statuses of a behavior tree node.
    """

    RUNNING = auto()
    SUCCESS = auto()
    FAILURE = auto()


class BTNode(ABC):
    """
    Abstract base class for all behavior tree nodes.
    """

    @abstractmethod
    def tick(self) -> BTStatus:
        """
        Executes one tick of the node.

        Returns:
            BTStatus: The status after executing the node.
        """
        pass


class Sequence(BTNode):
    """
    Composite node that ticks its children in order until one fails or is running.
    Returns SUCCESS only if all children return SUCCESS.
    """

    def __init__(self, children: list[BTNode]):
        """
        Args:
            children (list[Node]): The child nodes to execute in sequence.
        """
        self.children = children

    @override
    def tick(self) -> BTStatus:
        """
        Ticks each child node in sequence.

        Returns:
            BTStatus: The status of the first child that is not SUCCESS,
                      or SUCCESS if all children succeed.
        """
        for child in self.children:
            result = child.tick()

            # stop on FAILURE or RUNNING
            if result != BTStatus.SUCCESS:
                return result

        return BTStatus.SUCCESS


class Selector(BTNode):
    """
    Composite node that ticks its children in order until one succeeds or is running.
    Returns FAILURE only if all children return FAILURE.
    """

    def __init__(self, children: list[BTNode]):
        """
        Args:
            children (list[Node]): The child nodes to execute in selection.
        """
        self.children = children

    @override
    def tick(self):
        """
        Ticks each child node in order.

        Returns:
            BTStatus: The status of the first child that is not FAILURE,
                      or FAILURE if all children fail.
        """
        for child in self.children:
            result = child.tick()

            # stop on SUCCESS or RUNNING
            if result != BTStatus.FAILURE:
                return result

        return BTStatus.FAILURE


class Inverter(BTNode):
    """
    A decorator node that inverts the result of its child node.
    - SUCCESS becomes FAILURE
    - FAILURE becomes SUCCESS
    - RUNNING remains RUNNING
    """

    def __init__(self, child: BTNode):
        self.child = child

    @override
    def tick(self) -> BTStatus:
        """
        Ticks the child node and inverts its result.
        """
        result = self.child.tick()
        if result == BTStatus.SUCCESS:
            return BTStatus.FAILURE
        elif result == BTStatus.FAILURE:
            return BTStatus.SUCCESS
        return BTStatus.RUNNING


class Parallel(BTNode):
    """
    A composite node that ticks all children in parallel.
    Succeeds if at least `success_threshold` children succeed.
    Fails if at least `failure_threshold` children fail.
    Otherwise, returns RUNNING.
    """

    def __init__(
        self,
        children: list[BTNode],
        success_threshold: int,
        failure_threshold: int,
    ):
        self.children = children
        self.success_threshold = success_threshold or len(
            children
        )  # default: all must succeed
        self.failure_threshold = failure_threshold or 1  # default: fail if any fails

    @override
    def tick(self) -> BTStatus:
        """
        Ticks all children and counts successes and failures.
        Returns SUCCESS, FAILURE, or RUNNING based on thresholds.
        """
        successes = 0
        failures = 0
        for child in self.children:
            result = child.tick()
            if result == BTStatus.SUCCESS:
                successes += 1
            elif result == BTStatus.FAILURE:
                failures += 1

        if successes >= self.success_threshold:
            return BTStatus.SUCCESS
        if failures >= self.failure_threshold:
            return BTStatus.FAILURE
        return BTStatus.RUNNING


class DebugNode(BTNode):
    """
    A decorator node that prints the result of its child node for debugging.
    """

    def __init__(self, child: BTNode, name: str):
        self.child = child
        self.name = name

    @override
    def tick(self) -> BTStatus:
        """
        Ticks the child node, prints its result, and returns the result.
        """
        result = self.child.tick()
        print(self.name + ":" + str(result))
        return result
