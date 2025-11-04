from actuators import ActuatorsProposal
from ai.behaviors.behavior import Behavior
from sensors.colors import ColorSensors
from utils.blackboard import BlackBoard


class LineReturnBehavior(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors

    def update(self):
        # TODO: Update self.weight
        pass

    def actuators_proposal(self):
        # TODO:
        proposal = ActuatorsProposal(0, 0, False)

        return proposal
