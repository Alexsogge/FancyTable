from random import randint


class Frame:

    frame_matrix = []
    tails = False
    tail_value = 1

    colors = ['r', 'g', 'b']

    frame_outputs = []

    def __init__(self, width, height, output=None, init_random=False):
        """
        Initiaize the buffer
        :param width: number of pixels per row
        :param height: number of pixelrows
        :param output: outputdevice
        :param init_random: start with random colored
        """
        for i in range(height):
            self.frame_matrix.append([])
            for j in range(width):
                init_dict = {'r': 0, 'g': 0, 'b': 0}
                if init_random:
                    init_dict['r'] = randint(0, 255)
                    init_dict['g'] = randint(0, 255)
                    init_dict['b'] = randint(0, 255)
                self.frame_matrix[-1].append(init_dict)
        self.frame_outputs.append(output)

    def set_tales(self, tail, val=1):
        """
        If tails is enabled pixels glow out by clean
        :param tail: Sets tailmode
        :param val: the value which the colors will be decreased
        """
        self.tails = tail
        if tail:
            self.tail_value = val

    def add_output(self, output):
        """
        Add an new
        :rtype: object
        """
        self.frame_outputs.append(output)

    def get_dimensions(self):
        """
        Returns the width and height of the frame matrix
        :return: (width, height)
        """
        return len(self.frame_matrix[0]), len(self.frame_matrix)

    def clear_frame(self):
        """
        Clears the Frame. If tails is enabled the pixels will glow out
        """
        if self.tails:
            for row in self.frame_matrix:
                for col in row:
                    for color in self.colors:
                        if col[color] >= self.tail_value:
                            col[color] -= self.tail_value
                        else:
                            col[color] = 0
        else:
            for row in self.frame_matrix:
                for col in row:
                    for color in self.colors:
                        col[color] = 0

    def set_pixel(self, x, y, r, g, b):
        """
        Sets the color of an specific pixel
        :param x: column
        :param y: row
        :param r: red value
        :param g: green value
        :param b: blue value
        """
        self.frame_matrix[y][x]['r'] = r
        self.frame_matrix[y][x]['g'] = g
        self.frame_matrix[y][x]['b'] = b
        # print(self.frame_matrix)

    def set_pixel_col(self, x, y, col):
        """
        Sets the color of an specific pixel
        :param x: column
        :param y: row
        :param col: (red, green, blue)
        """
        self.set_pixel(self, x, y, col[0], col[1], col[2])

    def draw_rect(self, x, y, w, h, r, g, b, fill=True):
        """
        Draws an rectangle on the given position with given size
        :param x: column
        :param y: row
        :param w: width
        :param h: height
        :param r: red
        :param g: green
        :param b: blue
        :param fill: fill out rectangle (Default: True)
        """
        for i in range(w):
            for j in range(h):
                if fill is False and ((i != 0 and j != 0) and (i != w and j != h)):
                    continue
                self.set_pixel(x+i, y+j, r, g, b)

    def draw_rect_col(self, x, y, w, h, col, fill=True):
        """
        Draws an rectangle on the given position with given size
        :param x: column
        :param y: row
        :param w: width
        :param h: height
        :param col: (red, green, blue)
        :param fill: fill out rectangle (Default: True)
        """
        self.draw_rect(x, y, w, h, col[0], col[1], col[2], fill)

    def upload_frame(self):
        """
        Push the frame matrix to the outputs
        """
        for frame_output in self.frame_outputs:
            if frame_output is not None:
                frame_output.upload(self.frame_matrix)

    def get_matrix(self):
        """
        Returns the frame matrix
        :return: list of lists for each row. Lists contain dictionaries with 'r', 'g', 'b' values
        """
        return self.frame_matrix

    def get_pixel(self, x, y):
        """
        Returns the color of an specific pixel
        :param x: column
        :param y: row
        :return: {'r': redval, 'g': greenval, 'b': blueval}
        """
        return self.frame_matrix[y][x]

    def set_matrix_row(self, row, pixels):
        """
        Sets the color of an entire row
        :param row: the row which should be replaced
        :param pixels: List of color dictionaries
        """
        if len(self.frame_matrix) > row and len(pixels) == len(self.frame_matrix[row]):
            self.frame_matrix[row] = pixels

    def set_matrix_column(self, col, pixels):
        """
        Sets the color of an entire column
        :param col: the column which should be replaced
        :param pixels: List of color dictionaries
        """
        if len(self.frame_matrix[0]) > col and len(pixels) == len(self.frame_matrix):
            for i, row in enumerate(self.frame_matrix):
                row[col] = pixels[i]

    def get_matrix_row(self, row, pixels):
        """
        Returns the color of an entire row
        :param row: the row which should be returned
        """
        if len(self.frame_matrix) > row:
            return self.frame_matrix[row]

    def get_matrix_column(self, col, pixels):
        """
        Returns the color of an entire column
        :param col: the column which should be returned
        """
        if len(self.frame_matrix[0]) > col:
            column = []
            for i, row in enumerate(self.frame_matrix):
                column.append(row[col])
            return column


