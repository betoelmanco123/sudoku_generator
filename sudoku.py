import time, random

EMPTY = None


# check if a sudoku its all filled with numbers
def is_filled(sudoku) -> bool:
    for row in sudoku:
        for element in row:
            if not element:
                return False
    return True


# print a sudoku in a readable way
def print_sudoku(sudoku) -> None:
    for row in sudoku:
        for element in row:
            print(element, end="")
        print()


# a funtion that determinates what is the best next target on a given board
def get_next_target(sudoku: list[list[int]]) -> tuple:
    length = 10
    best_option = None
    for row in range(len(sudoku)):
        for column in range(len(sudoku)):
            # only check empty squares
            if not sudoku[row][column]:
                current = len(get_options(sudoku, (row, column)))
                # if a square can only have one number, then we inmediatly take it
                if current == 1:
                    return (row, column)
                # always looking for take the most significant value (MSV)
                if current < length:
                    length = current
                    best_option = (row, column)
    return best_option


# returns all the posibles values for a given position on a given board
def get_options(sudoku: list[list[int]], position: tuple[int, int]) -> list[int]:
    x, y = position
    values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for aux in range(len(sudoku)):
        values -= {sudoku[aux][y], sudoku[x][aux]}

    a = (x // 3) * 3
    b = (y // 3) * 3

    for row in range(a, a + 3):
        for column in range(b, b + 3):
            if sudoku[row][column]:
                values -= {sudoku[row][column]}
    return list(values)


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


# a function that returns the number of squares that are
# empty in a given sudoku
def count_used_squares(sudoku):
    counter = 0
    for row in range(len(sudoku)):
        for column in range(len(sudoku)):
            if sudoku[row][column]:
                counter += 1
    return counter


# a functions that for a given sudoku returns True if
# it has solution or False if not


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


def get_best_target_random(sudoku, predicate):
    length = 10
    options = list()
    for i in range(9):
        for j in range(9):
            if predicate(sudoku[i][j]):
                values = get_options(sudoku, (i, j))
                if len(values) < length:
                    length = len(values)
                    options = [(i, j)]
                elif len(values) == length:
                    options.append((i, j))
    return random.choice(options)


# return the position of a empty square from a given sudoku (random)
def get_next_target_random(sudoku):

    return get_best_target_random(sudoku, lambda v: not v)


# return the position of a filled square from a given sudoku (random)
def get_next_target_filled_random(sudoku):

    return get_best_target_random(sudoku, lambda v: bool(v))


def generate_sudoku_filled():

    void = [[EMPTY for _ in range(9)] for _ in range(9)]

    def _generate_sudoku_filled(sudoku):

        # base case
        if is_filled(sudoku):
            return True
        # get the target
        target = get_next_target_random(sudoku)
        x, y = target
        # get the avaiable options
        options = get_options(sudoku, target)
        # iterate over every option
        copy = options[:]
        for _ in range(len(options)):
            value = random.choice(copy)
            copy.remove(value)
            sudoku[x][y] = value

            if _generate_sudoku_filled(sudoku):
                return True
        sudoku[x][y] = EMPTY
        return False

    _generate_sudoku_filled(void)

    return void


def get_playable_sudoku(level):

    levels = [40, 35, 27]
    sudoku = generate_sudoku_filled()

    def take_off_squares(sudoku1, level):

        current = levels[level]
        # base case
        if count_used_squares(sudoku1) < current:
            return True
        # target
        target = get_next_target_filled_random(sudoku1)
        x, y = target

        save = sudoku1[x][y]

        sudoku1[x][y] = EMPTY
        if has_solution(sudoku1):
            if take_off_squares(sudoku1, level):
                return True

        sudoku1[x][y] = save
        print("get")
        return False

    take_off_squares(sudoku, level)

    return sudoku



def _solve_sudoku(sudoku, record=None):
    # base case
    if is_filled(sudoku):
        if record:
            record.append([row[:] for row in sudoku])
        return True
    x, y = get_next_target(sudoku)
    options = get_options(sudoku, (x, y))
    for number in options:
        # set the option in the sudoku
        sudoku[x][y] = number
        # save the step to the record
        if record is not None:
            record.append([row[:] for row in sudoku])
        if _solve_sudoku(sudoku, record):
            return True
    # the backtrack step
    sudoku[x][y] = EMPTY

    return False

def has_solution(sudoku1):
    sudoku = [row[:] for row in sudoku1]
    return solve_sudoku(sudoku)

def solve_sudoku(sudoku):
    # the record of the moves
    record = []
    copy = [row[:] for row in sudoku]
    result = _solve_sudoku(copy, record)
    return result, copy, record

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
