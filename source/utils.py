def count_used_squares(sudoku) -> int:
    """
    This function takes a sudoku as input and returns the number of squares that have a number on it.
    """
    # set the counter to 0
    counter = 0
    # iterate over every element on the sudoku
    for row in range(len(sudoku)):
        for column in range(len(sudoku)):
            # if the element exist (is not None), update the counter
            if sudoku[row][column]:
                counter += 1
    return counter


def is_filled(sudoku) -> bool:
    """
    This function takes a sudoku as input and returns `False` if the sudoku have a `EMPTY` square, return `True` otherwise.
    """
    # iterates over every element
    for row in sudoku:
        for element in row:
            # if find a element that dont exist then return False
            if not element:
                return False
    return True


def print_sudoku(sudoku) -> None:
    """
    This function takes a sudoku as input and print the sudoku in a readable way on the console.
    """
    # iterates over every element
    for row in sudoku:
        for element in row:
            # print the element with a space but without break line
            print(element, end=" ")
        # print a break line
        print()


# |--------------------pygame---------------------------|
"""
Functions whose only purpose in life is to help the pygame runner 
dont need to be documented
"""
def get_range(position: tuple[int, int]) -> list[int]:
    row, column = position
    sudoku_range = set()
    for aux in range(9):
        sudoku_range.add((aux, column))
        sudoku_range.add((row, aux))
    a = (row // 3) * 3
    b = (column // 3) * 3

    for row in range(a, a + 3):
        for column in range(b, b + 3):
            sudoku_range.add((row, column))
    return sudoku_range


def get_same_number(position, sudoku):
    row, column = position
    value = sudoku[row][column]
    everything = set()
    for i in range(9):
        for j in range(9):
            if i != row and j != column and sudoku[i][j] == value:
                everything.add((i, j))
    return everything
