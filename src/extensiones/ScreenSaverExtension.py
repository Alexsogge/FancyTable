from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
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
        self.dimx, self.dimy = self.render_engine.frame_buffer.get_dimensions()
        self.dots = []
        self.startpoints = {}

    def set_active(self):
        self.last_frame = current_milli_time()
        self.color_step = 0
        self.startpoints.clear()
        self.dots = []
        self.render_engine.set_tales(True, 30)

    def process_input(self, action):
        if action.type == ActionType.PRESSED:
            self.startpoints[action.z] = StartPoint(action.x, action.y, action.pixels)
        if action.z in self.startpoints and action.type == ActionType.RELEASED:
            startpoint = self.startpoints.pop(action.z)
            pixel, angle, movement = startpoint.get_start(action.x, action.y)
            dot = Dot(action.pixels[0], action.pixels[1], self.render_engine, Colors.generate_random(), angle, movement)
            self.dots.append(dot)

    def loop(self, time_delta):
        if True or current_milli_time() > self.last_frame + self.movement_speed:
            self.render_engine.clear_buffer()
            for dot in self.dots:
                dot.process(self.startpoints)

            self.last_frame = current_milli_time()



class StartPoint:

    def __init__(self, x, y, pixel):
        self.x = x
        self.y = y
        self.pixel = pixel

    def get_start(self, x, y):
        x_diff = self.x - x
        y_diff = self.y - y
        radians = math.atan2(y_diff, x_diff)
        degrees = math.degrees(radians)
        size = math.hypot(x_diff, y_diff)
        return self.pixel, degrees, size/20

class Dot:

    def __init__(self, x, y, render_engine: RenderingEngine, color: Color, angle, movement):
        self.pos = [x, y]
        self.movement_step = movement
        self.direction = angle
        self.render_engine = render_engine
        self.dimx, self.dimy = self.render_engine.get_dimensions()
        self.color = color
        self.laststep = current_milli_time()

    def process(self, startpoints):
        rads = math.radians(self.direction)
        movement = (current_milli_time() - self.laststep) * self.movement_step
        self.pos[0] += math.cos(rads) * movement
        self.pos[1] += math.sin(rads) * movement
        self.draw_dot()
        if self.pos[0] > self.dimx or self.pos[0] < 0:  # distinction for first axis
            self.direction = (180 - self.direction) % 360
        if self.pos[1] > self.dimy or self.pos[1] < 0:  # distinction for second axis
            self.direction = (-self.direction) % 360
        self.laststep = current_milli_time()

        # for point in startpoints:
        #     if point.pixel[0] == int(self.pos[0]/1000) and point.pixel[1] == int(self.pos[1]/1000):
        #         self.direction *= -1
        #         break

    def draw_dot(self):
        pix_x = int(self.pos[0])
        pix_y = int(self.pos[1])
        self.render_engine.draw_pixel(pix_x, pix_y, self.color)



