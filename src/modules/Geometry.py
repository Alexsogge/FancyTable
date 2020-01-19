import numpy as np


class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def normalize(self):
        self.x /= self.magnitude
        self.y /= self.magnitude

    @property
    def magnitude(self) -> float:
        return np.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def normalized(self) -> 'Vector':
        return self / self.magnitude

    @property
    def round_x(self):
        return round(self.x)

    @property
    def round_y(self):
        return round(self.y)

    def __str__(self) -> str:
        return "[{}, {}]".format(self.x, self.y)

    def __add__(self, other) -> 'Vector':
        result = Vector(0, 0)
        if isinstance(other, float) or isinstance(other, int):
            result.x = self.x + other
            result = self.y + other
        elif isinstance(other, Vector):
            result.x = self.x + other.x
            result.y = self.y + other.y
        else:
            pass
        return result

    def __sub__(self, other) -> 'Vector':
        result = Vector(0, 0)
        if isinstance(other, float) or isinstance(other, int):
            result.x = self.x - other
            result.y = self.y - other
        elif isinstance(other, Vector):
            result.x = self.x - other.x
            result.y = self.y - other.y
        else:
            pass
        return result

    def __mul__(self, other) -> 'Vector':
        result = Vector(0, 0)
        if isinstance(other, float) or isinstance(other, int):
            result.x = self.x * other
            result.y = self.y * other
        elif isinstance(other, Vector):
            result.x = self.x * other.x
            result.y = self.y * other.y
        else:
            pass

        return result

    def __truediv__(self, other) -> 'Vector':
        result = Vector(0, 0)
        if isinstance(other, float) or isinstance(other, int):
            result.x = self.x / other
            result.y = self.y / other
        elif isinstance(other, Vector):
            result.x = self.x / other.x
            result.y = self.y / other.y
        else:
            pass
        return result

    def __eq__(self, other) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            return self.magnitude == other
        elif isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __gt__(self, other) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            return self.magnitude > other
        elif isinstance(other, Vector):
            return (self.x > other.x and self.y > other.y) or (self.x > other.x and self.y == other.y) or\
                   (self.x == other.x and self.y > other.y)
        else:
            return False

    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __lt__(self, other) -> bool:
        if isinstance(other, float) or isinstance(other, int):
            return self.magnitude < other
        elif isinstance(other, Vector):
            return (self.x < other.x and self.y < other.y) or (self.x < other.x and self.y == other.y) or \
                   (self.x == other.x and self.y < other.y)
        else:
            return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def set(self, other: 'Vector'):
        self.x = other.x
        self.y = other.y


    def dot(self, other: 'Vector') -> float:
        return self.x * other.x + self.y * other.y

    def calc_reflection_to(self, n: 'Vector') -> 'Vector':
        return self - n * (2 * self.dot(n))

    def reflect_to(self, n: 'Vector'):
        r = self.calc_reflection_to(n)
        self.x = r.x
        self.y = r.y

    def rotate(self, phi: float):
        rad = np.radians(phi)

        k = round(np.cos(rad) * self.x + -np.sin(rad) * self.y)
        self.y = round(np.sin(rad) * self.x + np.cos(rad) * self.y)
        self.x = k
