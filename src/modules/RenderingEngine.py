from random import randint
from typing import List, Dict, Tuple, Union
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from .Helpers import *
from .OutputDevice import OutputDevice


class RenderingEngine:

    frame_matrix = []

    colors = ['r', 'g', 'b']

    frame_outputs = []


    def __init__(self, width: int, height: int, output: OutputDevice=None, init_random=False):
        """
        Initiaize the Engine
        :param width: number of pixels per row
        :param height: number of pixelrows
        :param output: outputdevice
        :param init_random: start with random colored
        """
        self.tails = False
        self.tail_value = 1
        self.output_devices: List[OutputDevice] = []

        self.frame_buffer = FrameBuffer(width, height, init_random)
        if output is not None:
            self.output_devices.append(output)


    @property
    def width(self) -> int:
        return self.frame_buffer.width

    @property
    def height(self) -> int:
        return self.frame_buffer.height

    def set_tales(self, tail, val=1):
        """
        If tails is enabled pixels glow out by clean
        :param tail: Sets tailmode
        :param val: the value which the colors will be decreased
        """
        self.tails = tail
        if tail:
            self.tail_value = val

    def add_output(self, output):
        """
        Add an new
        :rtype: object
        """
        self.frame_outputs.append(output)

    def get_dimensions(self):
        """
        Returns the width and height of the frame matrix
        :return: (width, height)
        """
        return self.frame_buffer.width, self.frame_buffer.height


    def clear_buffer(self):
        """
        Clears the Frame. If tails is enabled the pixels will glow out
        """
        if self.tails:
            self.frame_buffer.shift(self.tail_value, Colors.BLACK)
        else:
            self.frame_buffer.clear()

    def flush_buffer(self, color: Color):
        self.frame_buffer.clear(color)

    def set_pixel_color(self, x, y, color: Color):
        self.set_pixel_rgb(x, y, color.r, color.g, color.b, color.a)


    def set_pixel_rgb(self, x, y, r: int, g: int, b: int, a: float = 1.0):
        """
        Sets the color of an specific pixel
        :param x: column
        :param y: row
        :param r: red value
        :param g: green value
        :param b: blue value
        """
        x = int(x)
        y = int(y)
        if y < 0 or y >= self.frame_buffer.height:
            return
        if x < 0 or x >= self.frame_buffer.width:
            return

        if a < 1:
            r = a * r + (1 - a) * self.frame_buffer.get_pixel_color(x, y).r
            g = a * g + (1 - a) * self.frame_buffer.get_pixel_color(x, y).g
            b = a * b + (1 - a) * self.frame_buffer.get_pixel_color(x, y).b

        self.frame_buffer.set_pixel_rgb(x, y, r, g, b)


    def draw_pixel(self, x_0, y_0, color: Color):
        self.set_pixel_color(x_0, y_0, color)

    def draw_line(self, x_1, y_1, x_2, y_2, color: Color):
        """
        Bresenham’s algorithm
        :param x_1:
        :param y_1:
        :param x_2:
        :param y_2:
        :param color:
        :return:
        """
        def swap(a, b):
            return b, a

        steep = abs(y_2 - y_1) > abs(x_2 - x_1)
        if steep:
            x_1, y_1 = swap(x_1, y_1)
            x_2, y_2 = swap(x_2, y_2)
        if x_1 > x_2:
            x_1, x_2 = swap(x_1, x_2)
            y_1, y_2 = swap(y_1, y_2)

        delta_x = abs(x_2 - x_1)
        delta_y = abs(y_2 - y_1)
        error = 0
        y_step = 1
        y = y_1
        if y_1 >= y_2:
            y_step = -1

        for x in range(int(x_1), int(x_2)):
            if steep:
                self.set_pixel_color(round(y), round(x), color)
            else:
                self.set_pixel_color(round(x), round(y), color)
            error += abs(delta_y)
            if 2 * error >= delta_x:
                y += y_step
                error -= delta_x




