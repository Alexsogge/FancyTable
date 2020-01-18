from .OutputDevice import OutputDevice
from typing import List, Dict, Tuple, Union
import graphics
from tkinter import Tk, Canvas, PhotoImage, mainloop
from .Helpers import Color, Colors
import PySimpleGUI as sg


class OutputEmulation(OutputDevice):

    def __init__(self, width: int, height: int, pixel_size):
        super().__init__(width*pixel_size, height*pixel_size)
        # self.win = graphics.GraphWin('OutputEmulation', width * pixel_size, height*pixel_size)
        sg.theme('DarkBlue1')

        layout = [
            [sg.Graph(canvas_size=(width*pixel_size, height*pixel_size), graph_bottom_left=(0, 0),
                      graph_top_right=(width*pixel_size, height*pixel_size),
                      background_color='black', key='graph', enable_events=True, drag_submits=True)],
        ]
        self.window = sg.Window('Window Title', layout)
        self.window.Finalize()
        self.graph = self.window['graph']
        self.pixel_size = pixel_size
        self.debug = False
        self.old_buffer: List[List[Color]] = None


    def upload(self, frame_matrix: List[List[Color]]):
        if self.old_buffer is None:
            self.old_buffer = []
            for y, row in enumerate(frame_matrix):
                self.old_buffer.append([])
                for x, color in enumerate(row):
                    self.old_buffer[-1].append(Color())
                    self.old_buffer[-1][-1].set_color(Colors.WHITE)
        if self.debug:
            print('########################################################')
        for y, row in enumerate(frame_matrix):
            i = y * self.pixel_size
            i = self.height - i - self.pixel_size
            line = ""
            for x, color in enumerate(row):
                if self.old_buffer[y][x] == color:
                    continue
                    pass
                else:
                    self.old_buffer[y][x].set_color(color)
                j = x * self.pixel_size
                self.graph.DrawRectangle((j, i), (j + self.pixel_size, i + self.pixel_size), line_color='black',
                                         fill_color=color.rgb_string)
                #rect = graphics.Rectangle(graphics.Point(j, i), graphics.Point(j+self.pixel_size, i+self.pixel_size))
                #rect.setFill(graphics.color_rgb(color.r, color.g, color.b))
                #rect.draw(self.win)
                line += str(color) + " "

            self.window.finalize()
            if self.debug:
                print(line)

