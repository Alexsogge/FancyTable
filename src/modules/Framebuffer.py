from random import randint


class Frame:

    frame_matrix = []
    tails = False
    tail_value = 1

    colors = ['r', 'g', 'b']

    frame_outputs = []

    def __init__(self, width, height, output=None, init_random=False):
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
        self.tails = tail
        if tail:
            self.tail_value = val

    def add_output(self, output):
        self.frame_outputs.append(output)

    def get_dimensions(self):
        return len(self.frame_matrix[0]), len(self.frame_matrix)

    def clear_frame(self):
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
        self.frame_matrix[y][x]['r'] = r
        self.frame_matrix[y][x]['g'] = g
        self.frame_matrix[y][x]['b'] = b
        # print(self.frame_matrix)

    def set_pixel_col(self, x, y, col):
        self.set_pixel(self, x, y, col[0], col[1], col[2])

    def draw_rect(self, x, y, w, h, r, g, b, fill=True):
        for i in range(w):
            for j in range(h):
                if fill is False and ((i != 0 and j != 0) and (i != w and j != h)):
                    continue
                self.set_pixel(x+i, y+j, r, g, b)

    def draw_rect_col(self, x, y, w, h, col, fill=True):
        self.draw_rect(x, y, w, h, col[0], col[1], col[2], fill)

    def upload_frame(self):
        for frame_output in self.frame_outputs:
            if frame_output is not None:
                frame_output.upload(self.frame_matrix)

    def get_dimensions(self):
        return len(self.frame_matrix[0]), len(self.frame_matrix)


