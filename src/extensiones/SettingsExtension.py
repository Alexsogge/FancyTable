from .Extension import Extension
from modules.Helpers import *


class SettingsExtension(Extension):

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/settings.ppm")
        self.last_pointer = None

    def set_active(self):
        self.render_engine.draw_rectangle_wh(2, 2, 20, 20, Colors.generate_color(Colors.WHITE))
        self.render_engine.draw_rectangle_wh(0, 0, 2, 2, Colors.RED)
        pass

    def process_input(self, action):
        updated = False

        if self.last_pointer is None:
            self.last_pointer = (action.x, action.y)
            return

        if action.pixels[0] <= 2 and action.pixels[1] <= 2:
            self.extension_manager.close_extension()
        elif abs(self.last_pointer[1] - action.y) > 200:
            self.render_engine.inc_diming(int((self.last_pointer[1] - action.y) / abs(self.last_pointer[1] - action.y)) * 0.00003)
            updated = True
        if updated:
            self.last_pointer = (action.x, action.y)

    def loop(self, time_delta):
        pass
