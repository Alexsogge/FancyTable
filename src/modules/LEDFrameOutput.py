class LEDFrameOutput:

    width = 0
    height = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height



    def upload(self, frame_matrix):
        data = ()
        for y, row in enumerate(frame_matrix):
            for x, col in enumerate(row):

        self.stdscr.refresh()