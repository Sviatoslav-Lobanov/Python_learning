
def print_step (table): # Печать игрового поля
    print ('  | 1 | 2 | 3 |')
    print ('---------------')
    for i in range(len(table)):
        print(f'{i+1} | {table[i][0]} | {table[i][1]} | {table[i][2]} |')
        print('---------------')

def check (a): # Проверка введенных координат
    point = input(f'Введите {a} :')
    if (point == '1') or (point == '2') or ((point == '3')) :
        return int(point)
    else:
        print('Введите числа 1, 2 или 3')
        return check (a)

def choose(a): # выбор ячейки на игровом поле
    print(f'Ходит {a}')
    x = check('горизонталь')-1
    y = check('вертикаль')-1
    if square[x][y] == ' ':
        square[x][y] = a
    else:
        print('Клетка занята, нужно изменить выбор')
        choose(a)
def winner ():
    combo = [[(0,0),(0,1),(0,2)],
             [(1, 0), (1, 1), (1, 2)],
             [(2, 0), (2, 1), (2, 2)],
             [(0, 0), (1, 0), (2, 0)],
             [(0, 1), (1, 1), (2, 1)],
             [(0, 2), (1, 2), (2, 2)],
             [(0, 0), (1, 1), (2, 2)],
             [(0, 2), (1, 1), (2, 0)]]
    for i in range(8):
        if square[combo[i][0][0]][combo[i][0][1]]==square[combo[i][1][0]][combo[i][1][1]]==square[combo[i][2][0]][combo[i][2][1]]!=' ':
            print(i, square[combo[i][0][0]][combo[i][0][1]], square[combo[i][1][0]][combo[i][1][1]],
                  square[combo[i][2][0]][combo[i][2][1]], combo[i])
            return combo[i]

# New game
square = [[' ']*3 for i in range(3)]
print('Привет, это ваше поле', 'Первыми ходят X, вторыми O','Для хода введите координаты',sep='\n')
print_step(square)
champion = None

for i in range(9):
    mark = 'X' if i % 2 == 0 else 'O'
    choose(mark)
    print_step(square)
    champion = winner()
    if champion:
        print(f'Победил {mark} с комбинацией {champion}')
        break
if champion is None: print('Ничья') 




