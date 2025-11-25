import random
from utils import count_used_squares, is_filled
from solver import get_options, solve_sudoku

EMPTY = None


def random_best_target(sudoku, predicate) -> tuple[int]:
    """
    This function takes a sudoku, decide what are the best option to be ne next target and return one of them at random
    """
    # initialize a value that must be bigger than every square
    length = 10
    # a list that will store all the options
    options = list()
    # iterate over every element
    for row in range(9):
        for column in range(9):
            # if the element exist get their possible options
            if predicate(sudoku[row][column]):
                values = get_options(sudoku, (row, column))
                # if the element has less options than the current, we remplace the current with this new one
                if len(values) < length:
                    length = len(values)
                    options = [(row, column)]
                # if the element has the same number of options as the current, we added to the list
                elif len(values) == length:
                    options.append((row, column))
    # return a random choice between positons whiht the less length
    return random.choice(options)


def _generate_filled_sudoku(sudoku, record=None) -> True:
    """
    This function takes a empty board of sudoku to convert it to a completly filled one and returns True
    """
    # if the given sudoku dont have EMPTY squares then we return True
    if is_filled(sudoku):
        # store the state in the record if exist
        if record is not None:
            copy1 = [row[:] for row in sudoku]
            record.append(copy1)
        return True
    # get the best target and their options to be randomly filled
    row, column = random_best_target(sudoku, lambda v: not v)
    options = get_options(sudoku, (row, column))
    # create a copy of the list of options for the target
    copy = options[:]
    # repeat this block by the number of options the target have
    for _ in range(len(options)):
        # store the stage if exist
        if record is not None:
            copy1 = [row[:] for row in sudoku]
            record.append(copy1)
        # choose a value randomly and remove it from the copy
        value = random.choice(copy)
        copy.remove(value)
        # set the target to the choosen value
        sudoku[row][column] = value
        # if the branch return True, this branch also return True
        if _generate_filled_sudoku(sudoku, record):
            return True
    # if all the options return False then we set our target to None and return False
    sudoku[row][column] = EMPTY
    return False


def generate_filled_sudoku() -> list[list]:
    """
    This function returns a solved sudoku
    """
    # create a EMPTY sudoku
    void = [[EMPTY for _ in range(9)] for _ in range(9)]
    # fill the EMPTY sudoku
    _generate_filled_sudoku(void)
    return void


def has_solution(sudoku1) -> bool:
    """
    This function takes a sudoku as input and return `True`if it has solution, return `False` otherwise
    This function does not modify the original sudoku.
    """
    sudoku = [row[:] for row in sudoku1]
    return solve_sudoku(sudoku)


def take_off_squares(sudoku1, current, record=None) -> True:
    """
    This function takes a sudoku and removes numbers until has less than the `level`
    """
    # if the given sudoku has less squares than its supposed to then we return True
    if count_used_squares(sudoku1) < current:
        if record is not None:
            copy = [row[:] for row in sudoku1]
            record.append(copy)
        return True
    # get the best target that has a number on the square
    target = random_best_target(sudoku1, lambda v: bool(v))
    row, column = target
    # store a copy of the value on the target
    save = sudoku1[row][column]
    # set the target to EMPTY
    sudoku1[row][column] = EMPTY
    # if the sudoku still have a unique solution we recurselvy call the functions
    if record is not None:
        copy = [row[:] for row in sudoku1]
        record.append(copy)

    if has_solution(sudoku1):
        if take_off_squares(sudoku1, current, record):
            return True
    # if the new state dont have a solution, set the target to his
    # original value and return False
    sudoku1[row][column] = save
    return False


def get_playable_sudoku(level) -> list[list]:
    """
    This function takes a level as input an returns a sudoku completly ready to be played
    """
    # the levels a sudoku can have
    # easy -> 40
    # normal -> 40
    # hard -> 27
    levels = [40, 35, 27]
    current = levels[level]
    # generate a base sudoku with all the squares filled
    sudoku = generate_filled_sudoku()
    # remove random values until we reach the level
    take_off_squares(sudoku, current)

    return sudoku


def _get_playable_sudoku(level) -> list[list]:
    """
    This function takes a level as input an returns a sudoku completly ready to be played
    as well as a record with all the steps it took to create this sudoku
    """
    # the levels a sudoku can have
    # easy -> 40
    # normal -> 35
    # hard -> 27
    record = []
    levels = [40, 35, 27]
    current = levels[level]
    # generate a base sudoku with all the squares filled
    void = [[EMPTY for _ in range(9)] for _ in range(9)]
    _generate_filled_sudoku(void, record)
    # remove random values until we reach the level
    take_off_squares(void, current, record)
    return void, record
