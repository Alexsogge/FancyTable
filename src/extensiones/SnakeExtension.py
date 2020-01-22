from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
from modules.GuiElements import ScrollingText
from modules.Geometry import *
import math
import random


class SnakeElement:

    def __init__(self, x, y, render_engine: RenderingEngine):
        self.pos: Vector = Vector(x, y)
        self.render_engine = render_engine
        self.color = Colors.GREEN

    def draw(self):
        self.render_engine.draw_pixel(self.pos.x, self.pos.y, self.color)


class NewElement:

    def __init__(self, render_engine: RenderingEngine):
        self.render_engine = render_engine
        self.pos: Vector = Vector(random.randint(0, render_engine.width - 1),
                                  random.randint(0, render_engine.height - 1))

    def draw(self):
        self.render_engine.draw_pixel(self.pos.x, self.pos.y, Colors.WHITE)


class SnakeExtension(Extension):

    def __init__(self):
        self.default_config = {'border': False}
        super().__init__()
        self.icon_pic = self.read_icon("../icons/snake.ppm")

        self.control_colors: List[Color] = [Colors.generate_color(Colors.RED), Colors.generate_color(Colors.GREEN),
                                            Colors.generate_color(Colors.BLUE), Colors.generate_color(Colors.YELLOW)]
        for color in self.control_colors:
            color.a = 0.15

        self.snake_elements: List[SnakeElement] = []
        self.speed = 3
        self.step = 0
        self.direction: Vector = Vector(1, 0)
        self.border = self.config['border'] == 'True'
        self.new_element: NewElement = NewElement(self.render_engine)
        self.gameover = False
        self.gameover_text: Union[None, ScrollingText] = None
        self.moved_tile = True

    def set_active(self):
        self.snake_elements: List[SnakeElement] = [SnakeElement(10, 5, self.render_engine),
                                                   SnakeElement(9, 5, self.render_engine),
                                                   SnakeElement(8, 5, self.render_engine)]
        self.snake_elements[0].color = Colors.RED
        self.step = 0
        self.direction: Vector = Vector(1, 0)
        self.new_element: NewElement = NewElement(self.render_engine)
        self.gameover = False

    def process_input(self, action):
        if self.moved_tile:
            if action.x < 0.25:
                if self.direction.x == 0:
                    self.direction = Vector(-1, 0)
                    self.moved_tile = False
            elif action.x > 0.75:
                if self.direction.x == 0:
                    self.direction = Vector(1, 0)
                    self.moved_tile = False
            else:
                if action.y < 0.5:
                    if self.direction.y == 0:
                        self.direction = Vector(0, -1)
                        self.moved_tile = False
                else:
                    if self.direction.y == 0:
                        self.direction = Vector(0, 1)
                        self.moved_tile = False

    def loop(self, time_delta: float):
        self.render_engine.clear_buffer()

        if not self.gameover:
            self.step += time_delta * self.speed
            if self.step >= 1:
                self.step = 0
                self.moved_tile = True
                for i in range(len(self.snake_elements) - 1, 0, -1):
                    self.snake_elements[i].pos = self.snake_elements[i - 1].pos
                self.snake_elements[0].pos += self.direction
                if self.border == False:
                    self.snake_elements[0].pos.x %= self.render_engine.width
                    self.snake_elements[0].pos.y %= self.render_engine.height

            # print(self.snake_elements[-1].pos, " == ", self.new_element.pos)
            if self.snake_elements[-1].pos == self.new_element.pos:
                print("match")
                self.snake_elements.append(
                    SnakeElement(self.new_element.pos.x, self.new_element.pos.y, self.render_engine))
                self.new_element = NewElement(self.render_engine)
            for tile in self.snake_elements[1:]:
                if self.snake_elements[0].pos == tile.pos:
                    self.game_over()

        head_pos = self.snake_elements[0].pos
        if head_pos.x < 0 or head_pos.x >= self.render_engine.width or head_pos.y < 0 or \
                head_pos.y >= self.render_engine.height:
            if not self.gameover:
                self.game_over()

        self.draw()
        if self.gameover:
            self.gameover_text.loop(time_delta)
            self.gameover_text.display()

    def game_over(self):
        self.gameover = True

        self.gameover_text = ScrollingText(self.render_engine, 2, 2, self.render_engine.width - 4,
                                           "Game over: " + str(len(self.snake_elements)))

    def draw(self):
        self.render_engine.draw_rectangle(0, 0, int(self.render_engine.width * 0.25), self.render_engine.height,
                                          self.control_colors[0])
        self.render_engine.draw_rectangle(int(self.render_engine.width * 0.25) + 1, 0,
                                          int(self.render_engine.width * 0.75) - 1,
                                          int(self.render_engine.height / 2) - 1,
                                          self.control_colors[1])
        self.render_engine.draw_rectangle(int(self.render_engine.width * 0.75), 0, self.render_engine.width,
                                          self.render_engine.height,
                                          self.control_colors[2])
        self.render_engine.draw_rectangle(int(self.render_engine.width * 0.25) + 1, int(self.render_engine.height / 2),
                                          int(self.render_engine.width * 0.75) - 1, self.render_engine.height,
                                          self.control_colors[3])
        for snake_element in self.snake_elements:
            snake_element.draw()

        self.new_element.draw()
