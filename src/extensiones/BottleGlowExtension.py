from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
import time
import random
import colorsys
import math

current_milli_time = lambda: int(round(time.time() * 1000))


class BottleGlowExtension(Extension):

    movement_speed = 1
    last_frame = 0

    color_lengh = 5000
    color_step = 0


    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/bottleglow.ppm")
        self.dimx, self.dimy = self.render_engine.get_dimensions()
        self.points = {}

    def set_active(self):
        self.last_frame = current_milli_time()
        self.color_step = 0
        self.points.clear()
        self.dots = []
        #self.framebuffer.set_tales(True, 2)

    def process_input(self, action):
        if action.type == ActionType.PRESSED:
            self.points[action.z] = Dot(action.pixels[0], action.pixels[1], Colors.generate_random(), self.render_engine)
        if action.z in self.points and action.type == ActionType.MOVED:
            self.points[action.z].update_pos(action.pixels[0], action.pixels[1])
        if action.z in self.points and action.type == ActionType.RELEASED:
            del self.points[action.z]

    def loop(self, time_delta: float):
        if current_milli_time() > self.last_frame + self.movement_speed:
            self.render_engine.clear_buffer()
            for key, point in self.points.items():
                point.expand()
                point.draw_drop()

            self.last_frame = current_milli_time()



class Dot:

    def __init__(self, x, y, color: Color, render_engine: RenderingEngine):
        self.x = x
        self.y = y
        self.radius = 1
        self.expansion_speed = 0.0000005
        self.color: Color = color
        self.initiated = current_milli_time()
        self.render_engine: RenderingEngine = render_engine
        self.direction = 1
        self.intense = 1

    def expand(self):
        self.intense += (current_milli_time() - self.initiated) * (self.expansion_speed * (1000 * (self.intense))) * self.direction
        #print(self.radius)
        #print("Speed:", self.expansion_speed)
        #print("intense:", self.intense)
        #print("mul:", self.expansion_speed * (10 ** self.intense))
        if self.intense > 3:
            self.direction = -1
        if self.intense < 0.8:
            self.direction = 1
        self.initiated = current_milli_time()


    def draw_drop(self):
        """
        d = −r
        x = r
        y = 0
        Wiederhole bis y > x
            Pixel (x, y) sowie symmetrische Pixel einfärben
            d = d + 2×y + 1
            y = y + 1
            Wenn d > 0
                d = d - 2×x + 2
                x = x - 1
        :param frame_buffer:
        :return:
        """
        self.render_engine.draw_circle(self.x, self.y, self.radius, self.color)


    def update_pos(self, x, y):
        self.x = x
        self.y = y







