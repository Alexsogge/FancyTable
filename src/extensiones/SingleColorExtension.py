from .Extension import Extension
import colorsys




class SingleColorExtension(Extension):

    last_pointer = None
    offset = 1
    color_select = 0
    color_length = 500

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/singlecolor.ppm")
        self.w, self.h = self.framebuffer.get_dimensions()

    def set_active(self):
        r, g, b = colorsys.hsv_to_rgb(self.color_select / self.color_length, 1, 1)
        R, G, B = max(min(int(255 * r) + self.offset, 255), 0), max(min(int(255 * g) + self.offset, 255), 0), \
                  max(min(int(255 * b) + self.offset, 255), 0)

        self.framebuffer.draw_rect(0, 0, self.w, self.h, R, G, B)

    def process_input(self, slot, action):
        updated = False
        if self.last_pointer is None:
            self.last_pointer = (action.x, action.y)
            return

        if abs(self.last_pointer[0] - action.x) > 200:
            self.color_select += int((self.last_pointer[0] - action.x) / abs(self.last_pointer[0] - action.x))
            self.color_select = self.color_select % self.color_length

            updated = True
        elif abs(self.last_pointer[1] - action.y) > 200:
            self.offset += int((self.last_pointer[1] - action.y) / abs(self.last_pointer[1] - action.y)) * 0.01
            self.offset = max(min(self.offset, 1), 0)
            updated = True


        if updated:
            self.last_pointer = (action.x, action.y)

            r, g, b = colorsys.hsv_to_rgb(self.color_select / self.color_length, 1, 1)
            R, G, B = max(min(int(255 * r * self.offset), 255), 0), max(min(int(255 * g * self.offset), 255), 0),\
                      max(min(int(255 * b * self.offset), 255), 0)

            self.framebuffer.draw_rect(0, 0, self.w, self.h, R, G, B)


    def loop(self):
        pass