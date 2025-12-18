# SUDOKU GENERATOR

A Python-based **Sudoku generator and solver** that creates valid 9×9 Sudoku puzzles with **unique solutions**. The repository includes runnable scripts as well as documentation explaining the core ideas behind the implementation.

---

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [How to Play](#how-to-play)
* [Project Structure](#project-structure)
* [Notes](#notes)

---

## Requirements

This project is written in **Python 3** and depends only on a few standard libraries. Install all required dependencies with:

```bash
pip install -r requirements.txt
```

---

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/betoelmanco123/sudoku_generator.git
cd sudoku_generator
```

---

## Usage

Run the game from the command line:

```bash
python source/runner.py
```

This will launch the Sudoku game in a graphical window.

![Sudoku demonstration](/media/sudoku_game.gif)

---

## How to Play

* The game displays a **9×9 Sudoku grid**.
* Some cells are pre-filled; these values **cannot be changed**.
* Empty cells must be filled with numbers from **1 to 9**.
* Each number must appear **exactly once** in:

  * every row
  * every column
  * every 3×3 subgrid

### Controls

* **Mouse click** on a cell to select it.
* **Number keys (1–9)** to place a value in the selected cell.
* **Eraser** to clear a cell (only if it is not fixed).

### Objective

Fill the entire grid correctly. The generated puzzle is guaranteed to have **one unique solution**, so logical solving is always possible.

---

## Project Structure

```
sudoku_generator/
│
├── source/
│   ├── runner.py        # Entry point (runs the game)
│   ├── generator.py     # Sudoku generation logic
│   ├── solver.py        # Backtracking solver
│   └── board.py         # Board representation and rules
│
├── media/
│   └── sudoku_game.gif  # Gameplay demonstration
│
├── requirements.txt
└── README.md
```

---

## Notes

* The Sudoku generator uses **backtracking and constraint checking** to ensure validity.
* Puzzle generation removes values while verifying that the solution remains unique.
* The project is intended as a **learning and demonstration tool**, not a commercial game.

Feel free to explore the source code and documentation for deeper explanations of the algorithms involved.

