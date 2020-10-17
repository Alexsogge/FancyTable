from modules.ConfigAdapter import ConfigAdapter
from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
import time
import random
import colorsys
import math

current_milli_time = lambda: int(round(time.time() * 1000))


class BottleGlowExtension(Extension):

    update_speed = 0.1

    color_lengh = 5000
    color_step = 0


    def __init__(self):
        self.default_config = {'offset': 0.2, 'radius': 1, 'polynom': 2, 'zyklus_time': 8}
        super().__init__()
        self.icon_pic = self.read_icon("../icons/bottleglow.ppm")
        self.dimx, self.dimy = self.render_engine.get_dimensions()
        self.points = {}
        self.passed_time = 0

    def set_active(self):
        self.color_step = 0
        self.points.clear()
        self.dots = []
        self.passed_time = 0
        self.render_engine.set_tales(False)

    def process_input(self, action):
        if action.type == ActionType.PRESSED:
            self.points[action.z] = Dot(action.pixels[0], action.pixels[1], Colors.generate_random(),
                                        self.render_engine, self.config)
        if action.z in self.points and action.type == ActionType.MOVED:
            self.points[action.z].update_pos(action.pixels[0], action.pixels[1])
        if action.z in self.points and action.type == ActionType.RELEASED:
            del self.points[action.z]

    def loop(self, time_delta: float):
        self.passed_time += time_delta
        for key, point in self.points.items():
            point.expand(time_delta)
        if self.passed_time > self.update_speed:
            self.passed_time = 0
            self.render_engine.clear_buffer()
            for key, point in self.points.items():
                point.draw_drop()




class Dot:

    def __init__(self, x, y, color: Color, render_engine: RenderingEngine, config: Dict):
        self.x = x
        self.y = y
        self.offset = config['offset']
        self.radius = config['radius']
        self.polynom = config['polynom']
        self.zyklus_time = config['zyklus_time']
        self.expansion_speed = 1/(self.zyklus_time**self.polynom)
        self.expansion_speed_neg = -(1/self.zyklus_time)-(self.expansion_speed*self.zyklus_time**(self.polynom-1))
        self.color: Color = color
        self.initiated = current_milli_time()
        self.render_engine: RenderingEngine = render_engine
        self.direction = 1
        self.intense = 1
        self.passed_time = 0

    def expand(self, time_delta):
        # self.intense += (current_milli_time() - self.initiated) * (self.expansion_speed * (1000 * (self.intense))) * self.direction
        #print(self.radius)
        #print("Speed:", self.expansion_speed)
        #print("intense:", self.intense)
        #print("mul:", self.expansion_speed * (10 ** self.intense))
        self.passed_time += time_delta
        if self.direction == 1:
            self.intense = self.passed_time**self.polynom * self.expansion_speed + self.offset
        else:
            self.intense = self.passed_time**self.polynom * self.expansion_speed + self.expansion_speed_neg * self.passed_time + 1
        # print(self.intense)
        if self.intense >= 1 and self.direction == 1:
            self.direction = -1
            self.intense = 1
            print(self.passed_time)
            self.passed_time = 0

        if self.intense <= self.offset and self.direction == -1:
            self.direction = 1
            self.intense = self.offset
            self.passed_time = 0
        self.color.a = self.intense


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
        self.render_engine.draw_pixel(self.x, self.y, self.color)
        self.render_engine.draw_circle(self.x, self.y, 1, self.color)


    def update_pos(self, x, y):
        self.x = x
        self.y = y







