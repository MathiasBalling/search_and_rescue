from actuators import ActuatorsProposal, WheelCommand


class Arbitrator:
    def __init__(self, controller):
        self.controller = controller

    def choose_proposal_competitive(self) -> ActuatorsProposal:
        best_behavior = max(self.controller.behaviors, key=lambda b: b.get_weight())
        proposal = best_behavior.actuators_proposal()
        # print("{}: {}".format(best_behavior, proposal))

        return proposal

    def choose_proposal_cooperative(self) -> ActuatorsProposal:
        # TODO: Make if it makes sense to have more than one behavior
        return ActuatorsProposal(WheelCommand(0, 0))
