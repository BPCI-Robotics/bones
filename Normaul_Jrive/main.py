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
        controller.buttonLeft.pressed(self._controller_button_left_pressed)
        controller.buttonUp.pressed(self._controller_button_up_pressed)
        controller.buttonX.pressed(self._controller_button_X_pressed)
        controller.buttonA.pressed(self._controller_button_A_pressed)



        self.add_option("Enter", Color.WHITE, ["", "Are you sure?", "ENTERED"])
    
    def on_enter(self, callback: Callable[[dict[str, Any]], None]):
        self.enter_callback = callback

    def add_option(self, name: str, color: Color | Color.DefinedColor, choices: list[Any]):
        if self.disabled:
            return
        
        self.options.insert(self.count - 1, SelectionMenu._Option(name, color, choices))
        self.count += 1
    
    def _controller_button_left_pressed(self):
        if self.disabled:
            return
        

        self.options[0].next()

        self.draw()
        

        if self.options[self.count - 1].value() == "ENTERED":
            self.enter_callback(self._get_all())
            self.disabled = True
            return
        

    def _controller_button_up_pressed(self):
        if self.disabled:
            return
        

        self.options[1].next()
        
        self.draw()
        

        if self.options[self.count - 1].value() == "ENTERED":
            self.enter_callback(self._get_all())
            self.disabled = True
            return


    def _controller_button_X_pressed(self):
        if self.disabled:
            return
        
        self.options[2].next()

        self.draw()
        
        if self.options[self.count - 1].value() == "ENTERED":
            self.enter_callback(self._get_all())
            self.disabled = True
            return

    def _controller_button_A_pressed(self):
        if self.disabled:
            return
        
        self.options[3].next()

        self.draw()

        if self.options[self.count - 1].value() == "ENTERED":
            self.enter_callback(self._get_all())
            self.disabled = True
            return
        


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

i_hate_MU = Inertial(Ports.PORT15)



right_group = MotorGroup(
    Motor(Ports.PORT4, ALL_MOTOR_CARTRIDGE, False), 
    Motor(Ports.PORT5, ALL_MOTOR_CARTRIDGE, False),
    Motor(Ports.PORT6, ALL_MOTOR_CARTRIDGE, False)
)

