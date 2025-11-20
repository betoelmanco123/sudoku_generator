import time, random

EMPTY = None


def get_options(sudoku: list[list[int]], position: tuple[int, int]) -> list[int]:
    """
    This function takes a sudoku and a position and return all the possible numbers the square can take
    """
    row, column = position
    # create a set with all the accepatable values in a sudoku
    values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for aux in range(9):
        # discard all the values that are on the same row and column
        values -= {sudoku[aux][column], sudoku[row][aux]}
    # determinite the left corner of the quadrant the position is on
    a = (row // 3) * 3
    b = (column // 3) * 3
    # iterates over every element on the same quadrant
    for row in range(a, a + 3):
        for column in range(b, b + 3):

            if sudoku[row][column]:
                # discard all the values that are on the same quadrant
                values -= {sudoku[row][column]}
    return list(values)


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


# print a sudoku in a readable way
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


def get_next_target(sudoku: list[list[int]]) -> tuple:
    """
    This function takes a board of sudoku and returns the position (x, y) of a EMPTY square
    """
    # initialize a value that must be bigger than every square
    length = 10
    best_option = None
    # itereates over eveery element on the sudoku
    for row in range(len(sudoku)):
        for column in range(len(sudoku)):
            # only check for empty squares
            if not sudoku[row][column]:
                # get the number of options the square has
                current = len(get_options(sudoku, (row, column)))
                # if a square can only have one number, then we inmediatly take it
                if current == 1:
                    return (row, column)
                # if theres a square with less options than the current then we take that
                if current < length:
                    # update the data
                    length = current
                    best_option = (row, column)
    return best_option


# returns all the posibles values for a given position on a given board
def _solve_sudoku(sudoku, record=None):
    """
    This function takes a sudoku as argument and modify it to the solution,
    return `True` if the sudoku has solution, `False` otherwise
    """
    # it the sudoku is filled then it must be already solve
    if is_filled(sudoku):
        # store the state on the record
        if record:
            record.append([row[:] for row in sudoku])
        # return True indicating we finished
        return True
    # get the next target
    row, column = get_next_target(sudoku)
    # get the avaiable numbers for the current target
    options = get_options(sudoku, (row, column))
    # iterate over each avaiable number
    for number in options:
        # set the option in the sudoku
        sudoku[row][column] = number
        # save the step to the record
        if record is not None:
            record.append([row[:] for row in sudoku])
        # if the recursive step return True, then we also do it
        if _solve_sudoku(sudoku, record):
            return True
    # the backtrack step
    sudoku[row][column] = EMPTY
    # return False to break this branch
    return False


def has_solution(sudoku1):
    """
    This function takes a sudoku as input and return `True`if it has solution, return `False` otherwise
    This function does not modify the original sudoku.
    """
    sudoku = [row[:] for row in sudoku1]
    return solve_sudoku(sudoku)


def solve_sudoku(sudoku):
    """
    This function takes a sudoku as input and return True or False if it have solution,
    the solution, and the record of the steps takes to solve the sudoku
    """
    # create an EMPTY record
    record = []
    # create a copy of the sudoku
    copy = [row[:] for row in sudoku]
    result = _solve_sudoku(copy, record)
    return result, copy, record


def count_used_squares(sudoku):
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


def random_best_target(sudoku, predicate):
    """
    This function takes a sudoku, decide what are the best option to be ne next target and return one of them at random
    """
    length = 10
    options = list()
    for row in range(9):
        for column in range(9):
            if predicate(sudoku[row][column]):
                values = get_options(sudoku, (row, column))
                if len(values) < length:
                    length = len(values)
                    options = [(row, column)]
                elif len(values) == length:
                    options.append((row, column))
    return random.choice(options)


def _generate_filled_sudoku(sudoku, record=None):
    """
    This function takes a empty board of sudoku to convert it to a completly filled one and returns True
    """
    if is_filled(sudoku):
        if record is not None:
            record.append(sudoku)
        return True
    row, column = random_best_target(sudoku, lambda v: not v)
    options = get_options(sudoku, (row, column))
    copy = options[:]
    for _ in range(len(options)):
        if record is not None:
            record.append(sudoku)
        value = random.choice(copy)
        copy.remove(value)
        sudoku[row][column] = value
        if _generate_filled_sudoku(sudoku, record):
            return True
    sudoku[row][column] = EMPTY
    return False


def generate_filled_sudoku():
    """
    This function returns a sudoku solved
    """
    void = [[EMPTY for _ in range(9)] for _ in range(9)]
    _generate_filled_sudoku(void)
    return void


def take_off_squares(sudoku1, current):
    """
    This function takes a sudoku and removes numbers until has less than the `level`
    """
    if count_used_squares(sudoku1) < current:
        return True

    target = random_best_target(sudoku1, lambda v: bool(v))
    row, column = target

    save = sudoku1[row][column]

    sudoku1[row][column] = EMPTY
    if has_solution(sudoku1):
        if take_off_squares(sudoku1, current):
            return True

    sudoku1[row][column] = save
    return False


def get_playable_sudoku(level):

    levels = [40, 35, 27]
    current = levels[level]
    sudoku = generate_filled_sudoku()
    take_off_squares(sudoku, current)

    return sudoku


# |--------------------pygame---------------------------|
def get_range(position: tuple[int, int]) -> list[int]:
    x, y = position
    sudoku_range = set()
    for aux in range(9):
        sudoku_range.add((aux, y))
        sudoku_range.add((x, aux))
    a = (x // 3) * 3
    b = (y // 3) * 3

    for row in range(a, a + 3):
        for column in range(b, b + 3):
            sudoku_range.add((row, column))
    return sudoku_range


def get_same_number(position, sudoku):
    x, y = position
    value = sudoku[x][y]
    everything = list()
    for i in range(9):
        for j in range(9):
            if i != x and j != y and sudoku[i][j] == value:
                everything.append((i, j))
    return everything


def main():
    start = time.time()
    new = get_playable_sudoku(1)
    result, solution, record = solve_sudoku(new)
    if not result:
        print("This sudoku dont have a solution")
    print_sudoku(solution)
    finish = time.time()
    print(finish - start)


if __name__ == "__main__":
    main()


def has_unique_solution(sudoku):
    # Contador de soluciones
    solutions = 0
    sudoku1 = [row[:] for row in sudoku]

    def backtrack(sudoku_2):
        sudoku = [row[:] for row in sudoku_2]
        nonlocal solutions

        # Si ya encontramos más de 1 solución, no hace falta seguir
        if solutions > 1:
            return True

        if is_filled(sudoku):
            solutions += 1
            return

        # Elegir siguiente casilla
        x, y = get_next_target(sudoku)
        options = get_options(sudoku, (x, y))

        for k in options:
            sudoku[x][y] = k
            if backtrack(sudoku):
                return True

        sudoku[x][y] = EMPTY  # deshacer
        return False

    # Trabajar sobre una copia para no modificar el original
    sudoku_copy = [row[:] for row in sudoku1]
    backtrack(sudoku_copy)

    return solutions == 1
