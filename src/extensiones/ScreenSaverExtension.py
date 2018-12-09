from .Extension import Extension
from modules.TouchInput import ActionType
import time
import random
import colorsys
import math

current_milli_time = lambda: int(round(time.time() * 1000))

class ScreenSaverExtension(Extension):

    movement_speed = 1
    last_frame = 0

    color_lengh = 5000
    color_step = 0


    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/screensaver.ppm")
        self.dimx, self.dimy = self.framebuffer.get_dimensions()
        self.dots = []
        self.startpoints = {}

    def set_active(self):
        self.last_frame = current_milli_time()
        self.color_step = 0
        self.startpoints.clear()
        self.dots = []
        self.framebuffer.set_tales(True, 30)

    def process_input(self, slot, action):
        if action.type == ActionType.PRESSED:
            self.startpoints[slot] = StartPoint(action.x, action.y, action.pixels)
        if slot in self.startpoints and action.type == ActionType.RELEASED:
            startpoint = self.startpoints[slot]
            pixel, angle, movement = startpoint.get_start(action.x, action.y)
            r, g, b = colorsys.hsv_to_rgb(random.random(), 1, 1)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            dot = Dot(pixel[0], pixel[1], self.framebuffer, R, G, B, angle, movement)
            self.dots.append(dot)

    def loop(self):
        if True or current_milli_time() > self.last_frame + self.movement_speed:
            self.framebuffer.clear_frame()
            for dot in self.dots:
                dot.process()

            self.last_frame = current_milli_time()



class Dot:

    def __init__(self, x, y, framebuffer, r, g, b, angle, movement):
        self.pos = [x*1000, y*1000]
        self.movement_step = movement/40
        self.direction = angle
        self.framebuffer = framebuffer
        self.dimx, self.dimy = self.framebuffer.get_dimensions()
        self.r = r
        self.g = g
        self.b = b
        self.laststep = current_milli_time()

    def process(self):
        rads = math.radians(self.direction)
        movement = (current_milli_time() - self.laststep) * self.movement_step
        self.pos[0] += math.cos(rads) * movement
        self.pos[1] += math.sin(rads) * movement
        self.draw_dot()
        if self.pos[0] > self.dimx * 1000 or self.pos[0] < 0:  # distinction for first axis
            self.direction = (180 - self.direction) % 360
        if self.pos[1] > self.dimy * 1000 or self.pos[1] < 0:  # distinction for second axis
            self.direction = (-self.direction) % 360
        self.laststep = current_milli_time()

    def draw_dot(self):
        pix_x = int(self.pos[0] / 1000)
        pix_y = int(self.pos[1] / 1000)
        self.framebuffer.set_pixel(pix_x, pix_y, self.r, self.g, self.b)



class StartPoint:

    def __init__(self, x, y, pixel):
        self.x = x
        self.y = y
        self.pixel = pixel

    def get_start(self, x, y):
        x_diff = x - self.x
        y_diff = y - self.y
        radians = math.atan2(y_diff, x_diff)
        degrees = math.degrees(radians)
        size = math.hypot(x_diff, y_diff)
        return self.pixel, degrees, size/35





