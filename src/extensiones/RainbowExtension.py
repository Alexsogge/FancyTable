from .Extension import Extension
from modules.Helpers import *
import time
import random
import colorsys

current_milli_time = lambda: int(round(time.time() * 1000))

class RainbowExtension(Extension):

    def __init__(self):
        super().__init__()
        self.switch_speed = 10
        self.switch_step = 1
        self.last_frame = 0

        self.color_lengh = 5000
        self.color_step = 0
        self.icon_pic = self.read_icon("../icons/rainbow.ppm")

    def set_active(self):
        self.last_frame = current_milli_time()
        self.color_step = 0

    def process_input(self, action):
        self.switch_speed = 50 * action.x

    def loop(self, time_delta):
        if current_milli_time() > self.last_frame + self.switch_speed:
            # r, g, b = colorsys.hsv_to_rgb(self.color_step / self.color_lengh, 1, 1)
            # R, G, B = int(255 * r), int(255 * g), int(255 * b)
            # column = []
            # for col in reversed(range(1, self.framebuffer.get_dimensions()[0])):
            #     self.framebuffer.set_matrix_column(col, self.framebuffer.get_matrix_column(col-1))
            # for i in range(self.framebuffer.get_dimensions()[1]):
            #    column.append({'r': R, 'g': G, 'b': B})
            # self.framebuffer.set_matrix_column(0, column)
            # print(self.color_step)
            for i in range(self.render_engine.frame_buffer.get_dimensions()[0]):
                color = Colors.generate_from_pallete(self.color_step + i * 100)
                self.render_engine.draw_column(i, color)

            self.last_frame = current_milli_time()
            self.color_step = (self.color_step + self.switch_speed)