#         k = (y_2 - y_1) / (x_2 - x_1)
#         print(k)
#         loop_counter = x_1
#         incrementor = y_1
#         stop = x_2
#         if k > 1:
#             loop_counter = y_1
#             incrementor = x_1
#             stop = y_2
#
#         while loop_counter <= stop:
#             if k <= 1:
#                 self.set_pixel_color(loop_counter, round(incrementor), color)
#             else:
#                 self.set_pixel_color(round(incrementor), loop_counter, color)
#             incrementor += k
#             loop_counter += 1
#


    def draw_rectangle(self, x_1, y_1, x_2, y_2, color: Color, fill=True):
        """
        Draws an rectangle on the given left upper point x_1, y_2 and left lower point x_2, y_2
        :param x_1: x of left upper point
        :param y_1: y of left upper point
        :param x_1: x of right lower point
        :param y_1: y of right lower point
        :param color: The color of rect
        :param fill: fill out rectangle (Default: True)
        """
        def swap(a, b):
            return b, a

        if x_2 < x_1:
            x_1, x_2 = swap(x_1, x_2)
        if y_2 < y_1:
            y_1, y_2 = swap(y_1, y_2)
        for x in range(int(x_1), int(x_2) + 1):
            for y in range(int(y_1), int(y_2) + 1):
                if fill or (x == x_1 or y == y_1 or x == x_2 or y == y_2):
                    self.set_pixel_color(x, y, color)

    def draw_rectangle_wh(self, x_1, y_1, width, height, color: Color, fill=True):
        self.draw_rectangle(x_1, y_1, x_1 + width, y_1 + height, color, fill)

    def draw_circle(self, x_0, y_0, r, color: Color, fill=False):
        def symetry_dots(x, y):
            self.frame_buffer.set_pixel_color(x + x_0, y + y_0, color)
            self.frame_buffer.set_pixel_color(-x + x_0, y + y_0, color)
            self.frame_buffer.set_pixel_color(x + x_0, -y + y_0, color)
            self.frame_buffer.set_pixel_color(-x + x_0, -y + y_0, color)
            self.frame_buffer.set_pixel_color(y + x_0, x + y_0, color)
            self.frame_buffer.set_pixel_color(-y + x_0, x + y_0, color)
            self.frame_buffer.set_pixel_color(y + x_0, -x + y_0, color)
            self.frame_buffer.set_pixel_color(-y + x_0, -x + y_0, color)


        theta = 0
        if r == 0:
            r = 0.001
        step = math.radians(15/r)

        while theta <= math.radians(360) + step:
            x = x_0 + r * math.cos(theta)
            y = y_0 + r * math.sin(theta)
            if fill:
                self.draw_line(x_0, y_0, round(x), round(y), color)
                # print("{}->{}, {}->{}".format(x_0, x, y_0, y))
            if x > 0 and y > 0:
                self.frame_buffer.set_pixel_color(round(x), round(y), color)
            theta += step

#         d = -r
#         x = r
#         y = 0
#         while y <= x:
#             symetry_dots(x, y)
#             d = d + 2 * y + 1
#             y = y + 1
#             if d > 0:
#                 d = d - 2 * x + 2
#                 x = x - 1

    def draw_text(self, x_0: int, y_0: int, text: str, color: Color = Colors.WHITE,  width: int = math.inf, offset: int = 0, size: int = 8):
        myfont = ImageFont.truetype("./small_pixel.ttf", size)
        size = myfont.getsize(text)
        img = Image.new("1", size, "black")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, "white", font=myfont)
        pixels = np.array(img, dtype=np.uint8)
        chars = np.array([' ', '#'], dtype="U1")[pixels]
        strings = chars.view('U' + str(chars.shape[1])).flatten()
        #print("\n".join(strings))
        for y, row in enumerate(pixels):
            for x, pixel in enumerate(row):
                if pixel == 1 and x > offset-1 and (x - offset - 1) < width:
                    self.draw_pixel(x_0 + x - offset, y_0 + y, color)
        #print(pixels)

    def draw_row(self, row: int, color: Color):
        self.draw_line(0, row, self.frame_buffer.width, row)

    def draw_column(self, column: int, color: Color):
        self.draw_line(column, 0, column, self.frame_buffer.height, color)

    def get_matrix(self):
        """
        Returns the frame matrix
        :return: list of lists for each row. Lists contain dictionaries with 'r', 'g', 'b' values
        """
        return self.frame_matrix

    def get_pixel(self, x, y) -> FramePixel:
        """
        Returns the color of an specific pixel
        :param x: column
        :param y: row
        :return: Pixel
        """
        return self.frame_buffer.get_pixel(x, y)

    def get_pixel_color(self, x, y) -> Color:
        """
        Returns the color of an specific pixel
        :param x: column
        :param y: row
        :return: Color at pixel
        """
        return self.frame_buffer.get_pixel(x, y).color

    def get_matrix_row(self, row) -> Union[None, List[Color]]:
        """
        Returns the color of an entire row
        :param row: the row which should be returned
        """
        if self.frame_buffer.height > row:
            return [pixel.color for pixel in self.frame_buffer.buffer[row]]
        return None

    def get_matrix_column(self, col) -> Union[None, List[Color]]:
        """
        Returns the color of an entire column
        :param col: the column which should be returned
        """
        if self.frame_buffer.width > col:
            column: List[Color] = []
            for row in self.frame_buffer.buffer:
                column.append(row[col].color)
            return column
        return None

    def inc_diming(self, val):
        for output_device in self.output_devices:
            output_device.dimming(val)

    def upload_buffer(self):
        for output_device in self.output_devices:
            output_device.upload(self.frame_buffer.get_color_buffer())

    def map_input(self, x, y):
        return int(x * self.frame_buffer.width), int(y * self.frame_buffer.height)
