import ev3dev.ev3 as ev3
import time

from params import GRIPPER_SPEED, MOTOR_OFF, TURN_TIME_PER_DEGREE


from typing import Union


class WheelCommand:
    """
    Set the wheel speeds.
    """

    def __init__(self, left_speed, right_speed):
        self.left_speed = left_speed
        self.right_speed = right_speed


class GripperCommand:
    """
    Does the gripping.
    """

    pass


class WheelGripperCommand:
    """
    Does the gripping and sets the wheel speeds.
    """

    def __init__(self, left_speed, right_speed):
        self.left_speed = left_speed
        self.right_speed = right_speed


class TurnCommand:
    """
    Turns the robot the specified number of degrees.
    """

    def __init__(self, deg, ccw):
        self.deg = deg
        self.ccw = ccw


class NoCommand:
    """
    Turns the robot the specified number of degrees.
    """

    def __init__(self):
        pass


Command = Union[
    WheelCommand, GripperCommand, WheelGripperCommand, TurnCommand, NoCommand
]


class ActuatorsProposal:
    def __init__(
        self,
        command,
    ):
        self.command = command

    def __str__(self):
        if isinstance(self.command, WheelCommand):
            return "left_motor: {}, right_motor: {}".format(
                self.command.left_speed, self.command.right_speed
            )
        elif isinstance(self.command, GripperCommand):
            return "grip"
        elif isinstance(self.command, WheelGripperCommand):
            return "left_motor: {}, right_motor: {}, grip".format(
                self.command.left_speed, self.command.right_speed
            )
        elif isinstance(self.command, TurnCommand):
            return "turn_deg: {}, turn_ccw: {}".format(
                self.command.deg, self.command.ccw
            )
        else:
            return "Unknown command"


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
        self.gripper_motor.duty_cycle_sp = -GRIPPER_SPEED
        time.sleep(4)
        self.gripper_motor.duty_cycle_sp = GRIPPER_SPEED
        time.sleep(4)
        self.gripper_motor.duty_cycle_sp = MOTOR_OFF

    def turn_deg(self, deg, ccw):
        print(deg)
        if ccw:
            self.set_wheel_duty_cycles(left=-40, right=40)
        else:
            self.set_wheel_duty_cycles(left=40, right=-40)

        sleep_time = 0.02222 * deg
        time.sleep(sleep_time)
        self.set_wheel_duty_cycles(left=MOTOR_OFF, right=MOTOR_OFF)

    def set_wheel_duty_cycles(self, left, right):
        self.left_motor.duty_cycle_sp = left
        self.right_motor.duty_cycle_sp = right
