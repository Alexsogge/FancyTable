from modules.ConfigAdapter import ConfigAdapter
from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
import time
import random
import colorsys
import math
import datetime

current_milli_time = lambda: int(round(time.time() * 1000))

candle_pos = [4, 7, 13, 16]

def get_num_candles():
    return 4
    now = datetime.datetime.now()
    christmas = datetime.datetime(now.year, 12, 25, 0, 0, 0)
    weekday = christmas.weekday()

    for i in range(3, -1, -1):
        if now < christmas - datetime.timedelta(weekday + 1 + i * 7):
            return 3 - i
    return 4


class AdventWreathExtension(Extension):

    update_speed = 0.01

    color_lengh = 5000
    color_step = 0


    def __init__(self):
        self.default_config = {'offset': 0.4, 'polynom': 2, 'zyklus_time': 8}
        super().__init__()
        self.icon_pic = self.read_icon("../icons/adventwreath.ppm")
        self.dimx, self.dimy = self.render_engine.get_dimensions()
        self.candles = []
        self.passed_time = 0

    def set_active(self):
        self.color_step = 0
        self.candles = []
        self.passed_time = 0
        self.render_engine.set_tales(False)
        for i in range(get_num_candles()):
            candle = Candle(candle_pos[i], int(self.dimy/2) - 1, Colors.generate_random(), self.render_engine, self.config)
            self.candles.append(candle)

    def process_input(self, action):
        pass

    def loop(self, time_delta: float):
        self.passed_time += time_delta
        for candle in self.candles:
            candle.expand(time_delta)
        if self.passed_time > self.update_speed or True:
            self.passed_time = 0
            self.render_engine.clear_buffer()
            for candle in self.candles:
                candle.draw()



class Candle:

    def __init__(self, x, y, color: Color, render_engine: RenderingEngine, config: Dict):
        self.x = x
        self.y = y
        self.offset = config['offset']
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
            # print(self.passed_time)
            self.passed_time = 0

        if self.intense <= self.offset and self.direction == -1:
            self.direction = 1
            self.intense = self.offset
            self.passed_time = 0
        self.color.a = self.intense


    def draw(self):
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


