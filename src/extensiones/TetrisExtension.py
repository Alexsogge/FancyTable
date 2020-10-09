from .Extension import Extension
from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine
from modules.GuiElements import ScrollingText
import math

tetromino_types = (((0, 0), (1, 0), (-1, 0), (2, 0)), ((0, 0), (0, -1), (1, 0), (1, 1)),
                   ((0, 0), (-1, 0), (0, 1), (0, -1)), ((0, 0), (-1, 0), (0, 1), (-1, 1)),
                   ((0, 0), (0, 1), (1, 0), (1, -1)), ((0, 0), (0, 1), (0, 2), (-1, 2)),
                   ((0, 0), (0, 1), (0, 2), (-1, 0)))
tetromino_colors = (Colors.GREEN, Colors.CYAN, Colors.RED, Colors.YELLOW, Colors.ORANGE, Colors.BLUE, Colors.PURPLE)

class Tetromino:


    def __init__(self, tetr_type, falling_speed, render_engine: RenderingEngine):
        self.x_0 = 0
        self.y_0 = 7
        self.render_engine = render_engine
        self.falling_speed = falling_speed
        self.pieces: List[List[int]] = list()
        self.color = Colors.generate_color(tetromino_colors[tetr_type])
        for piece in tetromino_types[tetr_type]:
            self.pieces.append([piece[0], piece[1]])
        # self.rotate_tetromino()


    def loop(self, time_delta):
        self.x_0 += time_delta * self.falling_speed

    def draw(self):
        for piece in self.pieces:
            self.render_engine.draw_pixel(int(self.x_0) + piece[0], self.y_0 + piece[1], self.color)

    def rotate(self, x, y):
        rad = math.radians(90)

        k = round(math.cos(rad) * x + -math.sin(rad) * y)
        n = round(math.sin(rad) * x + math.cos(rad) * y)
        return k, n

    def rotate_pieces(self, rad):
        for i in range(len(self.pieces)):
            piece = self.pieces[i]
            self.pieces[i] = self.rotate(piece[0], piece[1])

    def rotate_tetromino(self, other_tetrominos: List['Tetromino']):
        rad = math.radians(90)
        self.rotate_pieces(rad)
        for other_tetromino in other_tetrominos:
            if other_tetromino.check_colission(self):
                rad = math.radians(-90)
                #self.rotate_pieces(rad)
                return

        while True:
            moved = False
            for piece in self.pieces:
                if self.y_0 + piece[1] < 2:
                    moved = True
                    self.move_left()
            for piece in self.pieces:
                if self.y_0 + piece[1] > self.render_engine.get_dimensions()[1] - 1:
                    moved = True
                    self.move_right()
            if not moved:
                break

    def move_right(self):
        for piece in self.pieces:
            if self.y_0 + piece[1] < 3:
                return
        self.y_0 -= 1

    def move_left(self):
        for piece in self.pieces:
            if self.y_0 + piece[1] >= self.render_engine.get_dimensions()[1]-1:
                return
        self.y_0 += 1

    def check_colission(self, other: 'Tetromino'):
        for my_piece in self.pieces:
            if int(self.x_0) + my_piece[0] >= self.render_engine.get_dimensions()[0] - 1:
                return True
            if self == other:
                continue

            for other_piece in other.pieces:
                x_m = int(self.x_0) + my_piece[0] + 1
                x_o = int(other.x_0) + other_piece[0]

                y_m = int(self.y_0) + my_piece[1]
                y_o = int(other.y_0) + other_piece[1]
                if x_m == x_o and y_m == y_o:
                    return True

        return False





class TetrisExtension(Extension):


    def __init__(self):
        super().__init__()
        self.falling_speed = 3
        self.tetrominos: List[Tetromino] = list()
        self.game_over = False
        self.game_over_screen = None
        self.ui_left_color: Color = Color(255, 0, 120, 0.04)
        self.ui_right_color: Color = Color(120, 255, 0, 0.04)
        self.ui_drop_color: Color = Color(0, 120, 255, 0.04)
        self.ui_border_color: Color = Colors.generate_color(Colors.WHITE)
        self.ui_border_color.a = 0.04
        self.score = 0
        self.icon_pic = self.read_icon("../icons/tetris.ppm")


    def set_active(self):
        self.tetrominos: List[Tetromino] = []
        self.tetrominos.append(Tetromino(random.randint(0, 6), self.falling_speed, self.render_engine))
        self.game_over = False
        self.game_over_text: ScrollingText = None

    def process_input(self, action):
        if action.type == ActionType.PRESSED:
            if action.pixels[0] < self.render_engine.width - 3:
                self.tetrominos[-1].rotate_tetromino(self.tetrominos)
            elif action.pixels[1] < 4:
                self.tetrominos[-1].move_right()
                if self.check_colission(self.tetrominos[-1]):
                    self.tetrominos[-1].move_left()
            elif action.pixels[1] >= 8:
                self.tetrominos[-1].move_left()
                if self.check_colission(self.tetrominos[-1]):
                    self.tetrominos[-1].move_right()
            else:
                while not self.check_colission(self.tetrominos[-1]):
                    self.tetrominos[-1].x_0 += 0.2

    def loop(self, time_delta: float):
        self.render_engine.clear_buffer()
        if not self.game_over:
            self.render_engine.clear_buffer()
            self.tetrominos[-1].loop(time_delta)
            for tetromino in self.tetrominos:
                if self.tetrominos[-1].check_colission(tetromino):
                    self.score += self.check_line_complete()
                    self.tetrominos.append(Tetromino(random.randint(0, 6), self.falling_speed, self.render_engine))
                    print("check for game over")
                    if self.check_colission(self.tetrominos[-1]):
                        self.game_over = True
                        for tetromino in self.tetrominos:
                            tetromino.color.a = 0.3
                        print("game over")
                        self.game_over_text = ScrollingText(self.render_engine, 2, 2, 17, "Game over: {}".format(self.score), 0.15)
                        break
        for tetromino in self.tetrominos:
            tetromino.draw()


        self.render_engine.draw_rectangle(self.render_engine.width-3, 0, self.render_engine.width, 3, self.ui_right_color)
        self.render_engine.draw_rectangle(self.render_engine.width - 3, 4, self.render_engine.width, 7,
                                          self.ui_drop_color)
        self.render_engine.draw_rectangle(self.render_engine.width - 3, 8, self.render_engine.width, 11,
                                          self.ui_left_color)
        self.render_engine.draw_rectangle(0, 0, self.render_engine.width, 1,
                                          self.ui_border_color)

        if self.game_over:
            self.game_over_text.loop(time_delta)
            self.game_over_text.display()

    def check_colission(self, chack_tetromino: Tetromino):
        for tetromino in self.tetrominos:
            if self.tetrominos[-1].check_colission(tetromino):
                return True
        return False

    def check_line_complete(self, combo=0):
        for column in range(self.render_engine.width + 1):
            cells = 0
            for tetromino in self.tetrominos:
                for piece in tetromino.pieces:
                    if piece[0] + int(tetromino.x_0) == column:
                        cells += 1
            print(cells)
            if cells == self.render_engine.height-2:
                for tetromino in self.tetrominos[:]:
                    removed_piece = False
                    for piece in tetromino.pieces[:]:
                        if piece[0] + int(tetromino.x_0) == column:
                            removed_piece = True
                            tetromino.pieces.remove(piece)
                            if len(tetromino.pieces) == 0:
                                self.tetrominos.remove(tetromino)
                    if removed_piece:
                        tetromino.x_0 += 1
                return self.check_line_complete(combo*2)
        return combo
