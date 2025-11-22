# SUDOKU GENERATOR

This document describes the implementation of a Sudoku generator.
It explains how the data is handled and provides detailed descriptions of each function in the system.
All explanations are presented in both pseudocode and Python.

## **Introduction**
### Formal definition of sudoku
> **“A Sudoku puzzle is represented by a 9×9 grid, which comprises nine 3×3 sub-grids (also called boxes). Some of the entries in the grid are filled with numbers from 1 to 9, whereas other entries are left blank.”**  
> *(Lynce & Ouaknine, 2006, p. 1)*

A sudoku is a matrix 9x9 that have 9 sub-matrices (boxes), this matrix to be a valid sudoku need to meet the next requirements:
- There can only be one number in each square.
- There has to be all the numbers from 1 to 9 (Inclusive) in every row, column and box.
- Can only exist one solution to a given sudoku .

### **How to solve a sudoku**
There are a lot of tecniches to solve a sudoku for a human, such as:
- Single candidat
- Single position
- Pointing pairs
- Box line reduction

However for a machine solve a sudoku its pretty different (at least this aproach), we could use brute force but its theres actually a lot of different position to calculate, so insted of just brute force a more efficent method named **backtracking** is used instead.

### **Backtracking**
> **“Backtracking is a depth–first search method that tries possible choices one at a time and abandons them (“backtracks”) as soon as it is determined that they cannot lead to a valid solution.”**.        
> — Knuth, 2000, p. 4

The **bactracking** is a useful tool when it comes to solve sudoku, we can aply it to try the numbers a *EMPTY* square can have and determinate whic one is correct, in order to achive that, the algorithm first need to coninue checking the posibilities on other *EMPTY* squares.
This is an example of how it works:

