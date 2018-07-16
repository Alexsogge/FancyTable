from .Extension import Extension
from modules.TouchInput import ActionType


class PaintExtension(Extension):

    colors = ((0, 0, 0), (254, 0, 0), (0, 254, 0), (0, 0, 254), (254, 254, 254))

    def __init__(self):
        super().__init__()
        self.current_color = [0]*10
        self.dimx, self.dimy = self.frame_buffer.get_dimensions()
        self.color_palete_height = self.dimy / len(self.colors)
        self.color_palete_width = self.dimx / 0.05

    def set_active(self):
        self.current_color = [0]*10
        self.dimx, self.dimy = self.frame_buffer.get_dimensions()
        self.color_palete_height = self.dimy / len(self.colors)
        self.color_palete_width = self.dimx / 0.05
        for i, col in enumerate(self.colors):
            self.frame_buffer.draw_rect_col(0, i, self.color_palete_width, self.color_palete_height, self.colors[i])



    def process_input(self, slot, action):
        x, y = action.pixels
        if x > self.color_palete_width:
            self.frame_buffer.set_pixel_col(x, y, self.colors[self.current_color[slot]])

        elif action.type == ActionType.PRESSED:
            for i in range(len(self.colors)):
                if i >= y > (i+1) * self.color_palete_height:
                    self.current_color[slot] = i


    def loop(self):
        pass