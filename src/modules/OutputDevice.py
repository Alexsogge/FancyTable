from typing import List, Dict, Tuple, Union
from .Framebuffer import Color


class OutputDevice:

    def __init__(self, width: int, height: int):
        self.size: List[int, int] = [width, height]
        self.brightness: float = 1


    @property
    def width(self) -> int:
        return self.size[0]

    @width.setter
    def width(self, width: int):
        self.size[0] = width

    @property
    def height(self) -> int:
        return self.size[1]

    @height.setter
    def height(self, height: int):
        self.size[1] = height

    def upload(self, frame_matrix: List[List[Color]]):
        pass

    def dimming(self, value: float):
        self.brightness += value

    def set_brightness(self, new_brightness: float):
        self.brightness = new_brightness