**Pseudocode**
1. If the *base case*  is met, return `True`
1. Get the next target
1. Get the options the algorithm have
1. Set the initial state to the first option on the target
1. Recall the function with the updated sate
1. If the recall return True, return `True` 
1. Discard the option and return to step 4 if still options, else
1. Reset the current state to the initial state and return `False`
This algorithm is used to **Solve sudokus** and is implemented with the function
## **Functions description**
[_solve_sudoku](#solve_sudokusudoku-recordnone)

This sections present a detailed explanation of each function used on this implementation.


Each function present:
1. Description
1. Input requieried
1. Output
1. Pseudocode
1. Python implementation.
## `get_options(sudoku, position)`

### **Description**
This function takes a sudoku and a position and return all the possible numbers the square can take

### **Arguments**
- **Sudoku** : The board that its going to be used to check for every number its a matrix
- **Position** : The position that its going to be checked, it has to be a tuple (x, y)

### **Output**
- **Options** A list that contains all the possible values the square can take

### **Pseudocode**

1. Create a set `values` that contains the numbers from 1 to 9
1. Let `(x, y)` be the given position
2. For `i` from `0` to `9` do:
    - if `sudoku[i][y]` is not `None`, remove `sudoku[i][y]`
    - if `sudoku[x][i]` is not `None`, remove `sudoku[x][i]`

3. Let `a = (x // 3) * 3`
4. Let `b = (y // 3) * 3`
5. For `row` from `a` to `a + 3`, do:
    - For `column` from `b` to `b + 3` do:
        - If `sudoku[row][column]` is not `None`, remove `sudoku[row][column]` from values

6. Return values converted to a list

### **Implementation in python**
```python
def get_possible_options(sudoku: list[list] , position: tuple[int]) -> list[int]:
    x, y = position
    values = {k for k in range(1 ,9)}
    for aux in range(9):
        values -= {sudoku[aux][y], sudoku[x][aux]}
    a = (x // 3) * 3
    b = (y // 3) * 3
    for row in range(a, a + 3):
        for column in range(b, b + 3):
            if sudoku[row][column]:
                values -= {sudoku[row][column]}
    return list(values)
```

## `get_the_next_target(sudoku)`
### **Description**
This function takes a board of sudoku and returns the position `(x, y)` of a `EMPTY` square.
### **Arguments**
- Sudoku with `EMPTY`squares
### **Output**
- Position in format (x, y)
### **Pseudocode**
1. Let `length = 10`
1. Let `best_option = None`
1. for `row` from `0 to 9`, do:
    - For `column`from `0 to 9` do:
       - If `not sudoku[row][column]` then:
           - Get the possibilities to `sudoku[row][column]` by `temp = get_possible_options(sudoku, (row, column))`
        
            - If the `len` of `temp` is `1`, return `(row, column)`
            - If the `len` of `temp` is `< length`, then, set `length` to `len` of `temp` and set `best_option` to `(row ,column)`
1. Return `value`

## **Implementation on python**
```python
def get_next_target(sudoku: list[list[int]]) -> tuple:
    length = 10
    best_option = None
    for row in range(9):
        for column in range(9):
            if not sudoku[row][column]:
                current = len(get_possible_options(sudoku, (row, column)))
                if current == 1:
                    return (row, column)
                if current < length:
                    length = current
                    best_option = (row, column)
    return best_option
```

## `is_filled(sudoku)`
### **Description**
This function takes a sudoku as input and returns `False` if the sudoku have a `EMPTY` square, return `True` otherwise.
### **Arguments**
- Sudoku
### **Output**
- Boolean
### **Pseudocode**
1. For `row` from 0 to 9
    - For `column` from 0 to 9
        - If `sudoku[row][column] != None`, return `False`
1. Return `True`
### **Implementation on python**
``` python 
def is_filled(sudoku) -> bool:
    for row in sudoku:
        for element in row:
            if not element:
                return False
    return True
```

## `print_sudoku(sudoku)`
### **Description**
This function takes a sudoku as input and print the sudoku in a readable way on the console.
### **Arguments**
- Sudoku
### **Output**
- No output
### **Pseudocode**
1. For `row` from 0 to 9, do:
    - For `column` from 0 to 9, do:
        - Print `sudoku[row][column]`(without a line break) 
    - Print a line break
### **Implementation on python**
``` python 
def print_sudoku(sudoku) -> None:
    for row in sudoku:
        for element in row:
            print(element, end="")
        print()
```
## `_solve_sudoku(sudoku, record=None)`
### **Description**
This function solve a given sudoku and can store all the steps that it take to solve in a list named record, return `True` if the sudoku has solution, `False` otherwise 
> [!IMPORTANT]
> This function does *modify* the original sudoku.
 
### **Arguments**
- Sudoku
### **Output**
- `True` if the sudoku has solution, `False` otherwise 
### **Pseudocode**
1. If `is_filled(sudoku)`, do:
    - If `record`, append `sudoku` to `record`
    - Return `True`
1. Let `x, y = get_next_target(sudoku)`
1. Let `options = get_options(sudoku, target)`
1. For `number in option`, do:
    - If `record`, append `sudoku` to `record`
    - Set `sudoku[x][y] = number`
    - If `_solve_sudoku(sudoku, record)`, return `True`
- Set `sudoku[x][y] = None`
- Return `False`
### **Implementation on python**
```python
def _solve_sudoku(sudoku):
    if is_filled(sudoku):
        record.append([row[:] for row in sudoku])
        return True
    x, y = get_next_target(sudoku)
    options = get_options(sudoku, (x, y))
    for k in options:
        sudoku[x][y] = k
        record.append([row[:] for row in sudoku])
        if _solve_sudoku(sudoku):
            return True
    sudoku[x][y] = None
    return False
```


## `sudoku_solver(sudoku)`
### **Description**
This function takes a sudoku as input and return True or False if it have solution, the solution, and the record 
> [!IMPORTANT]
> This function does not modify the original sudoku.
### **Arguments**
- Sudoku
### **Output**
- `True` if the sudoku has solution, `False` otherwise 
- The last step the `sudoku` got( The solution if have)
- A list with all the states the sudoku has been to get solve 
### **Pseudocode**
1. Let `record = list()`
1. Let `copy` be a copy of the given sudoku
1. Let `result = _solve_sudoku(copy, record)`
1. Return `result, copy, record`
### **Implementation on python**
``` python 
def solve_sudoku(sudoku):
    record = []
    #create a copy of the given sudoku
    copy = [row[:] for row in sudoku]

    result = _solve_sudoku(copy)
    return result, copy, record
```

## `has_solution(sudoku)`
### **Description**
This function takes a sudoku as input and return `True`if it has solution, return `False` otherwise
> [!IMPORTANT]
> This function does not modify the original sudoku.
### **Arguments**
- Sudoku
### **Output**
- Return `True` it the sudoku has solution, `False`otherwise
### **Pseudocode**
1. Let `copy` be a copy of the sudoku
1. Return `_solve_sudoku(copy)
### **Implementation on python**
```python 
def has_solution(sudoku1):
    sudoku = [row[:] for row in sudoku1]
    return solve_sudoku(sudoku)
```

## `count_used_squares(sudoku)`
### **Description**
This function takes a sudoku as input and returns the number of squares that have a number on it.
### **Arguments**
- Sudoku
### **Output**
- A integer that  represents the number of squares that have a number
### **Pseudocode**
1. Let `count = 0`
1. For `row` from 0 to 9, do:
    - For `column` from 0 to 9, do:
        - If `sudoku[row][column] != None`, then `count += 1`
1. Return `count`
### **Implementation on python**
```python 
def count_used_squares(sudoku):
    counter = 0
    for row in range(len(sudoku)):
        for column in range(len(sudoku)):
            if sudoku[row][column]:
                counter += 1
    return counter
```

## `random_best_target(sudoku)`
### **Description**
This function takes a sudoku, decide what are the best option to be ne next target and return one of them at random
### **Arguments**
- Sudoku
- Predicate. Can accept one of two functions:
    - `return True` if a given element exist (filled value)
    - `return True` if a given element don't exist (empty value)

### **Output**
- A postion of the sudoku that is `EMPTY`
### **Pseudocode**
1. Let `length = 10`
1. Let `best_options` be an empty `list`
1. for `row` from `0 to 9`, do:
    - For `column`from `0 to 9` do:
       - If `predicate(sudoku[row][column])` then:
           - Get the possibilities to `sudoku[row][column]` by `temp = get_possible_options(sudoku, (row, column))`
        
            - If the `len` of `temp` is `1`, return `(row, column)`
            - If the `len` of `temp` is `< length`, set `length` to `len` of `temp` and set `best_options` to a list that contains `(row ,column)`
            - If the `len` of `temp` is equal to `length`, append `(row, column)` to `best_options`
1. Let value be a random choosen element from `best_options`.
1. Return `value`
### **Implementation**
```python
def random_best_target(sudoku, predicate):
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
```
## `_generate_filled_sudoku(sudoku, record=None)``
### **Description**
1. This function takes a empty board of sudoku to convert it to a completly filled one and returns `True`
### **Arguments**
- Sudoku
- Record
### **Output**
- `True`
### **Pseudocode**
1. If `is_filled(sudoku)`, do:
    - If `record`, append `sudoku` to `record`
    - Return `True`
1. Let `row, column = random_best_target(sudoku)`
1. Let `options = get_options(sudoku, target)`
1. Let `copy`be a copy of options.
1. For _ from `0` to `len(options)` , do:
    - Let `number`be a random choosen number from `copy`
    - Set `sudoku[row][column] = number`
    - Remove `number`from `copy` 
    - If `record`, append `sudoku` to `record`
    - If `generate_filled_sudoku(sudoku, record)`, return `True`
- Set `sudoku[x][y] = None`
- Return `False`
### **Implementation on python**
```python
def _generate_filled_sudoku(sudoku, record=None):
    """
    This function takes a empty board of sudoku to convert it to a completly filled one and returns True
    """
    if is_filled(sudoku):
        if record is not None:
            record.append(sudoku)
        return True
    row, column= random_best_target(sudoku, lambda v: not v)
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
```

## **`generate_filled_sudoku()`
### **Description**
This function returns a sudoku solved
### **Arguments**
- None
### **Output**
- Returns a sudoku solved
### **Pseudocode**
1. Let `void`be a sudoku completly `EMPTY`
1. Execute `_generate_filled_sudoku(void)`
1. Return `void`
### **Implementation on python**
``` python
def generate_sudoku_filled():
    void = [[EMPTY for _ in range(9)] for _ in range(9)]
    _generate_filled_sudoku(void)
    return void
```
## `take_off_squares(sudoku, level)`
### **Description**
This function takes a sudoku and removes numbers until has less than the `level`
### **Arguments**
- Sudoku
- Level, `int` 
### **Output**
- `True``
### **Pseudocode**
1. If `count_used_squares(sudoku) < level`, do:
    - Return `True`
1. Let `row, column = random_best_target(sudoku)`
1. Let `save = sudoku[row][column]`
1. Set `sudoku[row][column] = EMPTY`
1. For _ from `0` to `len(options)` , do:
1. If `has_solution(sudoku)`, If `take_off_squares(sudoku, level)`, `return True`
1. Set `sudoku[row][column] = save`
1. Return `False`
### **Implementation on python**
```python
def take_off_squares(sudoku1, current):

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
```

## `get_playable_sudoku(level)``
### **Description**
This function creates a new sudoku ready to play based on the level.
### **Arguments**
- Level
### **Output**
- Sudoku ready to be used
### **Pseudocode**
1. Let `levels = [40, 35, 27]`
1. Let `current = levels[level]`
1. Let `sudoku = generate_filled_sudoku()`
1. `take_off_squares(sudoku, current)`
1. Return `sudoku`
### **Implementation on python**
``` python
def get_playable_sudoku(level):

    levels = [40, 35, 27]
    current = levels[level]
    sudoku = generate_filled_sudoku()
    take_off_squares(sudoku, current)

    return sudoku
```