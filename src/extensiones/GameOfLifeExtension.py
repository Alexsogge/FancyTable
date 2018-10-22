from .Extension import Extension
from modules.TouchInput import ActionType
import random
import colorsys

import time

current_milli_time = lambda: int(round(time.time() * 1000))

class CellElement:
    """
    Every CellElement knows
        - its position as tuple, working as ID
        - if its alive
        - its color given as rgb values
    """
    _position = (0,0)  # maybe we dont need that
    _red = 120
    _green = 120
    _blue = 120
    _alive = False

# ______________________________________________________________________________
    def __init__(self, x=None, y=None, alive=False, r=255, g=255, b=255):
        self._position = (x, y)
        self._alive = alive
        self._red = r
        self._green = g
        self._blue = b

# ______________________________________________________________________________
    def changeColor(self, r=255, g=255, b=255):
        self._red = r
        self._green = g
        self._blue = b

# ______________________________________________________________________________
    def kill(self):
        self._alive = False

# ______________________________________________________________________________
    def birth(self):
        r, g, b = colorsys.hsv_to_rgb(random.random(), 1, 1)
        R, G, B = int(255 * r), int(255 * g), int(255 * b)
        self.setColor(R, G, B)
        self._alive = True

    def setColor(self, r, g, b):
        self._red = r
        self._green = g
        self._blue = b
# ______________________________________________________________________________
    def living(self):
        return self._alive

# ______________________________________________________________________________
    def getColor(self):

        if not self._alive:
            return (0, 0, 0)
        return (self._red, self._green, self._blue)



class GameOfLifeExtension(Extension):
    """
        Example with 11 x 21 cells
        The Grid: A 2D List: contains 11 sublist containing 21 'CellElement's each
                             thus covering 231 individual cells

            a  b  c  d  e  f  g  h  i  j  k  l  m  n  h  i  j  k  l  m  n
         0 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         1 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         2 [ ][ ][ ][ ][p][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         3 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         4 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         5 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         6 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         7 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][x][ ][ ][ ][ ][ ][ ][ ][ ]
         8 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
         9 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
        10 [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]

        for example m7 is marked with a 'x'
                    e2 is marked with a 'p'

        every 'CellElement' has:   bool _alive (for alive / dead)
                                   int _red    ( [0, 255] colorvalue)
                                   int _green  ( [0, 255] colorvalue)
                                   int _blue   ( [0, 255] colorvalue)
        """

    #  grid, for present state
    _grid = []

    # cells in this list will be killed
    _kill = []

    # cells in this list will be brought back to life
    _birth = []

    # size of the grid
    _xSize = 0
    _ySize = 0

    # Mouse Position
    _MouseX = 0
    _MouseY = 0

    # Gamemode variables to play around
    _autoplay = False

    proceed_input = False
    last_step = 0


    def set_active(self):
        gridTmp = []

        for y in range(self._ySize):
            line = []
            for x in range(self._xSize):
                cell = CellElement(x, y)
                line.append(cell)
            gridTmp.append(line)

        self._grid = gridTmp
        self.framebuffer.set_tales(True, 10)
        self.last_step = current_milli_time()

    def process_input(self, slot, action):
        x, y = action.pixels
        self._grid[y][x].birth()
        self.proceed_input = True
        self.framebuffer.set_pixel_col(x, y, self._grid[y][x].getColor())

    def loop(self):
        self.framebuffer.clear_frame()
        if current_milli_time() > self.last_step + 100:
            self.last_step = current_milli_time()
            if self.proceed_input:
                self.proceed_input = False
                time.sleep(1)
                return
            self.updateState()
            for i, row in enumerate(self._grid):
                for j, cell_element in enumerate(row):
                    if cell_element.living():
                        self.framebuffer.set_pixel_col(j, i, cell_element.getColor())


    # ______________________________________________________________________________
    def __init__(self):
        super().__init__()
        self.icon_pic = self.read_icon("../icons/gameoflife.ppm")
        self._xSize, self._ySize = self.framebuffer.get_dimensions()



    # ______________________________________________________________________________
    def aliveNeighbour(self, currX, currY):
        """
        checks the 3x3 frame around the position for living cells.

        Args:
            int currX = the x position of the current cell
            int currY = the y position of the current cell

        Returns:
            int living = the amount of living neighbours
        """
        living = 0

        for x in range(currX - 1, currX + 2):
            for y in range(currY - 1, currY + 2):
                # not the cell itselfX + 2
                # if cell in grid (x-axis)
                # if cell in grid (y-axis)
                if (x != currX or y != currY) and (x >= 0 and x < self._xSize) and (y >= 0 and y < self._ySize) and\
                        (self._grid[y][x].living()):
                    living += 1

        return living

    # ______________________________________________________________________________
    def calculateNextState(self):
        """
        Calculates for every cell if it should be alive in the next state
        using the method 'aliveNeighbour'
            dieing cells     : add into list  ( _kill )
            reanimated cells : add into list  ( _birth )
        """
        # iterating over every cell
        for y in range(self._ySize):
            for x in range(self._xSize):
                livingNB = self.aliveNeighbour(x, y)

                # if cell is alive
                if self._grid[y][x].living():
                    if livingNB != 2 and livingNB != 3:
                        self._kill.append((x, y))

                # if cell is dead
                else:
                    if livingNB == 3:
                        self._birth.append((x, y))

    # ______________________________________________________________________________
    def updateState(self):
        """
        updates _grid  by
            - killing     all in  _kill    and
            - reanimating all in  _birth
        """
        self.calculateNextState()
        for coord in self._kill:
            self._grid[coord[1]][coord[0]].kill()
        for coord in self._birth:
            self._grid[coord[1]][coord[0]].birth()
        del self._kill[:]
        del self._birth[:]

# ______________________________________________________________________________

