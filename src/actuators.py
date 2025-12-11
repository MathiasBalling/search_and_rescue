import ev3dev.ev3 as ev3
import time
import atexit

from params import (
    GRIPPER_SPEED,
    MOTOR_OFF,
    mps_to_dps,
)


from typing import Union


class WheelCommand:
    """
    Set the wheel speeds.
    """

    def __init__(self, left_speed, right_speed):
        self.left_speed = mps_to_dps(left_speed)
        self.right_speed = mps_to_dps(right_speed)


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
        self.left_speed = mps_to_dps(left_speed)
        self.right_speed = mps_to_dps(right_speed)


class StopCommand:
    """
    Turns the robot the specified number of degrees.
    """

    def __init__(self):
        pass


Command = Union[WheelCommand, GripperCommand, WheelGripperCommand, StopCommand]


class ActuatorsProposal:
    def __init__(
        self,
        command: Command,
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
        elif isinstance(self.command, StopCommand):
            return "stop"
        else:
            return "Unknown command"


def ctrl_c():
    print("End time: ", time.time())
    Actuators().stop_motors()


atexit.register(ctrl_c)


class Actuators:
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)
        assert self.left_motor.connected
        assert self.right_motor.connected

        self.gripper_motor = ev3.MediumMotor(ev3.OUTPUT_C)
        assert self.gripper_motor.connected
        self.gripper_motor.run_direct(duty_cycle_sp=MOTOR_OFF)

    def do_proposal(self, proposal: ActuatorsProposal):
        cmd = proposal.command
        if isinstance(cmd, WheelCommand):
            self.left_motor.run_forever(speed_sp=cmd.left_speed)

            self.right_motor.run_forever(speed_sp=cmd.right_speed)
        elif isinstance(cmd, GripperCommand):
            self.stop_motors()
            self.grip_object()
        elif isinstance(cmd, WheelGripperCommand):
            self.left_motor.run_forever(speed_sp=cmd.left_speed)
            self.right_motor.run_forever(speed_sp=cmd.right_speed)
            self.grip_object()
        elif isinstance(cmd, StopCommand):
            self.stop_motors()

    def grip_object(self):
        self.gripper_motor.run_direct(duty_cycle_sp=-GRIPPER_SPEED)
        time.sleep(3.5)
        self.gripper_motor.run_direct(duty_cycle_sp=GRIPPER_SPEED)
        time.sleep(3.5)
        self.gripper_motor.stop(stop_action=ev3.MediumMotor.STOP_ACTION_BRAKE)

    def get_wheel_motors(self):
        return self.left_motor, self.right_motor

    def stop_motors(self):
        self.left_motor.stop(stop_action=ev3.LargeMotor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.LargeMotor.STOP_ACTION_BRAKE)
        self.gripper_motor.stop(stop_action=ev3.MediumMotor.STOP_ACTION_BRAKE)
