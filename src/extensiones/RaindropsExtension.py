from .Extension import Extension
from modules.TouchInput import ActionType
import time
import random
import colorsys
import math

current_milli_time = lambda: int(round(time.time() * 1000))


class Raindrop:


    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 0
        self.expansion_speed = 1
        self.color = color


    def expand(self):
        self.radius += self.expansion_speed

    def draw_drop(self, frame_buffer):
        pass


class RaindropsExtension(Extension):
    switch_speed = 10
    switch_step = 1
    last_frame = 0

    color_lenght = 2000
    color_step = 0

    active_raindrops = []


    def set_active(self):
        pass

    def process_input(self, slot, action):
        if action.type == ActionType.PRESSED:
            self.active_raindrops.append(Raindrop(action.pixels[0], action.pixels[1], (255, 255, 255)))


    def loop(self):
        i = 0
        while i < len(self.active_raindrops):
            raindrop = self.active_raindrops[i]
            if raindrop.radius > math.max(self.framebuffer.get_dimensions()):
                self.active_raindrops.remove(raindrop)
                i -= 1
            else:
                raindrop.draw_drop(self.framebuffer)
                raindrop.expand()