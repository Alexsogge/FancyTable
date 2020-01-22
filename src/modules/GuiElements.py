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
