from actuators import ActuatorsProposal, WheelCommand
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
        # TODO: Update self.weight and blackboard[returned_to_line]
        pass

    def actuators_proposal(self):
        # TODO:
        proposal = ActuatorsProposal(WheelCommand(0, 0))

        return proposal

    def line_return(self):
        return WheelCommand(0, 0)
