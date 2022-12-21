class Dot:
    def __init__(self, x, y):
        self.x(x)
        self.y(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    # firstPoint - носовая часть корабля, l - его длина, а position - его расположение относительно
    # горизонтали или вертикали
    def __init__(self,  firstPoint, l, position):
        self.firstPoint(firstPoint)
        self.l(l)
        self.position(position)

    @property
    def dots(self):
        # Создаем список кораблей
        ship_dots = []
        #
        for i in range(self.l):
            cur_x = self.firstPoint.x
            cur_y = self.firstPoint.y

            if self.position == 0:
                cur_x += i
            elif self.position == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shoten(self, hit):
        return hit in self.dots


class Board:
    def __init__(self, visible = False, size = 6):
        self.size = size
        self.visible = visible
        self.was_killed = 0
        self.field = [["0"] * size for _ in range(size)]
        self.busy = []
        self.ships = []
    # Чертим игровое поле
    def __str__(self):
        paint = " "
        paint += " | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            paint += f"\n{i + 1} | " + " | ".join(row) + " | "
        # виден корабль
        if self.visible:
            paint = paint.replace("▣", "0")
        return paint
    # проверяем, не стреляет ли игрок за поле, просто зная значение size
    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))



