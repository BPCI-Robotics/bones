# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       wesle                                                        #
# 	Created:      7/22/2025, 2:13:38 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

#Constants
ALL_MOTOR_CARTRIDGE = GearSetting.RATIO_6_1
GEAR_RATIO_MOTOR_TO_WHEEL = 48 / 36

#Define robot parts
brain=Brain()
controller = Controller(PRIMARY)

brain.screen.print("Nourmull Jdrive Tchraine!")

right_group = MotorGroup(
    Motor(Ports.PORT1, ALL_MOTOR_CARTRIDGE, True),
    Motor(Ports.PORT2, ALL_MOTOR_CARTRIDGE, False),
    Motor(Ports.PORT3, ALL_MOTOR_CARTRIDGE, True)
            )

left_group = MotorGroup(
    Motor(Ports.PORT4, ALL_MOTOR_CARTRIDGE, False),
    Motor(Ports.PORT5, ALL_MOTOR_CARTRIDGE, True), 
    Motor(Ports.PORT6, ALL_MOTOR_CARTRIDGE, False)
)

"""spinners = MotorGroup(
    Motor(Ports.PORT10, ALL_MOTOR_CARTRIDGE, True), #fix reverse values later
    Motor(Ports.PORT11, ALL_MOTOR_CARTRIDGE, True),
    )
"""
class DigitalOutToggleable(DigitalOut):
    def __init__(self, port, default_state=False):
        super().__init__(port)

        self.state = default_state

    def toggle(self):
        self.state = not self.state
        self.set(self.state)

in_da_hood = DigitalOutToggleable(brain.three_wire_port.a)



dt = DriveTrain(
    lm = left_group,
    rm = right_group,
    wheelTravel = 101.6 * math.pi,
    trackWidth = 230,
    wheelBase = 340,
    units = MM,
    externalGearRatio = GEAR_RATIO_MOTOR_TO_WHEEL
)

def innit():
    left_group.set_stopping(COAST)
    right_group.set_stopping(COAST)


    #Controls
    bottom = Motor(Ports.PORT7, ALL_MOTOR_CARTRIDGE, False)
    top = Motor(Ports.PORT8, ALL_MOTOR_CARTRIDGE, False)

    controller.buttonL2.pressed(bottom.spin, (REVERSE, 100, PERCENT))
    controller.buttonL2.released(bottom.spin, (REVERSE, 0, PERCENT))
    controller.buttonL1.pressed(top.spin, (REVERSE, 100, PERCENT))
    controller.buttonL1.released(top.spin, (REVERSE, 0, PERCENT))

    controller.buttonR2.pressed(bottom.spin, (FORWARD, 100, PERCENT))
    controller.buttonR2.released(bottom.spin, (FORWARD, 0, PERCENT))
    controller.buttonR1.pressed(top.spin, (FORWARD, 100, PERCENT))
    controller.buttonR1.released(top.spin, (FORWARD, 0, PERCENT))

def scale_degrees(n):
    return (1/(1-0.352))*n

def scale_distance(n):
    return (1/0.352)*n


def alltaune():
    pass

def loup():
    while True:
        speed_stick = controller.axis3.position()
        turn_stick = controller.axis1.position()

        left_velocity = speed_stick+turn_stick
        right_velocity = speed_stick-turn_stick

        left_group.spin(FORWARD, left_velocity, PERCENT)
        right_group.spin(FORWARD, right_velocity, PERCENT)

innit()
competition = Competition(loup, alltaune)
