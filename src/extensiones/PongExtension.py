from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
from modules.GuiElements import ScrollingText
from modules.Geometry import *
import math
import random

tetromino_types = (((0, 0), (1, 0), (-1, 0), (2, 0)), ((0, 0), (0, -1), (1, 0), (1, 1)),
                   ((0, 0), (-1, 0), (0, 1), (0, -1)), ((0, 0), (-1, 0), (0, 1), (-1, 1)),
                   ((0, 0), (0, 1), (1, 0), (1, -1)), ((0, 0), (0, 1), (0, 2), (-1, 2)),
                   ((0, 0), (0, 1), (0, 2), (-1, 0)))
tetromino_colors = (Colors.GREEN, Colors.CYAN, Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.BLUE, Colors.PURPLE)

class Paddle:

    def __init__(self, render_engine: RenderingEngine):
        self.render_engine = render_engine
        self.pos: Vector = Vector(0, render_engine.height/2-2)
        self.size = Vector(1, 2)
        self.normal = Vector(1, 0)

    def draw(self):
        self.render_engine.draw_rectangle(int(self.pos.x), int(self.pos.y), int(self.pos.x),
                                          int(self.pos.y + self.size.y), Colors.WHITE)

    def check_collision(self, pos):
        # return self.pos <= pos <= self.pos + self.size
        b_x = int(pos.x)
        b_y = int(pos.y)
        p_x = int(self.pos.x)
        p_y = int(self.pos.y)

        return b_x == p_x and b_y >= p_y and b_y <= p_y + self.size.y

class Wall:

    def __init__(self, side, render_engine: RenderingEngine):
        self.border: int = 0
        self.normal: Vector = Vector(1, 0)
        self.side = side

        if side == 1:
            self.normal = Vector(0, 1)

        if side == 2:
            self.normal = Vector(-1, 0)
            self.border = render_engine.width

        if side == 3:
            self.normal = Vector(0, -1)
            self.border = render_engine.height - 1

    def check_collision(self, pos: Vector) -> bool:
        if self.side == 0:
            return pos.x < self.border
        if self.side == 1:
            return pos.y <= self.border
        if self.side == 2:
            return pos.x >= self.border
        else:
            return pos.y >= self.border


class Ball:

    def __init__(self, render_engine: RenderingEngine):
        self.render_engine = render_engine
        self.movement: Vector = Vector(1,0.2)
        self.movement.normalize()
        self.speed = 15

        self.pos: Vector = Vector(int(render_engine.width/2), 3)

        self.walls: List[Wall] = []
        self.walls.append(Wall(1, render_engine))
        self.walls.append(Wall(3, render_engine))



    def loop(self, time_delta):
        self.pos += self.movement * time_delta * self.speed
        self.check_bounce(time_delta)

    def draw(self):
        self.render_engine.draw_pixel(self.pos.round_x, self.pos.round_y, Colors.WHITE)

    def check_bounce(self, time_delta):
        for wall in self.walls:
            if wall.check_collision(self.pos):
                self.pos -= self.movement * time_delta * self.speed * 1.1
                self.movement.reflect_to(wall.normal)
                self.movement.normalize()






class PongExtension(Extension):


    def __init__(self):
        super().__init__()

        self.ball = Ball(self.render_engine)
        self.paddles = (Paddle(self.render_engine), Paddle(self.render_engine))
        self.paddles[1].pos.x = self.render_engine.width-1
        self.paddles[1].normal.x = -1
        self.scores = [0, 0]
        self.score_color = Colors.generate_color(Colors.WHITE)
        self.score_color.a = 0.3
        self.game_end = True
        self.player_ready = [False, False]
        self.player_released = [0, 0]

    def set_active(self):
        self.ball = Ball(self.render_engine)

    def process_input(self, action):
        if action.pixels[0] < self.render_engine.width / 2 - 1:
            if self.game_end and self.player_released[0] > 10:
                self.player_ready[0] = True
                if self.player_ready[1]:
                    self.start_round()
            self.paddles[0].pos.y = self.render_engine.height * action.y - 1
            self.player_released[0] = 0
        else:
            if self.game_end and self.player_released[1] > 10:
                self.player_ready[1] = True
                if self.player_ready[0]:
                    self.start_round()
            self.paddles[1].pos.y = self.render_engine.height * action.y - 1
            self.player_released[1] = 0


    def loop(self, time_delta: float):
        self.render_engine.clear_buffer()
        if self.game_end:
            self.player_released[0] += 1
            self.player_released[1] += 1
        else:
            self.ball.loop(time_delta)
            if self.ball.pos.x < 0:
                self.scores[1] += 1
                self.end_round()
            if self.ball.pos.x > self.render_engine.width:
                self.scores[0] += 1
                self.end_round()

            for paddle in self.paddles:
                if paddle.check_collision(self.ball.pos):
                    self.ball.movement.reflect_to(paddle.normal)


        self.ball.draw()
        self.paddles[0].draw()
        self.paddles[1].draw()

        self.render_engine.draw_text(0, -1, str(self.scores[0]), self.score_color, size=6)
        self.render_engine.draw_text(self.render_engine.width - len(str(self.scores[1])) * 4 + 1, -1, str(self.scores[1]), self.score_color, size=6)

    def start_round(self):
        self.game_end = False
        self.ball.pos.x = int(self.render_engine.width / 2)
        self.ball.pos.y = int(self.render_engine.height / 2 - 1)

    def end_round(self):
        self.game_end = True
        self.ball.pos.x = int(self.render_engine.width / 2)
        self.ball.pos.y = int(self.render_engine.height / 2 - 1)
        self.player_released = [0, 0]
        self.player_ready = [False, False]
