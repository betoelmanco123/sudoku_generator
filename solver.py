from utils import is_filled

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
    # determinate the top-left corner of the quadrant the position is on
    a = (row // 3) * 3
    b = (column // 3) * 3
    # iterates over every element on the same quadrant
    for row in range(a, a + 3):
        for column in range(b, b + 3):

            if sudoku[row][column]:
                # discard all the values that are on the same quadrant
                values -= {sudoku[row][column]}
    return list(values)


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
                # return (row,column) IN CASE YOU WANNA THE VISUAL WAY
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
        row, column = get_next_target(sudoku)
        options = get_options(sudoku, (row, column))

        for k in options:
            sudoku[row][column] = k
            if backtrack(sudoku):
                return True

        sudoku[row][column] = EMPTY  # deshacer
        return False

    # Trabajar sobre una copia para no modificar el original
    sudoku_copy = [row[:] for row in sudoku1]
    backtrack(sudoku_copy)

    return solutions == 1
