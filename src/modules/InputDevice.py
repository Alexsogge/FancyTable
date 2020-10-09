from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple, Union
from .RenderingEngine import RenderingEngine
from .Helpers import *


class InputDevice:

    def __init__(self, width=0, height=0):
        self.width: int = width
        self.height: int = height
        self.dimensions: List[int, int] = [self.width, self.height]

        self.inputs: Dict[int, Input] = dict()

    def setup(self, width, height):
        self.width = width
        self.height = height
        self.dimensions = [self.width, self.height]

    @abstractmethod
    def read_inputs(self):
        raise NotImplementedError

    def get_inputs(self) -> Dict[int, Input]:
        return self.inputs

    def clear_inputs(self, slot):
        self.inputs.pop(slot)

    def u(self, x) -> float:
        if x is None:
            return None
        return x / self.width

    def v(self, y) -> float:
        if y is None:
            return None
        return y / self.height

    def new_input(self, x, y, z):
        input = Input(self.u(x), self.v(y), z)
        self.inputs[z] = input

    def map_inputs_to_screen(self, render_engine: RenderingEngine):
        for input in self.inputs.values():
            input.set_pixels(render_engine)



