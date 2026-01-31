from vex import *
import math

class SelectionMenu:
    class _Option:
        def __init__(self, name: str, color: Color | Color.DefinedColor, choices: list[Any]):
            self.name = name
            self.color = color
            self.choices = choices
            self.index = 0
            self.count = len(choices)

        def value(self) -> Any:
            return self.choices[self.index]
        
        def next(self) -> None:
            self.index = (self.index + 1) % self.count
        
        def prev(self) -> None:
            if self.index == 0:
                self.index = self.count - 1
            else:
                self.index -= 1
    
    def __init__(self):
        self.count = 0
        self.options: list[SelectionMenu._Option] = []

        self.disabled = False
        self.enter_callback: Callable[[dict[str, Any]], None]

        brain.screen.pressed(self._on_brain_screen_press)

        self.add_option("Enter", Color.WHITE, ["", "Are you sure?", "ENTERED"])
    
    def on_enter(self, callback: Callable[[dict[str, Any]], None]):
        self.enter_callback = callback

    def add_option(self, name: str, color: Color | Color.DefinedColor, choices: list[Any]):
        if self.disabled:
            return
        
        self.options.insert(self.count - 1, SelectionMenu._Option(name, color, choices))
        self.count += 1
    
    def _on_brain_screen_press(self):
        if self.disabled:
            return
        
        x = brain.screen.x_position()
        y = brain.screen.y_position()

        if y < 240 - 100:
            return
        
        self.options[x * self.count // 480].next()

        self.draw()

        if self.options[self.count - 1].value() == "ENTERED":
            self.enter_callback(self._get_all())
            self.disabled = True
            return
    
    def force_submit(self):
            self.enter_callback(self._get_all())
            self.disabled = True
            return
    
    def _get_all(self) -> dict[str, Any]:
        if self.disabled:
            return {}
        
        d = {}
        for option in self.options:
            d[option.name] = option.value()
        
        return d

    def draw(self):
        if self.disabled:
            return
        
        brain.screen.clear_screen(Color.BLACK)

        # Print the configurations
        brain.screen.set_font(FontType.MONO20)

        i = 0
        for option in self.options:
            brain.screen.set_pen_color(option.color)
            brain.screen.set_cursor(i + 1, 1)
            brain.screen.print(option.name + ": " + str(option.value()))

            i += 1

        canvas_width = 480
        canvas_height = 240

        rect_width = (canvas_width - 10 * (self.count + 1)) / self.count
        rect_height = 70

        i = 0
        for option in self.options:
            brain.screen.set_pen_color(option.color)
            brain.screen.draw_rectangle(
                10 + (10 + rect_width) * i, 
                canvas_height - (rect_height + 5),
                rect_width,
                rect_height,
                option.color
            )
            i += 1

#Define robot parts
brain=Brain()
controller = Controller(PRIMARY)

#Constants
ALL_MOTOR_CARTRIDGE = GearSetting.RATIO_6_1
GEAR_RATIO_MOTOR_TO_WHEEL = 48/36

DRIVETRAIN_SCALE_FACTOR = 1.84 #for auton

#i_hate_MU = Inertial(Ports.PORT9)

right_group = MotorGroup(
    Motor(Ports.PORT4, ALL_MOTOR_CARTRIDGE, True), 
    Motor(Ports.PORT5, ALL_MOTOR_CARTRIDGE, False),
    Motor(Ports.PORT6, ALL_MOTOR_CARTRIDGE, True)
)

left_group = MotorGroup(
    Motor(Ports.PORT1, ALL_MOTOR_CARTRIDGE, False),
    Motor(Ports.PORT2, ALL_MOTOR_CARTRIDGE, True), 
    Motor(Ports.PORT3, ALL_MOTOR_CARTRIDGE, False)
)


dt = DriveTrain( #SmartDrive
    lm = left_group,
    rm = right_group,
    #g = i_hate_MU,
    wheelTravel = 82.55 * math.pi,
    trackWidth = 311,
    wheelBase = 254,
    units = MM,
    externalGearRatio = GEAR_RATIO_MOTOR_TO_WHEEL,
)


"""class spinner:
    def __init__(self, motor: Motor):

        self.motor = motor

        self.motor.set_stopping(BrakeType.HOLD)


    def reverse_direction(self):
        if self.motor.direction() == DirectionType.FORWARD:
            self.motor.spin_for(REVERSE, 1080, DEGREES, 100, PERCENT)

        elif self.motor.direction() == DirectionType.REVERSE:
            self.motor.spin_for(FORWARD, 1080, DEGREES, 100, PERCENT)

    def oscillate_unstuck(self):
        while self.motor.is_spinning():
            if self.motor.velocity(RPM) == 0:
                self.motor.spin(self.motor.direction(), 80, PERCENT)
                wait(200, MSEC)
                self.reverse_direction()

            wait(20, MSEC)

        pass


    def constantly_unstuck(self):
        self._constant_thread = Thread(self.oscillate_unstuck)"""



"""class agitator:
    def __init__(self, motor: Motor):
        self.motor = motor

        self.motor.set_stopping(BrakeType.HOLD)
    
    def oscillate_unstuck(self):
        while self.motor.is_spinning():
            wait(20, MSEC)
            if self.motor.velocity(RPM) == 0:
                self.motor.spin(FORWARD, 80, PERCENT)
                wait(0.5, SECONDS)
                self.motor.spin(REVERSE, 80, PERCENT)

            else:
                continue

    def constantly_unstuck(self):
        Thread(self.oscillate_unstuck)

"""



"""class smooth_auton_dt(DriveTrain):
    def __init__(self, lm: MotorGroup, rm: MotorGroup, wheelTravel, trackWidth, wheelBase, units, externalGearRatio):
        super().__init__(lm, rm, wheelTravel, trackWidth, wheelBase, units, externalGearRatio)
        self.min_v = 20"""




class DigitalOutToggleable(DigitalOut):
    def __init__(self, port, default_state=False):
        super().__init__(port)

        self.state = default_state

    def toggle(self):
        self.state = not self.state
        self.set(self.state)


#Define robot parts
brain=Brain()
controller = Controller(PRIMARY)

brain.screen.print("dont_select.py")

bottom = Motor(Ports.PORT8, ALL_MOTOR_CARTRIDGE, False)
top = Motor(Ports.PORT7, ALL_MOTOR_CARTRIDGE, False) 
#indexer = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

#weirdo = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
in_da_hood = DigitalOutToggleable(brain.three_wire_port.a)
pto = DigitalOutToggleable(brain.three_wire_port.b)
little_willy = DigitalOutToggleable(brain.three_wire_port.c)
red_bull = DigitalOutToggleable(brain.three_wire_port.d)
spinners = MotorGroup(bottom, top)

#bottom_spinner = spinner(bottom)

class hawk_tuon:
    def __init__(self):
        self.direction = LEFT
        self._routine_selected = self._noop

        #for the commented ones, uncomment once we've gooned the drivetrain with the IMU to form a SmartDrive
        #dt.set_heading()
        #dt.set_rotation(0, DEGREES)

        #dt.g.calibrate()
        #while dt.g.is_calibrating():
            #wait(20, MSEC)

        #dt.set_heading(0, DEGREES)

        #dt.set_turn_velocity(100, PERCENT)
        #dt.set_drive_velocity(100, PERCENT)


    def _noop(self):
        pass

    """def turn_head(self, target, vel):

        while abs(dt.g.heading() - target) >= 2:
            dt.turn(RIGHT, vel, PERCENT)
            brain.screen.clear_line(3)
            brain.screen.set_cursor(3,1)
            brain.screen.print(dt.g.heading(), "    ", (dt.g.heading() - target))
            wait(20, MSEC)

            if abs(dt.g.heading() - target) < 2:
                dt.stop()

        wait(2, SECONDS)
    
    def my_function(self):
        brain.screen.clear_line(2)
        brain.screen.set_cursor(2,1)
        brain.screen.print("I CHANGED!")"""



    def _quals(self):
        """dt.g.reset_heading()
        dt.g.calibrate()
        while (dt.g.is_calibrating()):
            wait(20, MSEC)

        
        self.turn_head(90,20)
        dt.g.changed(self.my_function)

        while True:
            brain.screen.set_cursor(1, 1)
            brain.screen.clear_line(1)
            brain.screen.print("Dumb bunny: " + str(dt.g.heading()) + str(i_hate_MU.orientation(OrientationType.YAW, DEGREES)))
            wait(100, MSEC)"""

        #remember, hood is closed to start off, so make sure to toggle it back 
        #same thing with lil will 
        #on the other hand, door starts out open, so make sure to close it

        #bottom.spin(REVERSE, 100, PERCENT)
        #top.spin(REVERSE, 100, PERCENT)

        if self.direction == LEFT:
            in_da_hood.set(False)
            red_bull.set(False)
            little_willy.set(False)
            pto.set(True)


            #NOTED TO SELF
            #gate is closed, value = False
            #hood is up, value = False

            bottom.spin(REVERSE, 100, PERCENT)
            top.spin(REVERSE, 100, PERCENT)

            
            dt.drive_for(FORWARD, 1.84*3, INCHES, 30, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*5.5, INCHES, 55, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*3.5, INCHES, 20, PERCENT, True)
            wait(0.25, SECONDS)
            dt.turn_for(LEFT, 1.10*22, DEGREES, 15, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*5, INCHES, 10, PERCENT, True)
            dt.turn_for(LEFT, 1.10*10, DEGREES, 15, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*7, INCHES, 10, PERCENT, True)
            dt.turn_for(LEFT, 1.10*3, DEGREES, 15, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*3, INCHES, 10, PERCENT)
            dt.turn_for(RIGHT, 1.10*3, DEGREES, 30, PERCENT)
            wait(1, SECONDS)
            dt.turn_for(RIGHT, 73, DEGREES, 70, PERCENT)

            dt.drive_for(FORWARD, 1.84*3.5, INCHES, 30, PERCENT)
            dt.drive_for(FORWARD, 1.84*5.5, INCHES, 65, PERCENT)
            dt.drive_for(FORWARD, 1.84*3.8, INCHES, 40, PERCENT)
            
            top.spin(FORWARD, 50, PERCENT)
            bottom.spin(REVERSE, 100, PERCENT)

            in_da_hood.toggle()
            pto.toggle()
            

        
        elif self.direction == RIGHT:
            in_da_hood.set(False)
            red_bull.set(False)
            little_willy.set(False)
            pto.set(True)


            #NOTED TO SELF
            #gate is closed, value = False
            #hood is up, value = False

            bottom.spin(REVERSE, 100, PERCENT)
            top.spin(REVERSE, 100, PERCENT)

            
            dt.drive_for(FORWARD, 1.84*3, INCHES, 30, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*5.5, INCHES, 75, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*3.5, INCHES, 20, PERCENT, True)
            wait(0.25, SECONDS)
            dt.turn_for(RIGHT, 1.10*22, DEGREES, 20, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*5, INCHES, 10, PERCENT, True)
            dt.turn_for(RIGHT, 1.10*15, DEGREES, 15, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*7, INCHES, 10, PERCENT, True)
            dt.turn_for(RIGHT, 1.10*16, DEGREES, 15, PERCENT, True)
            dt.drive_for(FORWARD, 1.84*3, INCHES, 10, PERCENT)
            dt.turn_for(LEFT, 1.10*8, DEGREES, 30, PERCENT)
            wait(1, SECONDS)
            dt.turn_for(LEFT, 93.5, DEGREES, 70, PERCENT)

            dt.drive_for(FORWARD, 1.84*3.5, INCHES, 30, PERCENT)
            dt.drive_for(FORWARD, 1.84*5.5, INCHES, 65, PERCENT)
            dt.drive_for(FORWARD, 1.84*4.5, INCHES, 40, PERCENT)

            top.spin(FORWARD, 0, PERCENT)
            bottom.spin(FORWARD, 80, PERCENT)

            in_da_hood.toggle()
            pto.set(False)
            

        
            


        
    
        #written by dumb bunny 2
        #0.9367*909"""


    def _elims(self):
        pass

    def _skills(self):
        little_willy.set(False)
        in_da_hood.set(False)
        pto.set(True)

        #bottom_spinner.constantly_unstuck()
        bottom.spin(FORWARD, 100, PERCENT)
        dt.drive_for(REVERSE, 1.84*4, INCHES, 100, PERCENT, True)
        dt.drive_for(FORWARD, 1.84*6.7, INCHES,100, PERCENT, True)
        wait (0.2, SECONDS)        
        dt.drive_for(FORWARD, 1.84*24, INCHES,100, PERCENT, True)

        """dt.drive_for(FORWARD, 1.84*31.85, INCHES, 30, PERCENT)
        wait(0.5, SECONDS)
        dt.turn_for(RIGHT, 89, DEGREES, 35, PERCENT, wait=True)

        bottom.spin(REVERSE, 100, PERCENT)
        top.spin(REVERSE, 100, PERCENT)

        dt.drive_for(FORWARD, 1.84*7.5, INCHES, 25, PERCENT)

        i = 0
        for i in range(0,7):
            dt.drive_for(FORWARD, 1.84*1.55, INCHES, 24, PERCENT)
            wait(0.1, SECONDS)
            dt.drive_for(REVERSE, 1.84*1.55, INCHES, 24, PERCENT)
            wait(0.7, SECONDS)

            i += 1

    
        wait(0.2, SECONDS)

        dt.drive_for(REVERSE, 1.84*8, INCHES, 30, PERCENT)
        little_willy.set(False)
        wait(0.5, SECONDS)
        dt.turn_for(RIGHT, 1.10*175, DEGREES, 30, PERCENT)
        wait(0.5, SECONDS)

        dt.drive_for(FORWARD, 1.84*11.7, INCHES, 30, PERCENT)
        #dt.drive_for(REVERSE, 1.84*3, INCHES, 65, PERCENT)
        #dt.drive_for(FORWARD, 1.84*3.35, INCHES, 30, PERCENT)
        
        in_da_hood.set(True)
        pto.set(False)
        wait(12, SECONDS)

        pto.set(True)
        dt.drive_for(REVERSE, 1.84*10, INCHES, 40, PERCENT)
        in_da_hood.toggle()
        dt.drive_for(REVERSE, 1.84*2, INCHES, 40, PERCENT)
        wait(0.2, SECONDS)
        dt.turn_for(RIGHT, 1.10*85, DEGREES, 40, PERCENT)
        dt.drive_for(REVERSE, 1.84*10, INCHES, 40, PERCENT)
        dt.turn_for(LEFT, 1.10*25, DEGREES, 30, PERCENT)
        dt.drive_for(REVERSE, 1.84*3, INCHES, 30, PERCENT)
        dt.turn_for(RIGHT, 1.10*28, DEGREES, 40, PERCENT)
        dt.drive_for(REVERSE, 1.84*26, INCHES, 55, PERCENT"""




    def _nothing(self):
        dt.drive_for(FORWARD, 1.84*3, INCHES, 20, PERCENT)

    
    def _test(self):
        pto.set(False)
        wait(3, SECONDS)
        pto.toggle()
        





    def set_config(self, config: dict[str, Any]):
        print(config)

        if config["Colour"] == "Red":
            self.color = Color.RED
        else:
            self.color = Color.BLUE
        
        if config["Auton direction"] == "Left":
            self.direction = LEFT
        else:
            self.direction = RIGHT
        
        if config["Auton type"] == "Skills":
            self._routine_selected = self._skills

        elif config['Auton type'] == "Quals":
            self._routine_selected = self._quals

        elif config['Auton type'] == "Elims":
            self._routine_selected = self._elims

        elif config['Auton type'] == "Nothing":
            self._routine_selected = self._nothing

        elif config["Auton type"] == "Test":
            self._routine_selected = self._test


    def __call__(self):
        self._routine_selected()


#def toggle_indexer_direction():
    #indexer.set_reversed(indexer.direction == DirectionType.FORWARD)

def innit():
    menu = SelectionMenu()
    menu.add_option("Colour", Color.RED, ["Red", "Blue"])
    menu.add_option("Auton direction", Color.BLUE, ["Left", "Right"])
    menu.add_option("Auton type", Color.PURPLE, ["Quals", "Elims", "Skills", "Nothing", "Test"])

    menu.on_enter(hawk_tuah.set_config)

    in_da_hood.set(True)

    menu.draw()
    print("\033[2J")

    dt.set_stopping(COAST)


def hood_pto_link():
    pto.set(not in_da_hood.state)

def drunk_driver():
    left_group.set_stopping(COAST)
    right_group.set_stopping(COAST)

    #control for the 5.5w indexer
    #controller.buttonR2.pressed(indexer.spin, (FORWARD, 100, PERCENT))
    #controller.buttonR2.released(indexer.spin, (FORWARD, 0, PERCENT))

    #control for top scoring
    controller.buttonL1.pressed(spinners.spin, (REVERSE, 100, PERCENT))
    controller.buttonL1.released(spinners.spin, (REVERSE, 0, PERCENT))

    #control for bottom scoring
    controller.buttonL2.pressed(bottom.spin, (FORWARD, 100, PERCENT))
    controller.buttonL2.released(bottom.spin, (FORWARD, 0, PERCENT))

    #control for intake and middle scoring
    controller.buttonR1.pressed(top.spin, (FORWARD, 100, PERCENT))
    controller.buttonR1.released(top.spin, (FORWARD, 0, PERCENT))
    controller.buttonR1.pressed(bottom.spin, (REVERSE, 100, PERCENT))
    controller.buttonR1.released(bottom.spin, (REVERSE, 0, PERCENT))

    #pistons
    controller.buttonRight.pressed(pto.toggle)
    controller.buttonY.pressed(in_da_hood.toggle)
    controller.buttonY.pressed(hood_pto_link)
    controller.buttonB.pressed(little_willy.toggle)
    controller.buttonDown.pressed(red_bull.toggle)

    while True:
        speed_stick = controller.axis3.position()
        turn_stick = controller.axis1.position()

        left_velocity = speed_stick + turn_stick
        right_velocity = speed_stick - turn_stick
        left_group.spin(FORWARD, left_velocity, PERCENT)
        right_group.spin(FORWARD, right_velocity, PERCENT)

        #print(weirdo.motor.torque(), top.torque())
        #the previous line was just used for testing


"""def scale_degrees(n):
    print((0.9367)*n)
    brain.screen.print((0.9367)*n)
    return (0.9367)*n

def scale_degrees_over_90(n):
    return(1/(1-0.352))*n

def scale_distance(n):
    return (2.167)*n"""
    

hawk_tuah = hawk_tuon()

competition = Competition(drunk_driver, hawk_tuah)
innit()
