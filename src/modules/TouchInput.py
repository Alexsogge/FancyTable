import mtdev
import sys
from enum import Enum
from queue import Queue
import time

class ActionType(Enum):
     PRESSED = 1
     RELEASED = 2
     MOVED = 3


class Action:

    def __init__(self, x, y, atype):
        self.x = x
        self.y = y
        self.type = atype

    def __str__(self):
        return "Action " + str(self.type) + " on " + str(self.x) + " | "+ str(self.y)


class Display:
    width = 0
    height = 0

    input_width = 0
    input_height = 0

    calibration_dots = []

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_input_range(self, width, height):
        self.input_width = width
        self.input_height = height

    def add_calibration_dot(self, x, y):
        print("Add calibrationpoint ", x ,y)
        self.calibration_dots.append((x, y))

    def perform_calibration(self):
        if len(self.calibration_dots) != 4:
            return False

        self.input_width = (self.calibration_dots[1][0] - self.calibration_dots[0][0] +
                            self.calibration_dots[3][0] - self.calibration_dots[2][0]) / 2
        self.input_height = (self.calibration_dots[2][1] - self.calibration_dots[0][1] +
                            self.calibration_dots[3][1] - self.calibration_dots[1][1]) / 2

        print("Calibrated:", self.input_width, self.input_height, "\n\r")

    def load_calibration(self, width, height):
        self.input_width = width
        self.input_height = height

    def get_pixel_from_input(self, x, y):
        #print(self.width, self.input_width)
        px = (self.width / self.input_width ) * x
        py = (self.height / self.input_height) * y
        #print("Map from ", x, y, " to ", px, py)
        if px < 0:
            px = 0
        if px > self.width:
            px = self.width-1
        if py < 0:
            py = 0
        if py > self.height:
            py = self.height-1

        return int(px), int(py)


class TInput:

    mt_class = 0
    x = 0
    y = 0

    states = None

    def __init__(self, mt_class):
        self.mt_class = mt_class
        self.states = Queue()

    def move(self, axis, value):
        if axis == 'x':
            self.x = value
        if axis == 'y':
            self.y = value
        self.states.put(Action(self.x, self.y, ActionType.MOVED))
        # print(str(self.mt_class) + " moved to x: " + str(self.x) + "  y: " + str(self.y))

    def press(self):
        self.states.put(Action(self.x, self.y, ActionType.PRESSED))
        # print(str(self.mt_class) + " pressed on x: " + str(self.x) + "  y: " + str(self.y))

    def release(self):
        self.states.put(Action(self.x, self.y, ActionType.RELEASED))
        # print(str(self.mt_class) + " released on x: " + str(self.x) + "  y: " + str(self.y))

    def do_sth_on_click(self, do_func, single_use=False):
        executed = False
        for action in list(self.states.queue):
            if action.type == ActionType.PRESSED:
                do_func(action.x, action.y)
                executed = True
                if single_use:
                    return True
        return executed

    def clear(self):
        self.states.queue.clear()

    def get_states(self):
        return self.states

    def __str__(self):
        out = "Tinput slot " + str(self.mt_class) + " with " + str(list(self.states.queue))
        return out


class TouchInputManager:
    display = None
    device = None
    slot = 0

    inputs = {0: TInput(0)}

    def __init__(self, device_path):
        print(mtdev)
        self.device = mtdev.Device(device_path)

    def read_inputs(self, idle=50):
        if self.device.idle(idle):
            return
        while True:
            data = self.device.get()
            if data is None:
                break
            if data.type == 0:
                continue

            # change the slot number
            if data.type == mtdev.MTDEV_TYPE_EV_ABS and data.code == mtdev.MTDEV_CODE_SLOT:
                self.slot = data.value
                if self.slot not in self.inputs:
                    self.inputs[self.slot] = TInput(self.slot)

            if data.type == mtdev.MTDEV_TYPE_EV_ABS and data.code == mtdev.MTDEV_CODE_TRACKING_ID:
                if data.value == -1:
                    self.inputs[self.slot].release()
                else:
                    self.inputs[self.slot].press()

            if data.type == mtdev.MTDEV_TYPE_EV_ABS and data.code == mtdev.MTDEV_CODE_POSITION_X:
                self.inputs[self.slot].move('x', data.value)
                #print("X to ", data.value)

            if data.type == mtdev.MTDEV_TYPE_EV_ABS and data.code == mtdev.MTDEV_CODE_POSITION_Y:
                self.inputs[self.slot].move('y', data.value)


    def get_inputs(self):
        """
        >>> tmgr = TouchInputManager("/dev/input/event1")
        >>> i1 = TInput(0)
        >>> i1.press()
        >>> i1.move('x', 0)
        >>> i1.move('y', 1)
        >>> i1.move('x', 2)
        >>> i1.move('y', 3)

        >>> i2 = TInput(1)
        >>> i2.press()
        >>> i2.move('x', 4)
        >>> i2.move('y', 5)
        >>> tmgr.inputs = {0: i1, 1: i2}
        >>> inp = tmgr.get_inputs()
        >>> print([str(a) for a in list(inp[1].states.queue)])
        >>> inp[0].states == inp[1].states
        """
        return self.inputs

    def define_display(self, width, height):
        self.display = Display(width, height)

    def clear_inputs(self):
        self.inputs = {0: TInput(0)}

    def load_calibration(self, width, height):
        self.display.load_calibration(width, height)

    def calibrate(self, framebuffer):
        if self.display is None:
            return False

        def set_input_corner(x, y):
            self.display.add_calibration_dot(x, y)

        def read_corner(corner_x, corner_y):
            framebuffer.clear_frame()

            framebuffer.set_pixel(corner_x, corner_y, 254, 254, 254)
            framebuffer.upload_frame()
            self.read_inputs(200)
            self.clear_inputs()
            released = False
            pressed = False
            mean_x = 0
            mean_y = 0
            while not released:
                self.read_inputs(200)
                i_states = self.inputs[0].states
                while True:
                    if i_states.empty():
                        break
                    i_state = i_states.get()
                    if i_state.type == ActionType.PRESSED:
                        pressed = True
                    if i_state.type == ActionType.MOVED and pressed:
                        mean_x = (i_state.x + mean_x) / 2
                        mean_y = (i_state.y + mean_y) / 2
                    if i_state.type == ActionType.RELEASED and pressed:
                        self.display.add_calibration_dot(mean_x, mean_y)
                        released = True
            self.read_inputs()
            self.clear_inputs()
            framebuffer.clear_frame()
            framebuffer.upload_frame()
            time.sleep(3)


        buffer_w, buffer_h = framebuffer.get_dimensions()
        if buffer_w < 2 or buffer_h < 2:
            return False

        read_corner(0, 0)
        read_corner(-1, 0)
        read_corner(0, -1)
        read_corner(-1, -1)
        print("Calibrate....\n\r")

        if not self.display.perform_calibration():
            return False

        return True




    def map_to_display(self, x, y):
        if self.display is None:
            return None
        return self.display.get_pixel_from_input(x, y)

