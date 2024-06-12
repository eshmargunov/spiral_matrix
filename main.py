import re
import asyncio
import httpx
from typing import List


async def get_matrix(url: str) -> List[int]:
    response = httpx.get(url)
    response.raise_for_status()
    matrix = get_matrix_from_text(response.text)
    return spiral(matrix)


def get_matrix_from_text(text: str) -> List[List[int]]:
    lines = text.split('\n')
    matrix = []
    for line in lines:
        if numbers := re.findall(r'\d+', line):
            matrix.append([int(x) for x in numbers])
    return matrix


def spiral(matrix: List[List[int]]) -> List[int]:
    if not matrix:
        return []

    result = []
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
        for row in range(left, right + 1):
            result.append(matrix[bottom][row])
        bottom -= 1

        # снизу в вверх правый столбец
        if top <= bottom:
            for col in range(bottom, top - 1, -1):
                result.append(matrix[col][right])
            right -= 1

        # справа на налево вверхний ряд.
        if left <= right:
            for row in range(right, left - 1, -1):
                result.append(matrix[top][row])
            top += 1

    return result


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
