# Motor class, for managing a SINGLE motor

import SocketCanPort as scp
import CiA402SetupData as CiA402sd
import Cia402device as Cia402d
import json as js
import os
import numpy as np


class Motor:

    def __init__(self, idMotor, nameFile):

        with open(
            os.path.dirname(os.path.realpath(__file__)) + "/" + nameFile
        ) as articulationFile:
            config = js.load(articulationFile)

        self.pm = scp.SocketCanPort(config["canPort"])

        self.sd = CiA402sd.CiA402SetupData(
            config["new_encRes"],
            config["new_mlRatio"],
            config["new_SampSL"],
            config["motor_current_limit"],
            config["drive_current_limit"]
        )

        # Create an instance of the Cia402d library
        self.motor = Cia402d.CiA402Device(
            idMotor,
            self.pm,
            self.sd
        )

        # ============================================================
        # Motor communication / state
        # ============================================================

        self.started = False
        self.enabled = False

        # ============================================================
        # Operation mode
        # ============================================================

        # Possible values:
        #   None
        #   "position"
        #   "velocity"
        #   "torque"
        self.operation_mode = None

        # ============================================================
        # Synchronize state with the physical drive
        # ============================================================
        
        self.updateState()

    # ================================================================
    # Motor communication / state
    # ================================================================

    def updateState(self):

        # ------------------------------------------------------------
        # Read CiA402 Statusword (6041h)
        # ------------------------------------------------------------
        status = self.motor.GetStatus()

        # Mask used to identify the CiA402 state
        state = status & 0x006F

        # Operation Enabled
        self.enabled = (state == 0x0027)

        # ------------------------------------------------------------
        # Read Mode of Operation Display (6061h)
        # ------------------------------------------------------------
        mode = self.motor.GetOperationMode()

        if mode == 1:
            self.operation_mode = "position"

        elif mode == 3:
            self.operation_mode = "velocity"

        elif mode == 4:
            self.operation_mode = "torque"

        else:
            self.operation_mode = None

        # For now, communication with the drive is enough to consider
        # the motor available.
        self.started = True

        # ------------------------------------------------------------
        # DEBUG: show actual state read from the drive
        # ------------------------------------------------------------
        # print(
        #     "State:",
        #     "started =", self.started,
        #     "enabled =", self.enabled,
        #     "mode =", self.operation_mode
        # )


        return 0


    def startMotor(self):

        # Synchronize software state with the physical drive
        self.updateState()

        # Motor is already enabled
        if self.enabled:
            return 0

        # If the motor is not enabled, perform the normal startup sequence
        result = self.motor.Reset()

        if result != 0:
            self.started = False
            self.enabled = False
            return result

        self.started = True

        result = self.motor.SwitchOn()

        if result != 0:
            self.enabled = False
            return result

        self.enabled = True

        return 0


    def stopMotor(self):

        result = self.motor.SwitchOff()

        if result == 0:
            self.enabled = False

        return result


    # ================================================================
    # Operation mode
    # ================================================================

    def setupPositionMode(self, vel, accel):

        if not self.started or not self.enabled:
            raise RuntimeError(
                "Motor must be started and enabled before "
                "selecting Position Mode."
            )

        # Already in Position Mode
        if self.operation_mode == "position":
            print("Position Mode already configured.")
            return 0

        # Change to Position Mode
        result = self.motor.SetupPositionMode(
            vel,
            accel
        )

        if result == 0:
            self.operation_mode = "position"

        return result

    def Setup_Velocity_Mode(self, acceleration, target):

        if not self.started or not self.enabled:
            raise RuntimeError(
                "Motor must be started and enabled before "
                "selecting Velocity Mode."
            )

        # Already in Velocity Mode
        if self.operation_mode == "velocity":
            print("Velocity Mode already configured.")
            return 0

        # Change to Velocity Mode
        result = self.motor.Setup_Velocity_Mode(
            acceleration,
            target
        )

        if result == 0:
            self.operation_mode = "velocity"

        return result

    def Setup_Torque_Mode(self, torque_slope=1000):

        if not self.started or not self.enabled:
            raise RuntimeError(
                "Motor must be started and enabled before "
                "selecting Torque Mode."
            )

        # ============================================================
        # Configure Torque Slope
        #
        # torque_slope corresponds to object 6087h.
        #
        # 1000 = 100% of motor rated current per second
        #
        # With motor rated current 6075h = 823 mA:
        #   1000 -> 0.823 A/s
        #    500 -> 0.4115 A/s
        #    200 -> 0.1646 A/s
        #
        # Example:
        #   Setup_Torque_Mode(1000)
        # ============================================================

        # Already in Torque Mode
        if self.operation_mode == "torque":
            print("Torque Mode already configured.")
            return 0

        result = self.motor.Setup_Torque_Mode(torque_slope)

        if result == 0:
            self.operation_mode = "torque"

        return result
    
    # ================================================================
    # Position
    # ================================================================

    def setPosition(self, theta):

        return self.motor.SetPosition(theta)


    def getPosition(self):

        return self.motor.GetPosition()


    # ================================================================
    # Velocity
    # ================================================================

    def setVelocity(self, velocity):

        return self.motor.SetVelocity(velocity)


    def getVelocity(self):

        return self.motor.GetVelocity()


    # ================================================================
    # Current
    # ================================================================

    def getAmp(self):

        return self.motor.GetAmps()


    def getFilteredAmps(self, n_samples):

        data = []

        for _ in range(n_samples):
            data.append(self.motor.GetAmps())

        data = np.array(data)

        print(data)

        return np.mean(data)


    # ================================================================
    # Torque
    # ================================================================

    def SetTorque(self, torq):

        return self.motor.SetTorque(torq)


    # ================================================================
    # State information
    # ================================================================

    def isStarted(self):

        return self.started


    def isEnabled(self):

        return self.enabled


    def getOperationMode(self):

        return self.operation_mode


    def getState(self):

        return {
            "started": self.started,
            "enabled": self.enabled,
            "operation_mode": self.operation_mode
        }