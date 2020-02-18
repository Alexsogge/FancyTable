from extensiones import *
from modules.Helpers import *
from modules.Framebuffer import Frame
from modules.RenderingEngine import RenderingEngine
import importlib
import time
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.WebServerConnection import WebServerConnection


class MenueSwitch:
    """
    Checks for a 3 finger swipe from top to bottom for back to home screen
    """


    def __init__(self, framebuffer):
        self.startpoint: Union[None, Dict[int, int]] = None
        self.endpoint = None
        self.framebuffer = None
        self.inited = 0
        self.framebuffer = framebuffer
        self.inited = time.time()

    def add_input(self, action: Action):
        if action.type == ActionType.PRESSED:
            if action.pixels[1] <= 2:
                if self.startpoint is None:
                    # print("Create Start", action.z, "on", action.pixels[0])
                    self.startpoint = {action.z: action.pixels[0]}
                    return
                if action.z not in self.startpoint:
                    for key, val in self.startpoint.items():
                        if abs(val - action.pixels[0]) <= 3:
                            # print("Add Start", action.z, "on", action.pixels[0])
                            self.startpoint[action.z] = action.pixels[0]
                            return
            elif self.startpoint is not None and action.z in self.startpoint:
                self.startpoint.pop(action.z)
        if self.startpoint is None:
            return False
        if action.type == ActionType.RELEASED:
            if action.pixels[1] >= self.framebuffer.get_dimensions()[1]-3:
                if action.z not in self.startpoint:
                    return
                if self.endpoint is None:
                    print("Create End", action.z)
                    self.endpoint = {action.z: True}
                if action.z not in self.endpoint:
                    print("Add End", action.z)
                    self.endpoint[action.z] = True
            else:
                if self.endpoint is not None and action.z in self.endpoint:
                    self.endpoint.pop(action.z)

    def check_switch(self) -> bool:
        return self.endpoint is not None and len(self.endpoint.keys()) == 3

    def check_timeout(self) -> bool:
        return time.time() > self.inited + 3



class Menue:

    def __init__(self, render_engine: RenderingEngine, extensions):
        self.render_engine = render_engine
        self.extensions = extensions
        self.is_active = True

        self.extension_side = 0

    def set_active(self):
        self.is_active = True
        self.render_engine.set_tales(False)
        self.render_engine.clear_buffer()
        for i, ext in enumerate(self.extensions):
            print("Ext:", ext)
            self.draw_icon(ext, i)
        self.render_engine.upload_buffer()
        # print(self.frame_buffer.frame_matrix)

    def get_active(self):
        return self.is_active

    def process_input(self, input: Action):
        if input.type == ActionType.PRESSED:
            print("Menuetest: ", input.pixels[1] , "vs", self.render_engine.frame_buffer.height-1)
            if input.pixels[1] >= self.render_engine.frame_buffer.height-1:
                print("Bottom line")
                if input.pixels[0] < self.render_engine.frame_buffer.width/2:
                    self.extension_side = (self.extension_side - 1) % math.ceil(len(self.extensions) / 2)
                else:
                    self.extension_side = (self.extension_side + 1) % math.ceil(len(self.extensions) / 2)
                self.render_engine.clear_buffer()
                for i, ext in enumerate(self.extensions):
                    self.draw_icon(ext, i)
            for i, ext in enumerate(self.extensions):
                if ext.clicked_on_icon(input.pixels[0], input.pixels[1]):
                    self.is_active = False
                    return i
        return None

    def draw_icon(self, extension, number):
        icon = extension.get_icon()
        f_width, f_height = self.render_engine.get_dimensions()
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
                    self.render_engine.draw_pixel(x + (number - self.extension_side * num_icons_per_frame) * (icon_width + 1),
                                                  y + 1, Color(pix[0], pix[1], pix[2]))





class ExtensionManager:




    def __init__(self, render_engine: RenderingEngine, websocket_connection=None):
        self.render_engine: RenderingEngine = render_engine
        self.websocket_connection = websocket_connection
        Extension.set_global_render_engine(render_engine)
        Extension.set_global_extension_manager(self)
        Extension.set_global_websocket_connection(self.websocket_connection)

        self.current_active_extension: int = 0
        self.extensions: List[Extension] = []
        self.menue_switch: Union[None, MenueSwitch] = None

        self.load_from_file("../extensions.txt")
        self.menue: Menue = Menue(render_engine, self.extensions)
        self.menue.set_active()

    def process_input(self, action):
        # print("Slot: ", slot, "Action:", action)
        if self.menue.get_active():
            new_ext = self.menue.process_input(action)
            if new_ext is not None:
                self.current_active_extension = new_ext
                print("Reset")
                self.render_engine.clear_buffer()
                self.extensions[new_ext].set_active()

        else:
            if self.check_menue_call(action):
                return
            self.extensions[self.current_active_extension].process_input(action)


    def loop(self, time_delta: float):
        if not self.menue.get_active():
            self.extensions[self.current_active_extension].loop(time_delta)
            if self.menue_switch is not None and self.menue_switch.check_timeout():
                self.menue_switch = None

    def check_menue_call(self, action: Action):
        if self.menue_switch is None:
            self.menue_switch = MenueSwitch(self.render_engine)
        self.menue_switch.add_input(action)
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

    def close_extension(self):
        self.menue_switch = None
        self.menue.set_active()


    def open_extension(self, extension_name: str):
        # @TODO: replace extenlist with dict -> replace following
        for i, extension in enumerate(self.extensions):
            print(type(extension).__name__ )
            if type(extension).__name__ == extension_name:
                print("Switch to", extension)
                self.current_active_extension = i
                self.render_engine.set_tales(False)
                self.render_engine.clear_buffer()
                self.menue.is_active = False
                extension.set_active()
                break
