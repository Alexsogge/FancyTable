from .Extension import Extension
from modules.Helpers import ActionType
from modules.Helpers import *

class PaintExtension(Extension):

    colors = (Colors.BLACK, Colors.WHITE, Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW, Colors.CYAN, Colors.PURPLE)

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/paint.ppm")
        self.current_color: List[Color] = [Colors.generate_color(Colors.BLACK)]*10
        self.dimx, self.dimy = self.render_engine.frame_buffer.get_dimensions()
        self.color_palete_height = self.dimy / len(self.colors)
        self.color_palete_width = self.dimx / 0.05

    def set_active(self):
        self.current_color: List[Color] = [Colors.generate_color(Colors.BLACK)]*10
        self.dimx, self.dimy = self.render_engine.frame_buffer.get_dimensions()
        self.color_palete_height = max(int(self.dimy / len(self.colors)), 1)
        self.color_palete_width = max(int(self.dimx * 0.05), 1)
        for i, col in enumerate(self.colors):
            self.render_engine.draw_rectangle(0, i, self.color_palete_width, i + self.color_palete_height, self.colors[i])



    def process_input(self, action):
        x, y = action.pixels
        # print("Paint process", x, ">", self.color_palete_width)
        if x > self.color_palete_width:
            # print("Draw:", self.colors[self.current_color[slot]])
            self.render_engine.draw_pixel(x, y, self.current_color[action.z])

        elif action.type == ActionType.PRESSED:
            for i in range(len(self.colors)):
                # print(i, "<= ", y, "<", (i+1) * self.color_palete_height)
                if i <= y < (i+1) * self.color_palete_height:
                    # print("Update color", i)
                    self.current_color[action.z] = Colors.generate_color(self.colors[i])


    def loop(self, time_delta):
        pass