from extensiones import *
from modules import Action, ActionType, Frame
import importlib
import time
import math


class MenueSwitch:

    startpoint = None
    endpoint = None
    framebuffer = None
    inited = 0

    def __init__(self, framebuffer):
        self.framebuffer = framebuffer
        self.inited = time.time()

    def add_input(self, slot, action):
        if action.type == ActionType.PRESSED:
            if action.pixels[1] < 2:
                if self.startpoint is None:
                    print("Create Start", slot, "on", action.pixels[0])
                    self.startpoint = {slot: action.pixels[0]}
                    return
                if slot not in self.startpoint:
                    for key, val in self.startpoint.items():
                        if abs(val - action.pixels[0]) < 3:
                            print("Add Start", slot, "on", action.pixels[0])
                            self.startpoint[slot] = action.pixels[0]
                            return
            elif self.startpoint is not None and slot in self.startpoint:
                self.startpoint.pop(slot)
        if self.startpoint is None:
            return False
        if action.type == ActionType.RELEASED:
            if action.pixels[1] > self.framebuffer.get_dimensions()[1]-3:
                if slot not in self.startpoint:
                    return
                if self.endpoint is None:
                    print("Create End", slot)
                    self.endpoint = {slot: True}
                if slot not in self.endpoint:
                    print("Add End", slot)
                    self.endpoint[slot] = True
            else:
                if self.endpoint is not None and slot in self.endpoint:
                    self.endpoint.pop(slot)

    def check_switch(self):
        return self.endpoint is not None and len(self.endpoint.keys()) == 3

    def check_timeout(self):
        return time.time() > self.inited + 3



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
        self.frame_buffer.clear_frame()
        for i, ext in enumerate(self.extensions):
            print("Ext:", ext)
            self.draw_icon(ext, i)
        self.frame_buffer.upload_frame()
        # print(self.frame_buffer.frame_matrix)

    def get_active(self):
        return self.is_active

    def process_input(self, slot, input):
        if input.type == ActionType.PRESSED:
            if input.pixels[1] >= self.frame_buffer.get_dimensions()[1]-1:
                if input.pixels[0] < self.frame_buffer.get_dimensions()[0]/2:
                    self.extension_side = (self.extension_side - 1) % math.ceil(len(self.extensions) / 2)
                else:
                    self.extension_side = (self.extension_side + 1) % math.ceil(len(self.extensions) / 2)
                self.frame_buffer.clear_frame()
                for i, ext in enumerate(self.extensions):
                    self.draw_icon(ext, i)
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

        num_icons_per_frame = int(f_width / icon_width)
        # icon_y = int(f_height / 2 - icon_height/2)
        # icon_x = int(icon_width / 2 + icon_width * number)

        icon_y = 1
        icon_x = (number - self.extension_side * num_icons_per_frame) * (icon_width + 1)
        extension.set_icon_pos(icon_x, icon_y)

        # print("Check ", self.extension_side * num_icons_per_frame, " <= ", number, "<", (self.extension_side + 1) * num_icons_per_frame)

        if self.extension_side * num_icons_per_frame <= number < (self.extension_side + 1) * num_icons_per_frame:
            # print(icon)
            # print("ON x:", number - self.extension_side * num_icons_per_frame)
            for y, row in enumerate(icon):
                for x, pix in enumerate(row):
                    self.frame_buffer.set_pixel(x + (number - self.extension_side * num_icons_per_frame) * (icon_width + 1), y + 1, pix[1], pix[0], pix[2])





class ExtensionManager:
    current_active_extension = 0
    extensions = []
    frame_buffer = None

    menue = None
    menue_switch = None



    def __init__(self, framebuffer):
        self.frame_buffer = framebuffer
        Extension.set_global_frame_buffer(framebuffer)
        self.load_from_file("../extensions.txt")
        self.menue = Menue(framebuffer, self.extensions)
        self.menue.set_active()

    def process_input(self, slot, action):
        # print("Slot: ", slot, "Action:", action)
        if self.menue.get_active():
            new_ext = self.menue.process_input(slot, action)
            if new_ext is not None:
                self.current_active_extension = new_ext
                print("Reset")
                self.frame_buffer.clear_frame()
                self.extensions[new_ext].set_active()

        else:
            if self.check_menue_call(slot, action):
                return
            self.extensions[self.current_active_extension].process_input(slot, action)


    def loop(self):
        if not self.menue.get_active():
            self.extensions[self.current_active_extension].loop()
            if self.menue_switch is not None and self.menue_switch.check_timeout():
                self.menue_switch = None


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

