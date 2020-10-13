from abc import ABC, abstractmethod
from modules import Framebuffer


from modules.RenderingEngine import RenderingEngine
from modules.ConfigAdapter import ConfigAdapter
from typing import Dict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.ExtensionManager import ExtensionManager
    from modules.WebServerConnection import WebServerConnection
    from modules.InputDevice import InputDevice


class Extension(ABC):
    render_engine: RenderingEngine = None
    extension_manager: 'ExtensionManager' = None
    websocket_connection: 'WebServerConnection' = None
    input_device: 'InputDevice' = None
    default_config = dict()

    def __init__(self):
        """
        Initialize an empty default extension
        """
        self.icon_x = None
        self.icon_y = None
        self.icon_width = 10
        self.icon_height = 10
        self.icon_pic = self.read_icon("../icons/nonpic.ppm")
        self.config_adapter: ConfigAdapter = ConfigAdapter(self._type(), self.default_config)
        self.config: Dict = self.config_adapter.config

    @classmethod
    def set_global_render_engine(cls, render_engine: RenderingEngine):
        """
        Sets the frame buffer for all extensions
        :param render_engine:
        """
        cls.render_engine = render_engine

    @classmethod
    def set_global_input_device(cls, input_device: 'InputDevice'):
        """
        Sets the input device for all extensions
        :param input_device:
        """
        cls.input_device = input_device

    @classmethod
    def set_global_extension_manager(cls, mgr: 'ExtensionManager'):
        """
        Sets the frame buffer for all extensions
        :param mgr:
        """
        cls.extension_manager = mgr

    @classmethod
    def set_global_websocket_connection(cls, wsc: 'WebServerConnection'):
        """
        Sets the web_socket_connection for all extensions
        :param wsc: websocket_connection
        """
        cls.websocket_connection = wsc

    def get_icon(self):
        """
        Return the icon as rgb matrix
        :return: List of lists of (red, green, blue)
        """
        return self.icon_pic

    def set_icon_pos(self, x, y):
        """
        Sets the position of the icon
        :param x:
        :param y:
        """
        self.icon_x = x
        self.icon_y = y

    def set_icon_dimensions(self, width, height):
        self.icon_width = width
        self.icon_height = height

    def clicked_on_icon(self, x, y):
        # print(self.icon_x, "<=", x, "<=", self.icon_x + self.icon_width, "and", self.icon_y, "<", y, "<", self.icon_y + self.icon_height)
        return self.icon_x <= x <= self.icon_x + self.icon_width and \
                self.icon_y < y < self.icon_y + self.icon_height

    @abstractmethod
    def set_active(self):
        pass

    @abstractmethod
    def process_input(self, action):
        pass

    @abstractmethod
    def loop(self, time_delta: float):
        pass

    def _type(self):
        return self.__class__.__name__

    def write_default_config(self):
        for key, value in self.default_config.items():
            self.config_adapter.set_value(key, value)

    def read_icon(self, filename):
        """
        >>> ir = IconFileReader()
        >>> ir.read_icon("./icon/wuerfeln.ppm")

        :param filename:
        :return:
        """
        header_code = None
        width = None
        height = None
        max_val = None
        icon = []
        readed_lines = 0
        if filename[-4:] == ".ppm":
            pic = open(filename, 'r')
            if pic is None:
                return "File not found"
            for line in pic:
                if line[0] == '#':
                    continue
                if header_code is None:
                    header_code = line
                    continue
                if width is None:
                    dim_str = line.split()
                    width = int(dim_str[0])
                    height = int(dim_str[1])
                    if width != 10 or height != 10:
                        return "Wrong dimensions"
                    continue
                if max_val is None:
                    max_val = int(line)
                    if max_val > 255:
                        return "Wrong colorset"
                    continue
                x = int(readed_lines / 3 / width)
                y = int((readed_lines / 3) % height)
                if len(icon) <= x:
                    icon.append([])
                if len(icon[x]) <= y:
                    icon[x].append([])
                icon[x][y].append(int(line))
                # print(icon[x][y])
                # icon[x][y] = reversed(icon[x][y])
                readed_lines += 1
            pic.close()
            return icon

        return "Wrong file type"
