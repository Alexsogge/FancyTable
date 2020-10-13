from .Extension import Extension
import colorsys
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine




class SingleColorExtension(Extension):

    last_pointer = None
    offset = 1
    color_select = 0
    # color_length = 500
    color_length = 1

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/singlecolor.ppm")
        self.w, self.h = self.render_engine.frame_buffer.get_dimensions()

    def set_active(self):
        r, g, b = colorsys.hsv_to_rgb(self.color_select / self.color_length, 1, 1)
        R, G, B = max(min(int(255 * r) + self.offset, 255), 0), max(min(int(255 * g) + self.offset, 255), 0), \
                  max(min(int(255 * b) + self.offset, 255), 0)

        self.render_engine.draw_rectangle_wh(0, 0, self.w, self.h, Color(R, G, B))

    def process_input(self, action):
        updated = False
        if self.last_pointer is None:
            self.last_pointer = (action.x, action.y)
            return

        if abs(self.last_pointer[0] - action.x) > 0.03:
            # self.color_select += int((self.last_pointer[0] - action.x) / abs(self.last_pointer[0] - action.x))
            # self.color_select = self.color_select % self.color_length

            self.color_select = action.x
            updated = True


        if abs(self.last_pointer[1] - action.y) > 0.03:
            # self.offset += int((self.last_pointer[1] - action.y) / abs(self.last_pointer[1] - action.y)) * 0.01
            # self.offset = max(min(self.offset, 1), 0)
            self.offset = action.y
            updated = True


        if updated:
            self.last_pointer = (action.x, action.y)

            r, g, b = colorsys.hsv_to_rgb(self.color_select, 1, (1-self.offset) * 255)
            # print(self.color_select, '->', r, g, b)
            R, G, B = max(min(int(255 * r * self.offset), 255), 0), max(min(int(255 * g * self.offset), 255), 0),\
                      max(min(int(255 * b * self.offset), 255), 0)

            self.render_engine.draw_rectangle(0, 0, self.w, self.h, Color(int(r), int(g), int(b)))


    def loop(self, time_delta):
        pass