# remember to hop on field.jerryio to test this - dumb bunny 1
from vex import *
import math

#Constants
DRIVETRAIN_MOTOR_CARTRIDGE = GearSetting.RATIO_18_1
GEAR_RATIO_MOTOR_TO_WHEEL = 48 / 36

#Define robot parts
brain=Brain()
controller = Controller(PRIMARY)

brain.screen.print("Nourmull Jdrive Tchraine!")

left_group = MotorGroup(
    Motor(Ports.PORT1, DRIVETRAIN_MOTOR_CARTRIDGE, False),
    Motor(Ports.PORT2, DRIVETRAIN_MOTOR_CARTRIDGE, True),
    Motor(Ports.PORT3, DRIVETRAIN_MOTOR_CARTRIDGE, False)
            )

right_group = MotorGroup(
    Motor(Ports.PORT4, DRIVETRAIN_MOTOR_CARTRIDGE, True),
    Motor(Ports.PORT5, DRIVETRAIN_MOTOR_CARTRIDGE, False), 
    Motor(Ports.PORT6, DRIVETRAIN_MOTOR_CARTRIDGE, True)
)

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
    submissive = Motor(Ports.PORT7, DRIVETRAIN_MOTOR_CARTRIDGE, False)
    dominant = Motor(Ports.PORT8, DRIVETRAIN_MOTOR_CARTRIDGE, False)

    controller.buttonL2.pressed(submissive.spin, (REVERSE, 100, PERCENT))
    controller.buttonL2.released(submissive.spin, (REVERSE, 0, PERCENT))
    controller.buttonL1.pressed(dominant.spin, (REVERSE, 100, PERCENT))
    controller.buttonL1.released(dominant.spin, (REVERSE, 0, PERCENT))

    controller.buttonR2.pressed(submissive.spin, (FORWARD, 100, PERCENT))
    controller.buttonR2.released(submissive.spin, (FORWARD, 0, PERCENT))
    controller.buttonR1.pressed(dominant.spin, (FORWARD, 100, PERCENT))
    controller.buttonR1.released(dominant.spin, (FORWARD, 0, PERCENT))


def allton():
    pass

def loup():
    while True:
        speed_stick = controller.axis3.position()
        turn_stick = controller.axis1.position()

        left_velocity = speed_stick-turn_stick
        right_velocity = speed_stick+turn_stick

        left_group.spin(FORWARD, left_velocity, PERCENT)
        right_group.spin(FORWARD, right_velocity, PERCENT)

innit()
competition = Competition(loup, allton)
