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
1. Pseudocodigo
1. Python implementation.
## `get_posibble_options(sudoku, position)`

### **Description**
This function takes a sudoku and a position and return all the possible numbers the square can take

### **Arguments**
- **Sudoku** : The board that its going to be used to check for every number its a matrix
- **Position** : The position that its going to be cheacked, it has to be a tuple (x, y)

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
This function takes a board of sudoku and returns the position a `EMPTY` square 
### **Arguments**
- Sudoku with `EMPTY`squares
### **Output**
- Position in format (x, y)
### **Pseudocode**
1. Let `length = 10`
1. Let `best_option = None`
1. for `row` from `0 to 9`, do:
    - For `column`from `0 to 9` do:
       - Get the possibilities to `sudoku[row][column]` by `temp = get_possible_options(sudoku, (row, column))`
        
        - If the `len` of `temp` is `1`, return `(row, column)`
        - If the `len` of `temp` is `< length`, then, set `length` to `len` of `temp` and set `best_option` to `(row ,column)`
1. Return `value`

## ** Implementation on python**
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

is_filled(sudoku)
- for i=0 to 9 
-- for j = 0 to 9
--- if sudoku on the position (i, j) is different from None
---- return False
- return true


print_sudoku(sudoku)
- for i = 0 to 9 repeat
-- for j = 0 to 9 repeat
--- print sudoku on the position (i, j) 
-- print a line break


sudoku_solver(sudoku)
- call the funcion is_filled with sudoku as argument and save the result in filled
- if filled is true then
-- call the funcion print_sudoku whit sudoku as the argument 
-- return true
- get the target from get_the_next_target()
- get the posibble numbers list to the target using possible_options() with the position and the sudoku as arguments
-for each value in the posibble numbers as number repeat:
-- set the sudoku on the target position to number
-- call the function sudoku_solver giving the updated position of the board and save the result in result
-- if result is True then return True
- set the sudoku on the target position to None
- return False


count_not_empty(sudoku)
- create a variable named count and set it value to 0
- for i = 0 to 9 repeat
-- for j = 0 to 9 repeat
--- if sudoku on position (i, j) is different to None
---- update the value of cout by adding one
- return count


