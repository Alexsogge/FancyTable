from random import randint
from typing import List, Dict, Tuple, Union
import math
import enum
import colorsys
import random

class Color:

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: float = 1):
        self.color: List[int, int, int, float] = [r, g, b, a]

    def __repr__(self) -> Dict[str, int]:
        return {'r': self.color[0], 'g': self.color[1], 'b': self.color[2], 'a': self.color[3]}

    def __str__(self):
        return "({}, {}, {})".format(self.color[0], self.color[1], self.color[2])

    def __eq__(self, other: 'Color'):
        return self.r == other.r and self.g == other.g and self.b == other.b

    @property
    def r(self) -> int:
        return self.color[0]

    @r.setter
    def r(self, r: int):
        if r < 0:
            r = 0
        if r > 255:
            r = 255
        self.color[0] = r

    @property
    def g(self) -> int:
        return self.color[1]

    @g.setter
    def g(self, g: int):
        if g < 0:
            g = 0
        if g > 255:
            g = 255
        self.color[1] = g

    @property
    def b(self) -> int:
        return self.color[2]

    @b.setter
    def b(self, b: int):
        if b < 0:
            b = 0
        if b > 255:
            b = 255
        self.color[2] = b

    @property
    def a(self) -> float:
        return self.color[3]

    @a.setter
    def a(self, a: float):
        if a < 0:
            a = 0
        if a > 1:
            a = 1
        self.color[3] = a

    @property
    def rgb(self) -> List[int]:
        return self.color[:-1]

    @rgb.setter
    def rgb(self, new_rgb: List[int]):
        self.r = new_rgb[0]
        self.g = new_rgb[1]
        self.b = new_rgb[2]

    def set_color(self, color: 'Color'):
        self.rgb = color.rgb

    @property
    def rgb_string(self) -> str:
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)


class Colors:
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    YELLOW = Color(255, 255, 0)
    ORANGE = Color(255, 165, 0)
    CYAN = Color(0, 255, 255)
    PURPLE = Color(128, 0, 128)

    @classmethod
    def generate_color(cls, color: Color) -> Color:
        return Color(color.r, color.g, color.b, color.a)

    @classmethod
    def generate_random(cls) -> Color:
        r, g, b = colorsys.hsv_to_rgb(random.random(), 1, 1)
        R, G, B = int(255 * r), int(255 * g), int(255 * b)
        return Color(R, G, B)

    @classmethod
    def generate_from_pallete(cls, pos: int):
        color_length = 5000
        r, g, b = colorsys.hsv_to_rgb((pos % color_length) / color_length, 1, 1)
        R, G, B = int(255 * r), int(255 * g), int(255 * b)
        return Color(R, G, B)



class FramePixel:

    def __init__(self, r: int=0, g: int=0, b: int=0, a: float=1):
        self.color: Color = Color(r, g, b, a)

    def __str__(self):
        return "({}, {}, {})".format(self.color.r, self.color.g, self.color.b)

    def set_rgb(self, r, g, b):
        self.color.r = r
        self.color.g = g
        self.color.b = b

    def set_rgba(self, r, g, b, a):
        self.color.r = r
        self.color.g = g
        self.color.b = b
        self.color.a = a

    def set_color(self, color: Color):
        self.set_rgb(color.r, color.g, color.b)

    def set_color_rgba(self, color: Color):
        self.set_rgba(color.r, color.g, color.b, color.a)

    def shift_to_color(self, shift_value: float, color: Color):
        to_color = Color(color.r - self.color.r, color.g - self.color.g, color.b - self.color.b)
        sqdist = to_color.r ** 2 + to_color.g ** 2 + to_color.b ** 2

        if sqdist <= shift_value ** 2:
            self.color.rgb = color.rgb
        else:
            dist = math.sqrt(sqdist)
            self.color.r += int((to_color.r / dist) * shift_value)
            self.color.g += int((to_color.g / dist) * shift_value)
            self.color.b += int((to_color.b / dist) * shift_value)

