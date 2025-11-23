import time
from solver import solve_sudoku
from generator import _get_playable_sudoku

def main():
    start = time.time()
    new, states = _get_playable_sudoku(1)
    result, solution, record = solve_sudoku(new)
    if not result:
        print("This sudoku dont have a solution")
    print(states)
    # print_sudoku(states)
    finish = time.time()
    print(finish - start)