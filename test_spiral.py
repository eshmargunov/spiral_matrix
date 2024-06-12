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
