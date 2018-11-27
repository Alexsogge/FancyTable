from .Extension import Extension


class SettingsExtension(Extension):

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/settings.ppm")
        self.last_pointer = None

    def set_active(self):
        self.framebuffer.draw_rect(2, 2, 20, 20, 255, 255, 255)
        self.framebuffer.draw_rect(0, 0, 2, 2, 0, 255, 0)
        pass

    def process_input(self, slot, action):
        updated = False

        if self.last_pointer is None:
            self.last_pointer = (action.x, action.y)
            return

        if action.pixels[0] <= 2 and action.pixels[1] <= 2:
            self.extensionmanager.close_extension()
        elif abs(self.last_pointer[1] - action.y) > 200:
            self.framebuffer.inc_diming(int((self.last_pointer[1] - action.y) / abs(self.last_pointer[1] - action.y)) * 0.00003)
            updated = True
        if updated:
            self.last_pointer = (action.x, action.y)

    def loop(self):
        pass
