import ev3dev.ev3 as ev3
import time

from dataclasses import dataclass

from params import GRIPPER_SPEED, MOTOR_OFF, TURN_TIME_PER_DEGREE


@dataclass
class WheelCommand:
    """
    Set the wheel speeds.
    """

    left_speed: int
    right_speed: int


@dataclass
class GripperCommand:
    """
    Does the gripping.
    """

    pass


@dataclass
class WheelGripperCommand:
    """
    Does the gripping and sets the wheel speeds.
    """

    left_speed: int
    right_speed: int


@dataclass
class TurnCommand:
    """
    Turns the robot the specified number of degrees.
    """

    ccw: bool
    deg: float


Command = WheelCommand | GripperCommand | WheelGripperCommand | TurnCommand


class ActuatorsProposal:
    def __init__(
        self,
        command: Command,
    ):
        self.command = command

    # def __str__(self):
    #     return (
    #         f"left_motor: {self.left_motor_speed}, right_motor: {self.right_motor_speed}, "
    #         f"gripper_open: {self.grip_object}"
    #     )


class Actuators:
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)
        self.gripper_motor = ev3.MediumMotor(ev3.OUTPUT_C)

        self.left_motor.run_direct()
        self.right_motor.run_direct()
        self.gripper_motor.run_direct()

    def do_proposal(self, proposal: ActuatorsProposal):
        cmd = proposal.command
        if isinstance(cmd, WheelCommand):
            self.left_motor.duty_cycle_sp = cmd.left_speed
            self.right_motor.duty_cycle_sp = cmd.right_speed
        elif isinstance(cmd, GripperCommand):
            self.left_motor.duty_cycle_sp = MOTOR_OFF
            self.right_motor.duty_cycle_sp = MOTOR_OFF
            self.grip_object()
        elif isinstance(cmd, WheelGripperCommand):
            self.left_motor.duty_cycle_sp = cmd.left_speed
            self.right_motor.duty_cycle_sp = cmd.right_speed
            self.grip_object()
        elif isinstance(cmd, TurnCommand):
            self.turn_deg(cmd.deg, cmd.ccw)

    def grip_object(self):
        # FIX: New timing for the new gripper
        self.gripper_motor.duty_cycle_sp = GRIPPER_SPEED
        time.sleep(4)
        self.gripper_motor.duty_cycle_sp = -GRIPPER_SPEED
        time.sleep(4)
        self.gripper_motor.duty_cycle_sp = MOTOR_OFF

    def turn_deg(self, deg, ccw):
        if ccw:
            self.set_wheel_duty_cycles(left=-40, right=40)
        else:
            self.set_wheel_duty_cycles(left=40, right=-40)

        sleep_time = TURN_TIME_PER_DEGREE * deg
        time.sleep(sleep_time)
        self.set_wheel_duty_cycles(left=MOTOR_OFF, right=MOTOR_OFF)

    def set_wheel_duty_cycles(self, left, right):
        self.left_motor.duty_cycle_sp = left
        self.right_motor.duty_cycle_sp = right
