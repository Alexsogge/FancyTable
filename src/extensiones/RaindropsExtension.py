from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
import time
from modules import Framebuffer
import random
import colorsys
import math

current_milli_time = lambda: int(round(time.time() * 1000))


class Raindrop:
    def __init__(self, x, y, color: Color):
        self.x = x
        self.y = y
        self.radius = 0
        self.expansion_speed = 0.02
        self.color: Color = color
        self.initiated = current_milli_time()


    def expand(self):
        self.radius = (current_milli_time() - self.initiated) * self.expansion_speed



    def draw_drop(self, render_engine: RenderingEngine):
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
        render_engine.draw_circle(x, y, self.radius, self.color)



class RaindropsExtension(Extension):
    switch_speed = 10
    switch_step = 1
    last_frame = 0

    color_lenght = 2000
    color_step = 0

    active_raindrops = []

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/raindrop.ppm")


    def set_active(self):
        self.render_engine.set_tales(True, 20)

    def process_input(self, action):
        if action.type == ActionType.PRESSED:
            self.active_raindrops.append(Raindrop(action.pixels[0], action.pixels[1], Colors.generate_random()))


    def loop(self, time_delta):
        self.render_engine.clear_buffer()
        i = 0
        while i < len(self.active_raindrops):
            raindrop = self.active_raindrops[i]
            if raindrop.radius > math.sqrt(self.render_engine.frame_buffer.get_dimensions()[0]**2 +
                                           self.render_engine.frame_buffer.get_dimensions()[1]**2):
            #if raindrop.radius > max(self.framebuffer.get_dimensions()):
                self.active_raindrops.remove(raindrop)
                i -= 1
            else:
                raindrop.draw_drop(self.render_engine)
                raindrop.expand()
            i += 1