left_group = MotorGroup(
    Motor(Ports.PORT1, ALL_MOTOR_CARTRIDGE, True),
    Motor(Ports.PORT2, ALL_MOTOR_CARTRIDGE, True),
    Motor(Ports.PORT3, ALL_MOTOR_CARTRIDGE, True)
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


class DigitalOutToggleable(DigitalOut):
    def __init__(self, port, default_state=False):
        super().__init__(port)

        self.state = default_state

    def toggle(self):
        self.state = not self.state
        self.set(self.state)

brain.screen.print("dont_select.py")

top = Motor(Ports.PORT8, ALL_MOTOR_CARTRIDGE, True)
bottom = Motor(Ports.PORT7, ALL_MOTOR_CARTRIDGE, False) 
#indexer = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

#weirdo = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
middle = DigitalOutToggleable(brain.three_wire_port.c)
little_willy = DigitalOutToggleable(brain.three_wire_port.a)
red_bull = DigitalOutToggleable(brain.three_wire_port.b)
asian_parking = DigitalOutToggleable(brain.three_wire_port.d)
gropper = DigitalOutToggleable(brain.three_wire_port.e)
#spinners = MotorGroup(bottom, top)

#distance sensor
distance1 = Distance(Ports.PORT13)

#tracking wheels
track_x = Rotation(Ports.PORT14)
track_y = Rotation(Ports.PORT16)

#optical
#optical = Optical(Ports.PORT10)

def capture_heading():
    
    return i_hate_MU.heading(DEGREES)


"""def course_correct(direction, prev_heading: float, vel: float):

    error = capture_heading() - prev_heading
    if error > 180:
        error -= 360
    elif error < -180:
        error += 360

    dt.turn_for(direction, abs(error) + 13, DEGREES, vel, PERCENT)"""
    
def turn_to_heading(heading, stopping):

    print("Initial heading: ", capture_heading())
    

    while abs(heading - capture_heading()) > 0.2:

        error = heading - capture_heading()
        
        if error > 180: 
            error -= 360
        elif error < -180:
            error += 360


        if (error > 180):
            break

        if (error < -180):
            break



        if abs(error) <= 0.3:
            dt.stop(stopping)
            break


        vel = 130*(abs(error)/180) 

        if vel <= 1:
            vel = 1

        if vel >= 100:
            vel = 100

        
        if error > 0:
            direction = RIGHT

        elif error < 0:
            direction = LEFT

        dir_print = "L" if direction == LEFT else "R"
       
        dt.turn(direction, vel, PERCENT)

        print("H: ", round(i_hate_MU.heading(), 2), " E: ", round(error, 2), " D: ", dir_print, "V: ", round(vel, 2))
        wait(20, MSEC)


def calc_angle_error(heading):

    angle_error = heading - i_hate_MU.heading()

    if angle_error > 180:
        angle_error -= 360
    
    elif angle_error < -180:
        angle_error += 360

    dir = LEFT if angle_error < 0 else RIGHT

    angle_error = abs(angle_error)


    return [angle_error, dir]

def calc_r(dist, heading):

    r = (dist)/(2*math.sin(math.radians((calc_angle_error(heading)[0])/2)))

    return r


left_pos = left_group.position(DEGREES)
right_pos = right_group.position(DEGREES)

def dist_trav():
    global left_pos, right_pos

    left_trav = left_group.position(DEGREES) - left_pos
    right_trav = right_group.position(DEGREES) - right_pos

    left_trav /= 360
    right_trav /= 360

    left_trav *= dt.__getattribute__("wheelTravel")
    right_trav *= dt.__getattribute__("wheelTravel")

    trav = (left_trav + right_trav) / 2.0
    trav /= 25.4

    return trav

def update_pos():
    global left_pos, right_pos
    left_pos = left_group.position(DEGREES)
    right_pos = right_group.position(DEGREES)
    

def drive_heading(t_dist, t_heading, speed, stop):
    
    left_group.reset_position()
    right_group.reset_position()

    r = calc_r(t_dist, t_heading)

    curve_length = r*math.radians(calc_angle_error(t_heading)[0])

    forward = speed
    turn = forward/r

    while abs(curve_length - dist_trav()) > 0.1 or abs(t_heading - i_hate_MU.heading()) > 0.3:
        dist_error = curve_length - dist_trav()
        angle_error = calc_angle_error(t_heading)[0]

        update_pos()

        forward += dist_error
        turn += 50*(angle_error)/180

        forward *= math.cos(math.radians(angle_error))

        left = forward - turn
        right = forward + turn

        if left > 100:
            left *= 100/left
            right *= 100/left

        elif right > 100:
            left *= 100/right
            right *= 100/right


        left_group.spin(FORWARD, left, PERCENT)
        right_group.spin(FORWARD, right, PERCENT)

        wait(20, MSEC)

        

    



def iterative_correction(heading):

    error = heading - capture_heading()
    print("Heading: ", capture_heading())
    print("Error: ", error)

    """if original_direction == LEFT and error > 0:
        direction = RIGHT

    elif original_direction == LEFT and error < 0:
        direction = LEFT

    elif original_direction == RIGHT and error > 0:
        direction = RIGHT
    
    elif original_direction == RIGHT and error < 0:
        direction = LEFT"""

    
    dt.turn_for(RIGHT, error, DEGREES, 40, PERCENT)
    wait(20, MSEC)







    """while abs(heading - i_hate_MU.heading()) > 0.3:

        wait(20, MSEC)


        current = i_hate_MU.heading(DEGREES)
        print(current)

        error = heading - current

        if error > 180:
            error -= 360

        elif error < -180:
            error += 360

        print("Difference: ", error)

        direction = LEFT if error < 0 else RIGHT

        if direction != original_direction:
            dt.stop(HOLD)

        print("Current direction: ", direction)

        dt.turn_for(direction, error, DEGREES, (error/180 * 100), PERCENT)
        print("Heading: ", i_hate_MU.heading())"""









    """current = capture_heading()
        print(current)

        error = heading - current

        if error > 180: 
            error -= 360
        elif error < -180:
            error += 360
        print(error)

        direction = LEFT if error < 0 else RIGHT

        if direction != original_direction:
            dt.stop(HOLD)
        
        print(direction)

        dt.turn(direction, 50, PERCENT)
        print("Heading: ", heading)"""

def localize_x(direction):
    global pose
    x = distance1.object_distance()

    if direction == RIGHT:
        x_coord = x - 72

    if direction == LEFT:
        x_coord = 72 - x

    pose[0] = x_coord

    


def localize_y():
    global pose
    y = distance1.object_distance()

    y_coord = 72 - y

    pose[1] = y_coord

pose = [0, 0, 0] #x, y, theta
#theta is determined by IMU
#x and y are determined by tracking wheel
    


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

        if self.direction == LEFT:

            red_bull.set(False)
            little_willy.set(False)
            middle.set(False)

            top.set_stopping(HOLD)
            top.spin(FORWARD, 0, PERCENT)
            bottom.spin(FORWARD, 100, PERCENT)


            dt.drive_for(FORWARD, 2, INCHES, 66, PERCENT, True)
            dt.turn_for(LEFT, 1.1*20, DEGREES, 80, PERCENT, True)
            turn_to_heading(340, HOLD)
            print("Heading after auton turn 1: ", capture_heading())
            wait(0.1, SECONDS)
            dt.drive_for(FORWARD, 46, INCHES, 50, PERCENT, True)
            wait(0.1, SECONDS)
            dt.drive_for(REVERSE, 3, INCHES, 45, PERCENT, True)
            wait(0.1, SECONDS)
            dt.turn_for(LEFT, 1.1*122, DEGREES, 90, PERCENT, True)
            turn_to_heading(218, HOLD)
            print("Heading after auton turn 2: ", capture_heading())
            little_willy.set(True)


            dt.drive_for(REVERSE, 26, INCHES, 80, PERCENT)
            dt.drive_for(REVERSE, 3, INCHES, 35, PERCENT, wait=False)
            wait(0.4, SECONDS)
            middle.set(True)
            top.spin(FORWARD, 100, PERCENT)
            wait(1.7, SECONDS)
            top.spin(FORWARD, 0, PERCENT)
            middle.set(False)

            dt.drive_for(FORWARD, 3, INCHES, 30, PERCENT)
            turn_to_heading(230, HOLD)

            little_willy.set(True)
            dt.drive_for(FORWARD, 80, INCHES, 85, PERCENT)
            dt.turn_for(LEFT, 1.10*50, DEGREES, 86, PERCENT, True)
            turn_to_heading(180, HOLD)

            dt.drive_for(FORWARD, 27, INCHES, 55, PERCENT)
            dt.stop(HOLD)
            wait(0.5, SECONDS)

            turn_to_heading(180, HOLD)

            dt.drive_for(REVERSE, 48, INCHES, 60, PERCENT)
            top.spin(FORWARD, 100, PERCENT)
            wait(1.5, SECONDS)

            dt.drive_for(FORWARD, 8, INCHES, 90, PERCENT)
            dt.drive_for(REVERSE, 8, INCHES, 90, PERCENT)
            


        
        elif self.direction == RIGHT:
            red_bull.set(False)
            little_willy.set(False)
            middle.set(False)

            top.set_stopping(HOLD)
            top.spin(FORWARD, 0, PERCENT)
            bottom.spin(FORWARD, 100, PERCENT)


            dt.drive_for(FORWARD, 2, INCHES, 66, PERCENT, True)
            dt.turn_for(RIGHT, 1.10*20, DEGREES, 90, PERCENT, True)
            turn_to_heading(20, HOLD)
            wait(0.1, SECONDS)
            dt.drive_for(FORWARD, 42, INCHES, 40, PERCENT, True)
            wait(0.1, SECONDS)
            dt.turn_for(RIGHT, 137, DEGREES, 90, PERCENT)
            little_willy.set(True)
            turn_to_heading(140, HOLD)
            dt.drive_for(FORWARD, 56, INCHES, 66, PERCENT)
            dt.turn_for(RIGHT, 1.10*75, DEGREES, 66, PERCENT)
            dt.drive_for(FORWARD, 32, INCHES, 40, PERCENT)
            wait(0.5, SECONDS)
            #dt.drive_for(FORWARD, 3.3, INCHES, 40, PERCENT)
            #wait(0.4, SECONDS)
            #dt.drive_for(REVERSE, 3.3, INCHES, 40, PERCENT)
            dt.turn_for(RIGHT, 1.10*2, DEGREES, 70, PERCENT)
            dt.drive_for(REVERSE, 47, INCHES, 60, PERCENT)
            top.spin(FORWARD, 100, PERCENT)
            #wait(4, SECONDS)
            #top.spin(FORWARD, 0, PERCENT)
            #dt.drive_for(FORWARD, 5, INCHES, 50, PERCENT)
            #dt.drive_for(REVERSE, 5, INCHES, 90, PERCENT)

            


        
            

        
            


        
    
        #written by dumb bunny 2
        #0.9367*909


    def _elims(self):
        
        if self.direction == LEFT:
            print("")

        
        elif self.direction == RIGHT: 
            print("")
        


    def _skills(self):
        dt.drive_for(FORWARD, 2, INCHES, 100, PERCENT)
        dt.drive_for(REVERSE, 58, INCHES, 100, PERCENT)
        gropper.set(True)
        asian_parking.set(True)
        """little_willy.set(False)
        in_da_hood.set(False)
        pto.set(True)

        #bottom_spinner.constantly_unstuck()
        bottom.spin(FORWARD, 100, PERCENT)
        dt.drive_for(REVERSE, 1.84*4, INCHES, 100, PERCENT, True)
        dt.drive_for(FORWARD, 1.84*6.7, INCHES,100, PERCENT, True)
        wait (0.1, SECONDS)        
        dt.drive_for(FORWARD, 1.84*4, INCHES, 80, PERCENT)
        dt.drive_for(FORWARD, 1.84*20, INCHES, 50, PERCENT, True)

        dt.drive_for(FORWARD, 1.84*31.85, INCHES, 30, PERCENT)
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
        
        # in_da_hood.set(True)
        # pto.set(False)
        wait(12, SECONDS)

        # pto.set(True)
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




    def _solo_awp(self):
        i_hate_MU.set_heading(270)
        red_bull.set(False)
        little_willy.set(False)
        middle.set(False)
        top.set_stopping(HOLD)
        top.spin(FORWARD, 0, PERCENT)
        bottom.spin(FORWARD, 100, PERCENT)

        dt.drive_for(FORWARD, 7, INCHES, 66, PERCENT)
        wait(0.1, SECONDS)
        dt.drive_for(REVERSE, 2, INCHES, 50, PERCENT)
        dt.drive_for(REVERSE, 63, INCHES, 75, PERCENT)
        dt.stop(HOLD)
        wait(0.1, SECONDS)
        dt.turn_for(LEFT, 1.1*90, DEGREES, 90, PERCENT)
        little_willy.set(True)
        turn_to_heading(180, HOLD)
        dt.drive_for(FORWARD, 9, INCHES, 70, PERCENT)
        wait(0.3, SECONDS)
        turn_to_heading(180, HOLD)
        dt.drive_for(REVERSE, 48, INCHES, 60, PERCENT)
        top.spin(FORWARD, 100, PERCENT)
        wait(2.5, SECONDS)
        top.stop()

        little_willy.set(True)
        dt.turn_for(RIGHT, 1.10*135, DEGREES, 80, PERCENT, wait=False)
        turn_to_heading(315, HOLD)
        dt.drive_for(FORWARD, 24, INCHES, 75, PERCENT)
        dt.turn_for(LEFT, 1.10*45, DEGREES, 75, PERCENT)
        turn_to_heading(217, HOLD)




        


        
        



    
    def _test(self):

        print("Heading at the beginning: ", i_hate_MU.heading())
        turn_to_heading(340, HOLD)
        print("Heading after first turn: ", i_hate_MU.heading())
        wait(2, SECONDS)

        turn_to_heading(0, HOLD)
        print("Heading after second turn: ", i_hate_MU.heading())
        wait(2, SECONDS)

        turn_to_heading(235, HOLD)
        print("Heading after third turn: ", i_hate_MU.heading())
        wait(2, SECONDS)

        turn_to_heading(0, HOLD)
        print("Final heading: ", i_hate_MU.heading())
        wait(2, SECONDS)


        

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

        elif config['Auton type'] == "Solo AWP":
            self._routine_selected = self._solo_awp

        elif config["Auton type"] == "Test":
            self._routine_selected = self._test


    def __call__(self):
        self._routine_selected()


#def toggle_indexer_direction():
    #indexer.set_reversed(indexer.direction == DirectionType.FORWARD)

"""def colour_detection():
    while True:
        wait(120, MSEC)
        # Only check when intake is actually running
        if bottom.velocity(PERCENT) > 5:
            if optical.is_near_object() and (optical.hue() >= 350 and optical.hue() <= 25):
                print("Object detected!")
                # Fire the reject shot without blocking the thread
                top.spin_for(REVERSE, 1, SECONDS, 100, PERCENT)
                wait(200, MSEC)  # debounce so it doesn't fire repeatedly"""
            


def innit():

    for i in range(1,3):     
        line = 2
        i_hate_MU.calibrate()
        while i_hate_MU.is_calibrating():
            brain.screen.set_cursor(line, 1)
            brain.screen.print(i_hate_MU.heading())
            line += 1
            if line > 12:
                brain.screen.clear_screen()
                line = 1
            wait(20, MSEC)

    
    wait(1, SECONDS)
    val_1 = i_hate_MU.heading()

    wait(500, MSEC)
    val_2 = i_hate_MU.heading()


    while abs(val_2 - val_1) >= 0.05:
        brain.screen.next_row()
        brain.screen.print("Calibration did not happen properly!")
        i_hate_MU.calibrate()
        while i_hate_MU.is_calibrating:
            wait(20, MSEC)




    menu = SelectionMenu()
    menu.add_option("Colour", Color.RED, ["Red", "Blue"])
    menu.add_option("Auton direction", Color.BLUE, ["Left", "Right"])
    menu.add_option("Auton type", Color.PURPLE, ["Quals", "Elims", "Skills", "Solo AWP", "Test"])

    menu.on_enter(hawk_tuah.set_config)

    #in_da_hood.set(True)

    menu.draw()
    print("\033[2J")

    dt.set_stopping(COAST)

    #control for basic intake
    controller.buttonL1.pressed(bottom.spin, (FORWARD, 100, PERCENT))
    controller.buttonL1.released(bottom.spin, (FORWARD, 0, PERCENT))

    #control for bottom scoring
    controller.buttonL2.pressed(bottom.spin, (REVERSE, 100, PERCENT))
    controller.buttonL2.released(bottom.spin, (REVERSE, 0, PERCENT))

    #control for top scoring
    controller.buttonR1.pressed(top.spin, (FORWARD, 70, PERCENT))
    controller.buttonR1.pressed(bottom.spin, (FORWARD, 80, PERCENT))
    controller.buttonR1.released(top.spin, (FORWARD, 0, PERCENT))
    controller.buttonR1.released(bottom.spin, (FORWARD, 0, PERCENT))

    #control for middle scoring
    controller.buttonR2.pressed(bottom.spin, (FORWARD, 70, PERCENT))
    controller.buttonR2.pressed(top.spin, (FORWARD, 50, PERCENT))
    controller.buttonR2.pressed(middle.set, (True,))

    controller.buttonR2.released(bottom.spin, (FORWARD, 0, PERCENT)) 
    controller.buttonR2.released(top.spin, (FORWARD, 0, PERCENT))
    controller.buttonR2.released(middle.set, (False,))

    #pistons
    controller.buttonRight.pressed(red_bull.toggle)
    controller.buttonY.pressed(little_willy.toggle)
    controller.buttonDown.pressed(asian_parking.toggle)
    controller.buttonB.pressed(gropper.toggle)

    #optical
    #optical.set_light(LedStateType.ON)
    #optical.set_light_power(100, PERCENT)


def drunk_driver():
    #Thread(colour_detection)

    left_group.set_stopping(COAST)
    right_group.set_stopping(COAST)
    top.set_stopping(HOLD)

    while True:
        speed_stick = controller.axis3.position()
        turn_stick = controller.axis1.position()

        left_velocity = speed_stick + turn_stick
        right_velocity = speed_stick - turn_stick

        left_group.spin(FORWARD, left_velocity, PERCENT)
        right_group.spin(FORWARD, right_velocity, PERCENT)

        wait(10, MSEC)


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