class FrameBuffer:

    def __init__(self, width: int, height: int, init_random=False):
        self.size: List[int, int] = [width, height]
        self.buffer: List[List[FramePixel]] = []

        for i in range(height):
            self.buffer.append([])
            for j in range(width):
                init_color = Color()
                if init_random:
                    init_color.r = randint(0, 255)
                    init_color.g = randint(0, 255)
                    init_color.b = randint(0, 255)
                self.buffer[-1].append(FramePixel(init_color.r, init_color.g, init_color.b))

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    def get_dimensions(self) -> Tuple[int]:
        return self.size

    def clear(self, background_color: Color = Colors.BLACK):
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                self.buffer[i][j].set_rgb(background_color.r, background_color.g, background_color.b)

    def shift(self, shift_value: float, color: Color = Colors.BLACK):
        if color is None:
            color = Color()

        for i in range(self.size[1]):
            for j in range(self.size[0]):
                self.buffer[i][j].shift_to_color(shift_value, color)

    def set_pixel_color(self, x: int, y: int, color: Color):
        if x < self.width and y < self.height:
            self.buffer[int(y)][int(x)].set_color(color)

    def set_pixel_rgb(self, x: int, y: int, r: int, g: int, b: int):
        self.set_pixel_color(x, y, Color(r, g, b))

    def get_pixel(self, x: int, y:int) -> FramePixel:
        return self.buffer[y][x]

    def get_pixel_color(self, x: int, y: int) -> Color:
        return self.buffer[y][x].color

    def get_color_buffer(self) -> List[List[Color]]:
        color_buffer: List[List[Color]] = []
        for row in self.buffer:
            color_buffer.append([])
            for pixel in row:
                color_buffer[-1].append(pixel.color)

        return color_buffer


class ActionType(enum.Enum):
    PRESSED = 1
    RELEASED = 2
    MOVED = 3


class Action:

    def __init__(self, x, y, atype: ActionType, z=0):
        """
        Action event
        :param x: [0,1]
        :param y: [0,1]
        :param atype:
        """
        self.x = x % 1
        self.y = y % 1
        self.z = z
        self.type = atype
        self.pixels = (x, y)

    def __str__(self):
        return "Action " + str(self.type) + " on " + str(self.x) + " | "+ str(self.y) + " -> "+ str(self.pixels)

    def add_pixels(self, pixels: List[int]):
        """
        :rtype: (x, y) on screen space
        """
        self.pixels = pixels


class Input:

    def __init__(self, x: float=None, y: float=None, z: int=0):
        self.pos: List[Union[float, int]] = [x, y, z]
        self.actions: List[Action] = list()

    @property
    def x(self) -> float:
        return self.pos[0]

    @property
    def y(self) -> float:
        return self.pos[1]

    @property
    def z(self) -> int:
        return self.pos[2]

    @x.setter
    def x(self, x: float):
        self.pos[0] = x

    @y.setter
    def y(self, y: float):
        self.pos[1] = y

    @z.setter
    def z(self, z: int):
        self.pos[2] = z

    def set_pixels(self, render_engine):
        for action in self.actions:
            action.add_pixels(render_engine.map_input(action.x, action.y))

    def press(self):
        self.actions.append(Action(self.x, self.y, ActionType.PRESSED, self.z))

    def release(self):
        self.actions.append(Action(self.x, self.y, ActionType.RELEASED, self.z))

    def move(self, x: float=None, y:float=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        # Update Previous Actions
        for action in reversed(self.actions):
            if action.type == ActionType.MOVED:
                break
            if action.x is None:
                action.x = self.x
            if action.y is None:
                action.y = self.y
        self.actions.append(Action(self.x, self.y, ActionType.MOVED, self.z))

    def clear(self):
        self.actions = []

    def __str__(self):
        return "Input at {}|{} with {} actions.".format(self.x, self.y, len(self.actions))
