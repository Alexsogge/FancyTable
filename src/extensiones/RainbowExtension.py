from .Extension import Extension
from modules.TouchInput import ActionType
import time
import random
import colorsys

current_milli_time = lambda: int(round(time.time() * 1000))

class RainbowExtension(Extension):

    switch_speed = 10
    switch_step = 1
    last_frame = 0

    color_lengh = 5000
    color_step = 0

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/rainbow.ppm")

    def set_active(self):
        self.last_frame = current_milli_time()
        self.color_step = 0

    def process_input(self, slot, action):
        pass

    def loop(self):
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
            for i in range(self.framebuffer.get_dimensions()[0]):
                r, g, b = colorsys.hsv_to_rgb(((self.color_step + i * 100) % self.color_lengh) / self.color_lengh, 1, 1)
                R, G, B = int(255 * r), int(255 * g), int(255 * b)
                column = []
                for j in range(self.framebuffer.get_dimensions()[1]):
                  column.append({'r': R, 'g': G, 'b': B})
                # print(i, "->", column)
                self.framebuffer.set_matrix_column(i, column)

            self.last_frame = current_milli_time()
            self.color_step = (self.color_step + self.switch_speed)









