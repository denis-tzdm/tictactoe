FIELD_SIZE = 3  # размер поля
WIN_SEQ_LEN = 3  # длина выигрышной последовательности
# соответствие значений списка (поля игры) и символов на экране
SYMBOLS = {0: ' ', 1: '×', 2: 'o'}
# варианты исхода игры
OUTCOMES = {1: 'игрок 1', 2: 'игрок 2', 3: 'ничья', 4: 'партия прервана'}
STOP_WORD = '0'  # стоп-слово для прерывания партии
STOP_CODE = 4  # код возврата при прерывании партии
DRAW_CODE = 3  # код возврата ничьей

# смещение координат на 1 меньше выигрышной последовательности,
# потому что она включает текущий ход
OFFSET = WIN_SEQ_LEN - 1


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


def get_line_range(ind: int) -> range:
    """Получить диапазон координаты для горизонтальной или вертикальной линии

    Одна из координат вертикальной или горизонтальной линии,
    построенной относительно переданной точки,
    в которой может быть выигрышная последовательность.
    """
    return range(
        max(0, ind - OFFSET),  # не меньше 0
        min(FIELD_SIZE - 1, ind + OFFSET) + 1  # и в переделах поля
    )


def get_diag_points(field: list,
                    row: int,
                    col: int,
                    y_factor: 1 | -1) -> list:
    """Получить точки диагонали для проверки победы.

    Точки диагональной линии от заданной позиции, в которой
    может быть выигрышная последовательность.
    """
    # для диагонали проверяем обе координаты,
    # ни одна не должна выходить за пределы поля
    # для обратной диагонали движение по вертикали
    # противоположно по знаку движению по горизонтали
    return [field[row + y_factor * ind][col + ind]
            for ind in range(-OFFSET, OFFSET + 1)
            if (0 <= row + y_factor * ind <= FIELD_SIZE - 1
                and 0 <= col + ind <= FIELD_SIZE - 1)]


def check_is_over(field, point):
    # проверяем только линии, в которых задействована новая точка
    row = point[0]
    col = point[1]

    # возможные победные последовательности -- N одинаковых элементов подряд
    # в координатах ±(N-1) точки от текущей по горизонтали, вертикали, диагонали
    check_cells = [
        [field[row][ind] for ind in get_line_range(col)],  # горизонталь
        [field[ind][col] for ind in get_line_range(row)],  # вертикаль
        get_diag_points(field, row, col, 1),  # диагональ \
        get_diag_points(field, row, col, -1)  # диагональ /
    ]

    # проверяем линии срезами, равными длине выигрышной последовательности
    # если в срезе все значения одинаковые, значит, текущий игрок победил
    for seq in check_cells:
        seq_len = len(seq)
        if seq_len < WIN_SEQ_LEN:
            continue
        if any(
                len(set(seq[ind:ind + WIN_SEQ_LEN])) == 1
                for ind in range(seq_len - WIN_SEQ_LEN + 1)
        ):
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
    if not all(map(str.isdigit, move_list)):
        return None

    # координаты
    col, row = map(lambda x: int(x) - 1, move_list)

    # если одно из значений вне поля
    if not all(map(lambda x: 0 <= x <= FIELD_SIZE - 1, [col, row])):
        return None

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
        move = input('Введите координаты в виде "x y"'
                     f' или "{STOP_WORD}" для прерывания партии: ')
        if move.lower() == STOP_WORD.lower():
            return STOP_CODE

        point = validate_input(move, field)

        if point:
            field[point[0]][point[1]] = current_player
            code_over = check_is_over(field, point)
            if code_over:
                show_field(field)
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
