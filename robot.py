#!/usr/bin/env python3
import wpilib
from commands2 import (
    TimedCommandRobot,
    CommandScheduler,
    Command,
    PrintCommand,
    RunCommand,
    InstantCommand,
    cmd,
)
from commands2.button import CommandXboxController
import drivetrain
import constants
from typing import Tuple, List

####
from followapriltag import FollowAprilTag
###


class MyRobot(TimedCommandRobot):
    """Class that defines the totality of our Robot"""

    def robotInit(self) -> None:
        """
        This method must eventually exit in order to ever have the robot
        code light turn green in DriverStation. So, this will create an
        instance of the Robot that contains all the subsystems,
        button bindings, and operator interface pieces like driver
        dashboards
        """
        # Setup the operator interface (typically CommandXboxController)
        self._driver_controller = CommandXboxController(0)
        # self.rangefinder = wpilib.AnalogInput(1)

        # Instantiate any subystems
        self._drivetrain: drivetrain.DriveTrain = drivetrain.DriveTrain()
        wpilib.SmartDashboard.putData("Drivetrain", self._drivetrain)

        # Setup the default commands for subsystems
        if wpilib.RobotBase.isSimulation():
            # Set the Drivetrain to arcade drive by default
            self._drivetrain.setDefaultCommand(
                # A split-stick arcade command, with forward/backward controlled by the left
                # hand, and turning controlled by the right.
                RunCommand(
                    lambda: self._drivetrain.drive_teleop(
                        -self._driver_controller.getRawAxis(
                            constants.CONTROLLER_FORWARD_SIM
                        ),
                        -self._driver_controller.getRawAxis(
                            constants.CONTROLLER_TURN_SIM
                        ),
                    ),
                    self._drivetrain,
                ).withName("DefaultDrive")
            )
        else:
            self._drivetrain.setDefaultCommand(
                # A split-stick arcade command, with forward/backward controlled by the left
                # hand, and turning controlled by the right.
                RunCommand(
                    lambda: self._drivetrain.drive_teleop(
                        -self._driver_controller.getRawAxis(
                            constants.CONTROLLER_FORWARD_REAL
                        ),
                        self._driver_controller.getRawAxis(
                            constants.CONTROLLER_TURN_REAL
                        ),
                    ),
                    self._drivetrain,
                ).withName("DefaultDrive")
            )

        self.__configure_button_bindings()
        self._auto_command = None

    def __configure_button_bindings(self) -> None:
        self._driver_controller.a().onTrue(
            drivetrain.DriveMMInches(self._drivetrain, 120)
        )
        self._driver_controller.x().onTrue(
            self._drivetrain.configure_turn_pid(90)
            .andThen(self._drivetrain.turn_with_pid())
            .withName("Turn 90")
        )
        self._driver_controller.b().onTrue(
            self._drivetrain.mm_drive_config(45)
            .andThen(self._drivetrain.mm_drive_distance())
            .withName("Drive 45")
        )

    def getAutonomousCommand(self) -> Command:
        # return PrintCommand("Default auto selected")
    ###
        return FollowAprilTag(self._drivetrain)
    ###

    def teleopInit(self) -> None:
        if self._auto_command is not None:
            self._auto_command.cancel()

    def testInit(self) -> None:
        CommandScheduler.getInstance().cancelAll()

    def autonomousInit(self) -> None:
        self._auto_command = self.getAutonomousCommand()

        if self._auto_command is not None:
            self._auto_command.schedule()

    def disabledPeriodic(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def testPeriodic(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        return super().teleopPeriodic()
