from abc import abstractmethod

from actuators import ActuatorsProposal
from utils.blackboard import BlackBoard


class Behavior:
    def __init__(self, blackboard: BlackBoard, weight: float = 0.0, priority=1.0):
        self.blackboard = blackboard
        self.priority = priority
        self.weight = weight

    @abstractmethod
    def update(self):
        """
        Updates weight of the behavior.
        """
        pass

    @abstractmethod
    def actuators_proposal(self) -> ActuatorsProposal:
        """
        Computes the control proposal for the behavior.
        """
        pass

    def get_weight(self) -> float:
        """
        Weight of the behavior.
        Returns the weight that determines if the behavior should be chosen.
        """
        return self.weight * self.priority

    def __str__(self):
        return self.__class__.__name__
