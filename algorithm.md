# SUDOKU GENERATOR

This document describes the implementation of a Sudoku generator.
It explains how the data is handled and provides detailed descriptions of each function in the system.
All explanations are presented in both pseudocode and Python.

## **Functions description**
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
## `count_used_squares(sudoku)`
### **Description**
This function takes a sudoku as input and returns the number of squares that have a number.
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

