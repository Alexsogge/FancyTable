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

    color_lenght = 2000
    color_step = 0


    def set_active(self):
        self.last_frame = current_milli_time
        self.color_step = 0

    def process_input(self, slot, action):
        pass

    def loop(self):
        if current_milli_time() > self.last_frame + self.switch_speed:
            r, g, b = colorsys.hsv_to_rgb(self.color_step / self.color_lenght, 1, 1)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            column = []
            for col in range(1, self.framebuffer.get_dimensions()[0]):
                self.framebuffer.set_matrix_column(col, self.framebuffer.get_matrix_column(col-1))
            for i in range(self.framebuffer.get_dimensions()[1]):
                column.append({'r': R, 'g': G, 'b': B})
            self.framebuffer.set_matrix_column(column)
            self.last_frame = current_milli_time()
            self.color_step = (self.color_step + 1) % self.color_lenght










