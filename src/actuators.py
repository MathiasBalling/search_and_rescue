import ev3dev.ev3 as ev3
import time

from params import GRIPPER_SPEED, MOTOR_OFF


class ActuatorsProposal:
    def __init__(
        self,
        left_motor_speed: int,
        right_motor_speed: int,
        grip_object: bool,
    ):
        assert abs(left_motor_speed) <= 100
        assert abs(right_motor_speed) <= 100

        self.left_motor_speed = left_motor_speed
        self.right_motor_speed = right_motor_speed
        self.grip_object = grip_object

    def __str__(self):
        return (
            f"left_motor: {self.left_motor_speed}, right_motor: {self.right_motor_speed}, "
            f"gripper_open: {self.grip_object}"
        )


class Actuators:
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)
        self.gripper_motor = ev3.MediumMotor(ev3.OUTPUT_C)

        self.left_motor.run_direct()
        self.right_motor.run_direct()
        self.gripper_motor.run_direct()

    def do_proposal(self, proposal: ActuatorsProposal):
        self.left_motor.duty_cycle_sp = proposal.left_motor_speed

        self.right_motor.duty_cycle_sp = proposal.right_motor_speed

        if proposal.grip_object:
            self.grip_object()

    def grip_object(self):
        # FIX: New timing for the new gripper
        self.gripper_motor.duty_cycle_sp = GRIPPER_SPEED
        time.sleep(3)
        self.gripper_motor.duty_cycle_sp = -GRIPPER_SPEED
        time.sleep(3)
        self.gripper_motor.duty_cycle_sp = MOTOR_OFF
