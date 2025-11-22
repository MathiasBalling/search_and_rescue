from actuators import Actuators
from ai.arbitrator import Arbitrator
from ai.behaviors.behavior import Behavior
from params import DT
from sensors.sensor import Sensor

import time


class Controller:
    def __init__(self, actuators):
        self.sensors = []
        self.behaviors = []
        self.actuators = actuators
        self.arbitrator = Arbitrator(self)

    def add_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)

    def add_behavior(self, behavior: Behavior):
        self.behaviors.append(behavior)

    def step(self):
        """
        Steps the controller. No timing!
        """
        for sensor in self.sensors:
            sensor.update()

        for behavior in self.behaviors:
            behavior.update()

        proposal = self.arbitrator.choose_proposal_competitive()

        self.actuators.do_proposal(proposal)

    def run(self):
        """
        Runs the controller in DT time steps forever.
        """
        last_update_time = time.time()
        while True:
            # Sleep until the next update
            current_time = time.time()

            if (current_time - last_update_time) < DT:
                time.sleep(DT - (current_time - last_update_time))

            last_update_time = current_time

            self.step()
