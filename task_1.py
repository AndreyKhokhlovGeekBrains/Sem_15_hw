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


class NegativeValueError(ValueError):
    pass


class Rectangle:
    def __init__(self, width, height=None):
        if width <= 0:
            logger.error(f'Ширина должна быть положительной, а не {width}')
            raise NegativeValueError(f'Ширина должна быть положительной, а не {width}')
        self._width = width
        if height is None:
            self._height = width
        else:
            if height <= 0:
                logger.error(f'Высота должна быть положительной, а не {height}')
                raise NegativeValueError(f'Высота должна быть положительной, а не {height}')
            self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value > 0:
            logger.info(f'Переназначение ширины: текущая ширина {self._width}, новая ширина {value}')
            self._width = value
        else:
            logger.error(f'Ширина должна быть положительной, а не {value}')
            logger.info(f'Ширина не была изменена. Текущая ширина: {self._width}')

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value > 0:
            logger.info(f'Переназначение высоты: текущая высота {self._height}, новая высота {value}')
            self._height = value
        else:
            logger.error(f'Высота должна быть положительной, а не {value}')
            logger.info(f'Высота не была изменена. Текущая высота: {self._height}')

    def perimeter(self):
        return 2 * (self._width + self._height)

    def area(self):
        return self._width * self._height

    def __add__(self, other):
        width = self._width + other._width
        perimeter = self.perimeter() + other.perimeter()
        height = perimeter / 2 - width
        return Rectangle(width, height)

    def __sub__(self, other):
        if self.perimeter() < other.perimeter():
            self, other = other, self
        width = abs(self._width - other._width)
        perimeter = self.perimeter() - other.perimeter()
        height = perimeter / 2 - width
        if height < 0:
            logger.error(f'При вычитании прямоугольника с шириной {other.width} и высотой {other.height} из примоугольника с шириной {self._width} и высотой {self._height} получается отрицатльная высота {height}')
        return Rectangle(width, height)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Создаем экземпляр класса Rectangle')
    parser.add_argument(
        'params',
        nargs='*',
        default=None,
        help='2 числа через пробел, где первое число является шириной прямоугольника, а второе - высотой (пример: 5 2). '
             'Если задан только онид параметр, то высота будет равна ширине.'
    )
    args = parser.parse_args()

    if args.params:
        if len(args.params) == 2:
            width = int(args.params[0])
            height = int(args.params[1])
        elif len(args.params) == 1:
            width = int(args.params[0])
            height = None
        else:
            logger.error(f'При передаче параметров в коммандной строке было передано некорректное количество аргументов {args}')
            raise ValueError('Передано некорректное количество аргументов')

        try:
            if width is not None and height is not None:
                rect = Rectangle(width, height)
            elif width is not None and height is None:
                rect = Rectangle(width)
            logger.info(f'В коммандной строке были переданы параметры {args.params}. Был создан примоугольник с сторонами {rect.width} и {rect.height}')
        except NegativeValueError as e:
            logger.error(f'Ошибка при создании прямоугольника из параметров {args.params}, переданных в коммандной строке: {e}')
    else:
        r1 = Rectangle(5)
        r2 = Rectangle(3, 4)
        r1.width = 6
        r2.height = 5
        r1.width = -6
        r2.height = -5
        r3 = Rectangle(10, 3)
        r4 = Rectangle(1, 4)
        r5 = r3 - r4


