# Sudoku Solver - AI Assignment 05

This project implements an automated Sudoku solver using standard Artificial Intelligence techniques for Constraint Satisfaction Problems (CSPs).

## Overview

The solver reads Sudoku puzzles from text files and employs a combination of inference and search algorithms to find a valid solution. It tracks performance metrics such as the number of backtracking calls and failures.

## Features

- **Input Handling**: Reads 9x9 Sudoku grids from text files where `0` represents an empty cell.
- **CSP Modeling**: 
  - **Variables**: The 81 cells of the Sudoku grid.
  - **Domains**: Values `{1, 2, ..., 9}` for each cell.
  - **Constraints**: Standard Sudoku rules (row, column, and 3x3 box uniqueness).
- **Inference**: Uses the **AC-3 (Arc Consistency)** algorithm to prune domains before starting the search.
- **Search Algorithm**: Implements **Backtracking Search** enhanced with:
  - **MRV (Minimum Remaining Values) Heuristic**: Selects the unassigned variable with the smallest domain to minimize the branching factor.
  - **Forward Checking**: Propagates assignments to neighbors to detect early failures.

## File Structure

- `F230620_Assignment5.py`: The main Python script containing the solver logic.
- `easy.txt`, `medium.txt`, `hard.txt`, `evil.txt`: Sample Sudoku puzzles of varying difficulty levels.

## Requirements

- Python 3.x

## How to Run

To run the solver on the provided test cases, execute the following command in your terminal:

```bash
python F230620_Assignment5.py
```

The script will automatically look for the puzzle files in the same directory and print the original puzzle, the solved board, and execution statistics to the console.

## Input Format

Puzzle files should be formatted as 9 lines of 9 digits each, with no spaces between digits. Use `0` for empty cells:

```text
004030050
609400000
...
```

## Performance Metrics

The solver outputs:
- **BACKTRACK calls**: Total number of times the recursive backtracking function was called.
- **BACKTRACK failures**: Number of times the search hit a dead end and had to backtrack.
