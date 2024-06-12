# Решение Тестового задания на python-разработчик

Первым делом нужно внимательно прочитать условие задачи. Самое главное в ней то, что дана матрица вида
```python
+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+
```
и нужно получить список, содержащий результат обхода полученной матрицы по спирали `[10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]`.
Для удобства этот список можно также представить в виде матрицы
```python
[
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]
```
Всё остальное в задании просто детали.

## 1 этап. Получение матрицы
По условию задачи матрицу мы можем получить по сети. В требованиях указано, что нужно использовать одну из асинхронных библиотек: `aiohttp, httpx или другого компонента на asyncio.`
Напишем функцию `get_matrix`, которая пока просто делает http-запрос и возвращает текст ответа. Сразу же проверим с помощью метода `raise_for_status()`, что во время запроса не было никаких ошибок.
```python
import httpx
import asyncio
from typing import List


async def get_matrix(url: str) -> List[int]:
    response = httpx.get(url)
    response.raise_for_status()
    return response.text


if __name__ == '__main__':
    _url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    _result = asyncio.run(get_matrix(_url))
    print(_result)
```

### 1.1 этап. Преобразование ответа к матрице
Преобразуем текст ответа к квадратной матрице, содержащий числа, в функции.
```python
import re
from typing import List


def get_matrix_from_text(text: str) -> List[List[int]]:
    lines = text.split('\n')
    matrix = []
    for line in lines:
        if numbers := re.findall(r'\d+', line):
            matrix.append([int(x) for x in numbers])
    return matrix
```
Можно разбить текст по символу `\n`. Так мы получим список из строк двух видов:
1. `+-----+-----+-----+-----+` их можно пропустить;
2. `|  10 |  20 |  30 |  40 |` здесь нужно достать числа. Для этого есть множества вариантов. 
В моём варианте мы достаём их через [регулярные выражение](https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%B3%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D1%8B%D0%B5_%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F).


## 2 этап. Алгоритм обхода матрицы 
Это самый сложный этап при решении задачи. Нужно реализовать функцию, которая принимает числовую матрицу и возвращает список чисел.
Напишем внешний цикл `while top <= bottom and left <= right:`, который проверяет границы матрицы. 
В нём же будет 4 цикла `for` для сбора чисел в список против часовой стрелки, начиная с левого верхнего угла.
```python
from typing import List


def spiral(matrix: List[List[int]]) -> List[int]:
    if not matrix:
        return []

    result = []
    # задаём размерность матрицы и её границы
    rows = len(matrix)
    cols = len(matrix[0])
    top = 0
    bottom = rows - 1
    left = 0
    right = cols - 1

    while top <= bottom and left <= right:
        # обход чисел сверху вниз в левом столбце
        for col in range(left, bottom + 1):
            result.append(matrix[col][top])
        left += 1

        # справа налево нижний ряд
        for row in range(left, bottom + 1):
            result.append(matrix[right][row])
        bottom -= 1

        # снизу в вверх правый столбец
        if top <= bottom:
            for col in range(bottom, top - 1, -1):
                result.append(matrix[col][right])
            right -= 1

        # справа на налево верхний ряд.
        if left <= right:
            for row in range(right, left - 1, -1):
                result.append(matrix[top][row])
            top += 1

    return result

```

### 2.1 этап. Тесты на алгоритм обхода матрицы
Так как этот алгоритм самая сложная часть в задании, то нужно написать на него тесты
Ограничимся 4 тестовыми сценариями
```python
import pytest

from main import spiral


@pytest.mark.parametrize("matrix, expected_data", [
    ([
         [1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10, 11, 12],
         [13, 14, 15, 16]
     ],
     [
         1, 5, 9, 13,
         14, 15, 16, 12,
         8, 4, 3, 2,
         6, 10, 11, 7,
     ]
    ),
    ([
         [0, 100000000],
         [0, 0]
     ],
     [0, 0, 0, 100000000]),
    ([], []),
    ([[1]], [1]),
]

                         )
def test_spiral(matrix, expected_data):
    assert spiral(matrix) == expected_data

```

## 3 этап. Собираем всё вместе
Финальное представление функции `get_matrix` будет иметь вид
```python
import re
import asyncio
import httpx
from typing import List


async def get_matrix(url: str) -> List[int]:
    response = httpx.get(url)
    response.raise_for_status()
    matrix = get_matrix_from_text(response.text)
    return spiral(matrix)


if __name__ == '__main__':
    _url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    _result = asyncio.run(get_matrix(_url))
    TRAVERSAL = [
        10, 50, 90, 130,
        140, 150, 160, 120,
        80, 40, 30, 20,
        60, 100, 110, 70,
    ]
    assert _result == TRAVERSAL
```

## 4 этап. requirements.txt
Для решения этой задачи мы использовали несколько внешних зависимостей. Правильно их перечислить в файле requirements.txt
```requirements
httpx==0.27.0
asyncio==3.4.3
pytest==8.2.2
```