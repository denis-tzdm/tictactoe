# соответствие значений списка (поля игры) и символов на экране
SYMBOLS = {0: ' ', 1: '×', 2: 'o'}
FIELD_SIZE = 3  # размер поля
# варианты исхода игры
OUTCOMES = {1: 'игрок 1', 2: 'игрок 2', 3: 'ничья', 4: 'партия прервана'}
STOP_WORD = '0'  # стоп-слово для прерывания партии
STOP_CODE = 4  # код возврата при прерывании партии
DRAW_CODE = 3  # код возврата ничьей


def show_field(field):
    show_cells_filling(' ')
    for col_num in range(FIELD_SIZE + 1):
        print('  ' + str(col_num) if col_num > 0 else '   ', end='  |')
    print()
    show_cells_filling('_')

    for row_index, row in enumerate(field):
        show_cells_filling(' ')
        print('  ' + str(row_index + 1), end='  |')
        for col in row:
            print('  ' + SYMBOLS[col], end='  |')
        print()
        show_cells_filling('_')


def show_cells_filling(char):
    for _ in range(FIELD_SIZE + 1):
        print(char * 5, end='|')
    print()


def check_is_over(field, point):
    # проверяем только линии, в которых задействована новая точка
    row = point[0]
    col = point[1]
    # линии по горизонтали или по вертикали
    if len(set(field[row])) == 1 or \
            len(set(row[col] for row in field)) == 1:
        return field[row][col]

    # линии по диагонали
    # 1 1 -> 3 3
    # если обе координаты точки одинаковые
    if row == col:
        if len(set(field[ind][ind] for ind in range(FIELD_SIZE))) == 1:
            return field[row][col]
    # 1 3 -> 3 1
    # если размер поля минус первая координата точки равна второй координате
    # -1, т. к. считаем от 0
    if FIELD_SIZE - row - 1 == col:
        if len(set(field[FIELD_SIZE - ind - 1][ind] for ind in range(FIELD_SIZE))) == 1:
            return field[row][col]

    # не осталось ходов
    if not any(0 in row for row in field):
        return DRAW_CODE

    return None


def validate_input(move, field):
    move_list = move.split()

    # если введено не 2 значения
    if len(move_list) != 2:
        return None

    # если одно из введённых значений состоит не только из цифр
    if not all(map(lambda x: x.isdigit(), move_list)):
        return None

    # если одно из значений меньше 1 или больше размера поля
    if not all(map(lambda x: 1 <= int(x) <= FIELD_SIZE, move_list)):
        return None

    # иначе координаты
    col, row = list(map(lambda x: int(x) - 1, move_list))

    # точка уже занята
    if field[row][col]:
        return None

    return row, col


def game():
    field = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
    point = ()
    current_player = 1
    move = ''

    while True:
        show_field(field)

        if move and not point:
            print("Неверный ввод :-(")

        print(f'{OUTCOMES[current_player].capitalize()}, Ваш ход.')
        move = input('Введите координаты в виде "колонка строка"'
                     f' или "{STOP_WORD}" для прерывания партии: ')
        if move.lower() == STOP_WORD.lower():
            return STOP_CODE

        point = validate_input(move, field)

        if point:
            field[point[0]][point[1]] = current_player
            code_over = check_is_over(field, point)
            if code_over:
                return code_over
            current_player = 2 if current_player == 1 else 1


def init():
    for p in range(1, 3):
        user_input = input(f'{OUTCOMES[p].capitalize()}, введите имя: ')
        if user_input != '':
            OUTCOMES[p] = user_input

    while True:
        outcome = game()

        pre = 'Победил(а)' if outcome < 3 else ''
        if outcome != STOP_CODE:
            print('Партия завершена!')
        print(f'{pre} {OUTCOMES[outcome].capitalize()}.'.strip())

        more = input('Ещё партию? ("y"/"д" = да, иначе нет) ')
        if not more or more.lower() not in 'yд':
            break


if __name__ == '__main__':
    init()
