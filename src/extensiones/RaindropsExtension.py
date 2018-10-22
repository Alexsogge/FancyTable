from .Extension import Extension
from modules.TouchInput import ActionType
import time
from modules import Framebuffer
import random
import colorsys
import math

current_milli_time = lambda: int(round(time.time() * 1000))


class Raindrop:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = 0
        self.expansion_speed = 0.02
        self.color = color
        self.initiated = current_milli_time()


    def expand(self):
        self.radius = (current_milli_time() - self.initiated) * self.expansion_speed


    def symetry_dots(self, x, y, frame_buffer):
        frame_buffer.set_pixel_col(x + self.x, y + self.y, self.color)
        frame_buffer.set_pixel_col(-x + self.x, y + self.y, self.color)
        frame_buffer.set_pixel_col(x + self.x, -y + self.y, self.color)
        frame_buffer.set_pixel_col(-x + self.x, -y + self.y, self.color)
        frame_buffer.set_pixel_col(y + self.x, x + self.y, self.color)
        frame_buffer.set_pixel_col(-y + self.x, x + self.y, self.color)
        frame_buffer.set_pixel_col(y + self.x, -x + self.y, self.color)
        frame_buffer.set_pixel_col(-y + self.x, -x + self.y, self.color)


    def draw_drop(self, frame_buffer: Framebuffer.Frame):
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
        d = -self.radius
        x = self.radius
        y = 0
        while y <= x:
            self.symetry_dots(x, y, frame_buffer)
            d = d + 2*y + 1
            y = y + 1
            if d > 0:
                d = d - 2*x + 2
                x = x - 1



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
        self.framebuffer.set_tales(True, 20)

    def process_input(self, slot, action):
        if action.type == ActionType.PRESSED:
            r, g, b = colorsys.hsv_to_rgb(random.random(), 1, 1)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            self.active_raindrops.append(Raindrop(action.pixels[0], action.pixels[1], (R, G, B)))


    def loop(self):
        self.framebuffer.clear_frame()
        i = 0
        while i < len(self.active_raindrops):
            raindrop = self.active_raindrops[i]
            if raindrop.radius > math.sqrt(self.framebuffer.get_dimensions()[0]**2 + self.framebuffer.get_dimensions()[1]**2):
            #if raindrop.radius > max(self.framebuffer.get_dimensions()):
                self.active_raindrops.remove(raindrop)
                i -= 1
            else:
                raindrop.draw_drop(self.framebuffer)
                raindrop.expand()
            i += 1