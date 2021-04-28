from random import randint
# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней.
# Внешняя логика игры — пользовательский интерфейс, искусственный интеллект, игровой контроллер, который считает побитые корабли.

# В начале имеет смысл написать классы исключений, которые будет использовать наша программа. Например, когда игрок пытается выстрелить в клетку за пределами поля, во внутренней логике должно выбрасываться соответствующее исключение BoardOutException, а потом отлавливаться во внешней логике, выводя сообщение об этой ошибке пользователю.
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Корабль вышел за границы поля"
    pass

# Далее нужно реализовать класс Dot — класс точек на поле. Каждая точка описывается параметрами:
#
# Координата по оси x .
# Координата по оси y .
# В программе мы будем часто обмениваться информацией о точках на поле, поэтому имеет смысле сделать отдельный тип данных дня них.
# Очень удобно будет реализовать в этом классе метод __eq__, чтобы точки можно было проверять на равенство.
# Тогда, чтобы проверить, находится ли точка в списке, достаточно просто использовать оператор in, как мы делали это с числами .
class Dot:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x},{self.y})"


# Следующим идёт класс Ship — корабль на игровом поле, который описывается параметрами:
#
# Длина.
# Точка, где размещён нос корабля.
# Направление корабля (вертикальное/горизонтальное).
# Количеством жизней (сколько точек корабля еще не подбито).
# И имеет методы:
#
# Метод dots, который возвращает список всех точек корабля.

class Ship:
    def __init__(self, bow, long, orientation):
        self.bow = bow
        self.long = long
        self.orientation = orientation
        self.lives = long

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.long):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == 0:
                cur_x += i

            elif self.orientation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

# Самый важный класс во внутренней логике — класс Board — игровая доска. Доска описывается параметрами:
#
# Двумерный список, в котором хранятся состояния каждой из клеток.
# Список кораблей доски.
# Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски).
# Количество живых кораблей на доске.
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    # И имеет методы:
    #
    # Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения).

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке кораблей (помечает соседние точки,
    # где корабля по правилам быть не может).

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    # Метод, который выводит доску в консоль в зависимости от параметра hid.
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    # Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит.
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения).
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class All_board():
    def __init__(self, board_1=None, board_2=None):
        self.board_1 = board_1
        self.board_2 = board_2

    def __str__(self):
        res = ""
        res2 = ""
        res += "   Доска пользователя             Доска компьютера        "
        res += f"\n  | 1 | 2 | 3 | 4 | 5 | 6 | ...  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.board_1.field):
            for j, row2 in enumerate(self.board_2.field):
                if i == j:
                    res2 = " | ".join(row2).replace("■", "O")
                    res += f"\n{i + 1} | " + " | ".join(row) + " | " +"..."+ f"{i + 1} | " + res2 + " | "

        return res

# Теперь нужно заняться внешней логикой: Класс Player — класс игрока в игру (и AI, и пользователь). Этот класс будет родителем для классов с AI и с пользователем.
# Игрок описывается параметрами:
# Собственная доска (объект класса Board)
# Доска врага.
# И имеет следующие методы:
#
# ask — метод, который «спрашивает» игрока, в какую клетку он делает выстрел.
# Пока мы делаем общий для AI и пользователя класс, этот метод мы описать не можем.
# Оставим этот метод пустым. Тем самым обозначим, что потомки должны реализовать этот метод.
# move — метод, который делает ход в игре.
# Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot), отлавливаем исключения, и если они есть, пытаемся повторить ход.
# Метод должен возвращать True, если этому игроку нужен повторный ход (например если он выстрелом подбил корабль).
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        last_shoot = None
        while True:
            try:
                target = self.ask(last_shoot)
                repeat = self.enemy.shot(target)
                # last_shoot = target
                # if repeat: print ("после попадания вторая попытка",last_shoot)
                return repeat
            except BoardException as e:
                print(e)

# Теперь нам остаётся унаследовать классы AI и User от Player и переопределить в них метод ask.
# Для AI это будет выбор случайной точка, а для User этот метод будет спрашивать координаты точки из консоли.


class AI(Player):
    def ask(self,last_shoot):
        # print(last_shoot)  попытка научить стрелять рядом
        # if last_shoot:
        #     while True:
        #         try:
        #             print("стреляю рядом 1")
        #             d = Dot(last_shoot.x, last_shoot, y + 1)
        #             break
        #         except BoardException as e:
        #             print(e)
        #         try:
        #             print("стреляю рядом 2")
        #             d = Dot(last_shoot.x, last_shoot, y - 1)
        #             break
        #         except BoardException as e:
        #             print(e)
        #         try:
        #             print("стреляю рядом 3")
        #             d = Dot(last_shoot.x + 1, last_shoot, y)
        #             break
        #         except BoardException as e:
        #             print(e)
        #         try:
        #             print("стреляю рядом 4")
        #             d = Dot(last_shoot.x - 1, last_shoot, y)
        #             break
        #         except BoardException as e:
        #             print(e)
        #
        # else:
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self,last_shoot):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

# После создаём наш главный класс — класс Game. Игра описывается параметрами:
#
# Игрок-пользователь, объект класса User.
# Доска пользователя.
# Игрок-компьютер, объект класса Ai.
# Доска компьютера.
# И имеет методы:
#
# random_board — метод генерирует случайную доску. Для этого мы просто пытаемся в случайные клетки изначально пустой доски расставлять корабли (в бесконечном цикле пытаемся поставить корабль в случайную току, пока наша попытка не окажется успешной). Лучше расставлять сначала длинные корабли, а потом короткие. Если было сделано много (несколько тысяч) попыток установить корабль, но это не получилось, значит доска неудачная и на неё корабль уже не добавить. В таком случае нужно начать генерировать новую доску.
# greet — метод, который в консоли приветствует пользователя и рассказывает о формате ввода.
# loop — метод с самим игровым циклом. Там мы просто последовательно вызываем метод mode для игроков и делаем проверку, сколько живых кораблей осталось на досках, чтобы определить победу.
# start — запуск игры. Сначала вызываем greet, а потом loop.
class Game:
    def __init__(self, size=6):
        self.size = size
        # pl = self.self_board()
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)
        self.all = All_board(self.us.board, self.ai.board)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
# Даем игроку самому расставить корабли
    def self_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        print("--------------------")
        print("-Установите корабли-")
        print(" формат ввода: x y z")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        print(" z - направление корабля (1-горизонтально, 0-вертикально)")

        for l in lens:
            while True:
                print("-" * 20)
                print("Доска пользователя:")
                print(board)

                bows = input(f"Введите координаты и направление для корабля длинной {l}: ").split()

                if len(bows) != 3:
                    print(" Введите 3 значения! координтаы носа и направление ")
                    continue

                x, y, z = bows

                if not (x.isdigit()) or not (y.isdigit()) or not (z.isdigit()):
                    print(" Введите числа! ")
                    continue

                x, y, z = int(x), int(y), int(z)
                ship = Ship(Dot(x-1, y-1), l, z)
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            # print("Доска пользователя:")
            # print(self.us.board)
            # print("-" * 20)
            # print("Доска компьютера:")
            # print(self.ai.board)
            print(self.all)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

# И останется просто создать экземпляр класса Game и вызвать метод start.
g = Game()
g.start()