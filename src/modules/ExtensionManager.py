from extensiones import *
from modules import Action, ActionType, Frame
import importlib


class MenueSwitch:

    startpoint = None
    endpoint = None
    framebuffer = None

    def __init__(self, framebuffer):
        self.framebuffer = framebuffer

    def add_input(self, slot, action):
        if action.type == ActionType.PRESSED:
            if action.y < 50:
                if self.startpoint is None:
                    self.startpoint = {slot: action.x}
                    return
                if slot not in self.startpoint:
                    for key, val in self.startpoint.items():
                        if abs(val.x - action.x) < 50:
                            self.startpoint[slot] = action.x
            elif self.startpoint is not None and slot in self.startpoint:
                self.startpoint.pop(slot)
        if action.type == ActionType.RELEASED:
            if action.y > self.framebuffer.get_dimensions()[1]-50:
                if slot not in self.startpoint:
                    return
                if self.endpoint is None:
                    self.endpoint = {slot: True}
                if slot not in self.endpoint:
                    self.endpoint[slot] = True
            else:
                if self.endpoint is not None and slot in self.endpoint:
                    self.endpoint.pop(slot)

    def check_switch(self):
        return len(self.endpoint.keys()) == 3



class Menue:

    frame_buffer = None
    is_active = True
    extensions = None

    extension_side = 0

    def __init__(self, frame_buffer, extensions):
        self.frame_buffer = frame_buffer
        self.extensions = extensions

    def set_active(self):
        self.is_active = True
        self.frame_buffer.set_tales(False)
        for i, ext in enumerate(self.extensions):
            self.draw_icon(ext, i)

    def get_active(self):
        return self.is_active

    def process_input(self, slot, input):
        if input.type == ActionType.PRESSED:
            for i, ext in enumerate(self.extensions):
                if ext.clicked_on_icon(input.pixels[0], input.pixels[1]):
                    self.is_active = False
                    return i
        return None

    def draw_icon(self, extension, number):
        icon = extension.get_icon()
        f_width, f_height = self.frame_buffer.get_dimensions()
        icon_width = 10
        icon_height = 10

        num_icons_per_frame = int(f_width / icon_width) - 1
        icon_y = f_height / 2 - icon_height/2
        icon_x = icon_width / 2 + icon_width * number

        extension.set_icon_pos(icon_x, icon_y)

        if self.extension_side * num_icons_per_frame <= number < (self.extension_side + 1) * num_icons_per_frame:
            for y, row in icon:
                for x, pix in row:
                    self.frame_buffer.set_pixel(x, y, pix[0], pix[1], pix[2])





class ExtensionManager:
    current_active_extension = 0
    extensions = []
    frame_buffer = None

    menue = None
    menue_switch = None



    def __init__(self, framebuffer):
        self.frame_buffer = framebuffer
        Extension.set_global_frame_buffer(framebuffer)
        self.menue = Menue(framebuffer, self.extensions)
        self.menue.set_active()
        pass

    def process_input(self, slot, action):
        if self.menue.get_active():
            new_ext = self.menue.process_input(slot, input)
            if new_ext is not None:
                self.current_active_extension = new_ext
                self.frame_buffer.clear_frame()
                self.extensions[new_ext].set_active()

        else:
            if self.check_menue_call(slot, action):
                return
            self.extensions[self.current_active_extension].process_input(slot, action)


    def loop(self):
        if not self.menue.get_active():
            self.extensions[self.current_active_extension].loop()


    def check_menue_call(self, slot, action):
        if self.menue_switch is None:
            self.menue_switch = MenueSwitch(self.frame_buffer)
        self.menue_switch.add_input(slot, action)
        if self.menue_switch.check_switch():
            self.menue_switch = None
            self.menue.set_active()
            return True
        return False

    def load_from_file(self, file_path):
        f = open(file_path, 'r')
        for ext in f:
            ext = ext.replace('\n', '')
            # print("Module:", __import__("extensiones"))
            class_ = getattr(__import__("extensiones"), ext)
            # print("Class:", class_)
            self.extensions.append(class_())
        f.close()

