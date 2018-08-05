from abc import ABC, abstractmethod
from modules import Framebuffer



class Extension(ABC):
    frame_buffer = None

    def __init__(self):
        """
        Initialize an empty default extension
        """
        self.icon_x = None
        self.icon_y = None
        self.icon_width = 10
        self.icon_height = 10
        self.icon_pic = self.read_icon("../icons/nonpic.ppm")

    @staticmethod
    def set_global_frame_buffer(buffer: Framebuffer.Frame):
        """
        Sets the frame buffer for all extensions
        :param buffer:
        """
        global frame_buffer
        frame_buffer = buffer

    @property
    def framebuffer(self) -> Framebuffer.Frame:
        """
        returns the global frame buffer
        :rtype: Framebuffer
        """
        global frame_buffer
        return frame_buffer

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
        print(self.icon_x, "<=", x, "<=", self.icon_x + self.icon_width, "and", self.icon_y, "<", y, "<", self.icon_y + self.icon_height)
        return self.icon_x <= x <= self.icon_x + self.icon_width and \
                self.icon_y < y < self.icon_y + self.icon_height

    @abstractmethod
    def set_active(self):
        pass

    @abstractmethod
    def process_input(self, slot, action):
        pass

    @abstractmethod
    def loop(self):
        pass

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
