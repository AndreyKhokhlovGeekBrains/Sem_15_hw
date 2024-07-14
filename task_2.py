import logging
import os
import argparse

FORMAT = '{levelname:<8} - {asctime}. В модуле "{name}" ' \
         'в строке {lineno:03d} функция "{funcName}()" ' \
         'в {created} секунд записала сообщение: {msg}'


def get_file_name():
    my_str = os.path.basename(__file__)
    res = my_str[:-3]
    return res


logging.basicConfig(
    format=FORMAT,
    style='{',
    level=logging.INFO,
    filemode='a',
    filename=f'{get_file_name()}.log',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


def check_queens(input_list: list[tuple[int, int]]) -> bool:
    """
    Программа получает на вход восемь пар чисел, каждое число от 1 до 8 - координаты 8 ферзей.
    Если ферзи не бьют друг друга возвращается истина, а если бьют - ложь.
    """
    logger.info(f'Был получен список со следующими параметрами: {input_list}')
    length = len(input_list)
    if length > 8:
        logger.error(f'Был получен список из {length} элементов. Список не должен превышать 8 элементов.')

    for i in range(length):
        for j in range(i + 1, length):
            # Check if queens share the same row or column
            if input_list[i][0] == input_list[j][0] or input_list[i][1] == input_list[j][1]:
                return False
            # Check if queens share the same diagonal: if any two queens share the same diagonal,
            # the absolute difference between their row indices must be equal to the absolute difference
            # between their column indices
            elif abs(input_list[i][0] - input_list[j][0]) == abs(input_list[i][1] - input_list[j][1]):
                logger.info(f'Программа отработала успешно и вернула значение False')
                return False
    logger.info(f'Программа отработала успешно и вернула значение True')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Проверяем расстановку ферзей таким образом, чтобы они не били друг друга')
    parser.add_argument(
        'queens',
        nargs='*',
        default=None,
        help='16 чисел через пробел, каждое число от 1 до 8 (пример: "1 1 2 2 3 3 4 4 5 5 6 6 7 7 8 8")'
    )
    # Пример команды для запуска из коммандной строки:
    # python task_2.py 1 1 2 5 3 8 4 6 5 3 6 7 7 2 8 4
    args = parser.parse_args()

    if args.queens:
        queens_cmd = [(int(args.queens[i]), int(args.queens[i + 1])) for i in range(0, len(args.queens), 2)]
        print(queens_cmd)
        if len(args.queens) % 2 != 0 or len(args.queens) > 16:
            raise ValueError('Вы должны указать четное количество координат, до 16 значений (8 пар).')
        print(check_queens(queens_cmd))
    else:
        queens = [(1, 1), (2, 5), (3, 8), (4, 6), (5, 3), (6, 7), (7, 2), (8, 4), (3, 5)]
        print(check_queens(queens))



