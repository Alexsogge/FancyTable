from .Extension import Extension
from modules.TouchInput import ActionType
import time
import random


class WuerfelnExtension(Extension):
    current_milli_time = lambda: int(round(time.time() * 1000))
    color = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../../icons/wuerfeln.ppm")
        self.setup = True
        self.players = []
        self.roll = False
        self.roll_start = 0
        self.passed_cycles = 0
        w, h = self.frame_buffer.get_dimensions()
        self.dice_size = min(w*0.5, h*0.5)
        self.dice_pos = ((w / 2) - (self.dice_size / 2), (h / 2) - (self.dice_size / 2))
        self.eye_size = int(self.dice_size / 5)


    def process_input(self, slot, action):
        if self.setup:
            if action.type == ActionType.PRESSED:
                self.roll = True
                self.roll_start = self.current_milli_time()
                self.passed_cycles = 0



    def init_player(self, x, y):
        self.players.append((x,y))
        if len(self.players) == 5:
            self.start_game()


    def loop(self):
        if self.roll:
            if self.current_milli_time() > self.roll_start + 200:
                self.frame_buffer.draw_rect(self.dice_pos[0], self.dice_pos[1], self.dice_size, self.dice_size, 0, 0, 0)
                self.draw_dice(random.randint(1, 6))
                self.passed_cycles += 1
                if random.random() > 0.95:
                    self.roll = False
                else:
                    self.roll_start = self.current_milli_time()
                    self.passed_cycles = 0

    def draw_dice(self, num):
        if 1 >= num >= 6:
            mid_x = self.dice_pos[0] + self.dice_size / 2
            mid_y = self.dice_pos[1] + self.dice_size / 2
            if num == 1:
                self.draw_eye_on(4)
            if num == 2:
                self.draw_eye_on(6)
                self.draw_eye_on(2)
            if num == 3:
                self.draw_eye_on(6)
                self.draw_eye_on(4)
                self.draw_eye_on(2)
            if num == 4:
                self.draw_eye_on(0)
                self.draw_eye_on(2)
                self.draw_eye_on(6)
                self.draw_eye_on(8)
            if num == 5:
                self.draw_eye_on(0)
                self.draw_eye_on(2)
                self.draw_eye_on(4)
                self.draw_eye_on(6)
                self.draw_eye_on(8)
            if num == 6:
                self.draw_eye_on(0)
                self.draw_eye_on(2)
                self.draw_eye_on(3)
                self.draw_eye_on(5)
                self.draw_eye_on(6)
                self.draw_eye_on(8)


    def draw_eye_on(self, slot):
        if slot == 0:
            self.frame_buffer.draw_rect_col(self.dice_pos[0], self.dice_pos[1], self.eye_size, self.eye_size,
                                            self.color)
        if slot == 1:
            self.frame_buffer.draw_rect_col(self.dice_pos[0] + 2 * self.eye_size, self.dice_pos[1], self.eye_size,
                                            self.eye_size, self.color)
        if slot == 2:
            self.frame_buffer.draw_rect_col(self.dice_pos[0] + 4 * self.eye_size, self.dice_pos[1], self.eye_size,
                                            self.eye_size, self.color)
        if slot == 3:
            self.frame_buffer.draw_rect_col(self.dice_pos[0], self.dice_pos[1] + 2 * self.eye_size , self.eye_size,
                                            self.eye_size, self.color)
        if slot == 4:
            self.frame_buffer.draw_rect_col(self.dice_pos[0]+ 2 * self.eye_size, self.dice_pos[1] + 2 * self.eye_size,
                                            self.eye_size, self.eye_size, self.color)
        if slot == 5:
            self.frame_buffer.draw_rect_col(self.dice_pos[0]+ 4 * self.eye_size, self.dice_pos[1] + 2 * self.eye_size,
                                            self.eye_size, self.eye_size, self.color)
        if slot == 6:
            self.frame_buffer.draw_rect_col(self.dice_pos[0], self.dice_pos[1] + 4 * self.eye_size , self.eye_size,
                                            self.eye_size, self.color)
        if slot == 7:
            self.frame_buffer.draw_rect_col(self.dice_pos[0]+ 2 * self.eye_size, self.dice_pos[1] + 4 * self.eye_size,
                                            self.eye_size, self.eye_size, self.color)
        if slot == 8:
            self.frame_buffer.draw_rect_col(self.dice_pos[0]+ 4 * self.eye_size, self.dice_pos[1] + 4 * self.eye_size,
                                            self.eye_size, self.eye_size, self.color)


    def start_game(self):
        self.setup = True




