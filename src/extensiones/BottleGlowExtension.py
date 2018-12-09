from .Extension import Extension
from modules.TouchInput import ActionType
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
        self.dimx, self.dimy = self.framebuffer.get_dimensions()
        self.points = {}

    def set_active(self):
        self.last_frame = current_milli_time()
        self.color_step = 0
        self.points.clear()
        self.dots = []
        #self.framebuffer.set_tales(True, 2)

    def process_input(self, slot, action):
        if action.type == ActionType.PRESSED:
            r, g, b = colorsys.hsv_to_rgb(random.random(), 1, 1)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            self.points[slot] = Dot(action.pixels[0], action.pixels[1], [R, G, B], self.framebuffer)
        if slot in self.points and action.type == ActionType.MOVED:
            self.points[slot].update_pos(action.pixels[0], action.pixels[1])
        if slot in self.points and action.type == ActionType.RELEASED:
            del self.points[slot]

    def loop(self):
        if current_milli_time() > self.last_frame + self.movement_speed:
            self.framebuffer.clear_frame()
            for key, point in self.points.items():
                point.expand()
                point.draw_drop()

            self.last_frame = current_milli_time()



class Dot:

    def __init__(self, x, y, color, framebuffer):
        self.x = x
        self.y = y
        self.radius = 1
        self.expansion_speed = 0.0000005
        self.color = color
        self.initiated = current_milli_time()
        self.framebuffer = framebuffer
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

    def symetry_dots(self, x, y):
        self.framebuffer.set_pixel_col(x + self.x, y + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(-x + self.x, y + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(x + self.x, -y + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(-x + self.x, -y + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(y + self.x, x + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(-y + self.x, x + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(y + self.x, -x + self.y, [i / self.intense for i in self.color])
        self.framebuffer.set_pixel_col(-y + self.x, -x + self.y, [i / self.intense for i in self.color])

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
        self.framebuffer.set_pixel_col(self.x, self.y, [i / self.intense for i in self.color])
        d = -self.radius
        x = self.radius
        y = 0
        while y <= x:
            self.symetry_dots(x, y)
            d = d + 2 * y + 1
            y = y + 1
            if d > 0:
                d = d - 2 * x + 2
                x = x - 1

    def update_pos(self, x, y):
        self.x = x
        self.y = y







