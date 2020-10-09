from modules.Helpers import *
from modules.RenderingEngine import RenderingEngine



class GuiElement:


    def __init__(self, render_engine: RenderingEngine, x_0: int, y_0: int):
        self.render_engine = render_engine
        self.x_0 = x_0
        self.y_0 = y_0

    def loop(self, time_delta):
        pass

    def display(self):
        pass



class ScrollingText(GuiElement):


    def __init__(self, render_engine: RenderingEngine, x_0: int, y_0: int, width: int, text: str,
                 scroll_speed: float = 0.3, color: Color = Colors.WHITE):
        super().__init__(render_engine, x_0, y_0)
        self.width = width
        self.text = text
        self.color = color
        self.movement = 0
        self.position = 0
        self.scroll_speed = scroll_speed

    def loop(self, time_delta):
        self.movement += time_delta
        if self.movement > self.scroll_speed:
            self.movement = 0
            self.position = (self.position + 1) % (len(self.text) * 4)

    def display(self):
        self.render_engine.draw_text(self.x_0, self.y_0, self.text, self.color, self.width, self.position)


class InputText(GuiElement):

    def __init__(self, render_engine: RenderingEngine, x_0: int, y_0: int, width: int, color: Color = Colors.WHITE):
        super().__init__(render_engine, x_0, y_0)
        self.text = 'A' * width
        self.color = color
        self.cursor_position = 0
        self.cursor_blink = 0
        self.cursor_blink_speed = 1
        self.offset = 0

    def loop(self, time_delta):
        self.render_engine.draw_text(self.x_0, self.y_0, self.text[self.offset:self.offset+3], self.color)

    def input(self, action: Action):
        if action.type == ActionType.PRESSED:
            char_size = 7
            if action.pixels[0] < self.x_0:
                self.text = self.text[:-1]
                if self.offset > 0:
                    self.offset -= 1
            elif action.pixels[0] > self.render_engine.width - 2:
                self.text += 'A'
                self.offset += 1
            print("text {} offset {} -> {}".format(self.text, self.offset, self.text[self.offset:self.offset+3]))
            for letter_x in range(0, char_size*len(self.text), char_size):
                if action.pixels[0] >= self.x_0 + letter_x and action.pixels[0] < self.x_0 + letter_x  + char_size:
                    print("inc {} at {}".format(self.text[int(letter_x/char_size)], int(letter_x/char_size)))
                    text_list = list(self.text)
                    char_pos = self.offset + int(letter_x/char_size)
                    if action.pixels[1] < self.y_0:
                        text_list[char_pos] = chr(ord(text_list[char_pos]) + 1)
                    if action.pixels[1] > self.y_0 + char_size:
                        text_list[char_pos] = chr(ord(text_list[char_pos]) - 1)
                    self.text = "".join(text_list)

