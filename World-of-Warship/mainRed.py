from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        print("Вы пытаетесь выстрелить за границу игрового поля!")


class BoardUsedException(BoardException):
    def __str__(self):
        print("Вы уже ходили в эту клетку!")


class BoardWrongShipException(BoardException):
    pass


class Ship:
    # firstPoint - носовая часть корабля, l - его длина, а position - его расположение относительно
    # горизонтали или вертикали
    def __init__(self,  firstPoint, l, position):
        self.firstPoint = firstPoint
        self.l = l
        self.position = position

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
    def __init__(self, visible = False, size=6):
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

    # Зона корабля и вокруг него

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for i in ship.dots:
            for ix, iy in near:
                cur = Dot(i.x + ix, i.y + iy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "▣"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=False)
                    print("Корабль уничтожен")
                    return False
                else:
                    print("Корабль ранен")
                    return True

        self.field[d.x][d.y] = "."
        print("Не попал!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.was_killed == len(self.ships)

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход будет на координаты: ").split()

            if len(cords) != 2:
                print("Введите две координаты!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Координаты следует писать цифрами!")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.visible = True

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def print_boards(self):
        print("-" * 18)
        print("Доска игрока:")
        print(self.us.board)
        print("-" * 18)
        print("Доска компьютера:")
        print(self.ai.board)
        print("-"*18)

    def loop(self):
        number = 0
        while True:
            self.print_boards()
            if number % 2 == 0:
                print("-"*18)
                print("Ходит игрок")
                repeat = self.us.move()
            else:
                print("-"*18)
                print("Ходит компьютер")
                repeat = self.ai.move()
            if repeat:
                number -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-"*18)
                print("Игрок победил!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-"*18)
                print("Победил компьютер!")
                break
            number += 1

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()
