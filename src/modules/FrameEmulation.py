import curses


class EmulatedOutput:

    window = None

    width = 0
    height = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

        curses.start_color()
        curses.use_default_colors()

        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        self.window = curses.newwin(height, width*2, 0, 0)
        self.window.bkgd(curses.color_pair(2))
        self.window.box()

    def upload(self, frame_matrix):
        for y, row in enumerate(frame_matrix):
            for x, col in enumerate(row):
                self.stdscr.addstr(y, x*2, '██', curses.color_pair(int(col['r'])))
        self.stdscr.refresh()


