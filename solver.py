#!/usr/bin/env python3
"""
Pensig Solver - A word-based Sudoku puzzle solver
"""

import itertools
from collections import defaultdict, Counter

# Constants from the puzzle
QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9
HEIGHT = len(QUOTE) // WIDTH

# Column letter bags provided by user
COLUMN_BAGS = [
    ['I','D','S','O','M','H','E','A','R','B','N','C'],
    ['A','S','A','D','I','B','E','R','N','A','F','A','S','C'],
    ['I','K','R','E','D','S','N','A','T','U','B','C'],
    ['D','D','S','B','R','B','W','N','E','A','E','I','C'],
    ['D','R','I','B','U','S','H','O','N','C','O','A','E'],
    ['I','N','K','I','R','E','M','A','D','R','N','B','S','C'],
    ['D','I','E','U','B','C','D','E','S','A','N','D','R','C'],
    ['R','A','E','S','H','S','E','N','D','I','B','C'],
    ['S','B','R','S','I','D','A','E','A','T','N','C']
]

# Target words from scoring function
TARGET_WORDS = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED', 'SKATEBOARD', 'CANINE']

def parse_grid():
    """Parse the QUOTE string into a grid with fixed positions"""
    grid = []
    fillable_positions = []
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        if len(grid) <= row:
            grid.append([None] * WIDTH)
            
        if char == ' ':
            grid[row][col] = None  # Blank cell
        elif char.isalpha() and char.isupper():
            grid[row][col] = char  # Fillable cell
            fillable_positions.append((row, col, char))
        else:
            grid[row][col] = char  # Fixed cell
    
    return grid, fillable_positions

def get_column_requirements():
    """Get the required letters for each column based on fillable positions"""
    grid, fillable_positions = parse_grid()
    column_requirements = defaultdict(list)
    
    for row, col, expected_char in fillable_positions:
        column_requirements[col].append((row, col, expected_char))
    
    return column_requirements

def print_grid(grid):
    """Print the grid in a readable format"""
    for i, row in enumerate(grid):
        print(f"Row {i+1:2d}: {' '.join(str(cell) if cell is not None else '.' for cell in row)}")

def find_words_in_grid(grid, words):
    """Find if target words exist in the grid in any direction"""
    found_words = []
    
    for word in words:
        # Check all directions: horizontal, vertical, diagonal
        for start_row in range(HEIGHT):
            for start_col in range(WIDTH):
                # Check 8 directions
                directions = [
                    (0, 1),   # right
                    (0, -1),  # left
                    (1, 0),   # down
                    (-1, 0),  # up
                    (1, 1),   # down-right
                    (1, -1),  # down-left
                    (-1, 1),  # up-right
                    (-1, -1)  # up-left
                ]
                
                for dr, dc in directions:
                    if check_word_at_position(grid, word, start_row, start_col, dr, dc):
                        found_words.append((word, start_row, start_col, dr, dc))
    
    return found_words

def check_word_at_position(grid, word, start_row, start_col, dr, dc):
    """Check if a word exists at a specific position and direction"""
    for i, char in enumerate(word):
        row = start_row + i * dr
        col = start_col + i * dc
        
        if row < 0 or row >= HEIGHT or col < 0 or col >= WIDTH:
            return False
        
        if grid[row][col] != char:
            return False
    
    return True

def is_valid_sudoku(grid):
    """Check if the grid satisfies Sudoku constraints"""
    # Check rows
    for row in grid:
        letters = [cell for cell in row if cell and cell.isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    # Check columns
    for col in range(WIDTH):
        letters = [grid[row][col] for row in range(HEIGHT) if grid[row][col] and grid[row][col].isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    # Check 3x3 boxes
    for box_row in range(0, HEIGHT, 3):
        for box_col in range(0, WIDTH, 3):
            letters = []
            for r in range(box_row, min(box_row + 3, HEIGHT)):
                for c in range(box_col, min(box_col + 3, WIDTH)):
                    if grid[r][c] and grid[r][c].isalpha():
                        letters.append(grid[r][c])
            if len(letters) != len(set(letters)):
                return False
    
    return True

def solve_puzzle():
    """Solve the puzzle by arranging letters from column bags"""
    grid, fillable_positions = parse_grid()
    column_requirements = get_column_requirements()
    
    print("Initial grid structure:")
    print_grid(grid)
    print()
    
    print("Column requirements:")
    for col, positions in column_requirements.items():
        print(f"Column {col}: {len(positions)} positions - {[pos[1] for pos in positions]}")
        print(f"  Available letters: {COLUMN_BAGS[col]}")
        print(f"  Need to place: {sorted([pos[1] for pos in positions])}")
        available_count = Counter(COLUMN_BAGS[col])
        needed_count = Counter([pos[1] for pos in positions])
        print(f"  Available vs Needed: {dict(available_count)} vs {dict(needed_count)}")
        print()
    
    # Try to solve by constraint satisfaction
    solution = solve_by_constraints(grid, fillable_positions, column_requirements)
    
    if solution:
        print("Solution found!")
        print_grid(solution)
        
        # Verify the solution
        found_words = find_words_in_grid(solution, TARGET_WORDS)
        print(f"\nFound words: {[word[0] for word in found_words]}")
        
        if is_valid_sudoku(solution):
            print("Solution satisfies Sudoku constraints!")
        else:
            print("Solution does NOT satisfy Sudoku constraints.")
            
        return solution
    else:
        print("No solution found.")
        return None

def solve_by_constraints(grid, fillable_positions, column_requirements):
    """Solve using backtracking with constraint satisfaction"""
    # Group positions by column
    columns_to_solve = {}
    for col, positions in column_requirements.items():
        columns_to_solve[col] = {
            'positions': positions,
            'available': COLUMN_BAGS[col][:]
        }
    
    # Try to solve column by column
    def backtrack(col_idx):
        if col_idx >= WIDTH:
            return True  # All columns solved
        
        if col_idx not in columns_to_solve:
            return backtrack(col_idx + 1)  # Skip columns with no fillable positions
        
        positions = columns_to_solve[col_idx]['positions']
        available = columns_to_solve[col_idx]['available'][:]
        
        # Try all permutations of available letters for this column
        needed_letters = [pos[1] for pos in positions]
        
        # Check if we have enough letters
        available_count = Counter(available)
        needed_count = Counter(needed_letters)
        
        for letter, count in needed_count.items():
            if available_count[letter] < count:
                return False  # Not enough letters available
        
        # Generate possible assignments
        for assignment in itertools.permutations(available, len(positions)):
            # Check if this assignment provides the required letters
            if sorted(assignment[:len(needed_letters)]) == sorted(needed_letters):
                # Try this assignment
                valid = True
                old_values = []
                
                for i, (row, col, expected) in enumerate(positions):
                    old_values.append(grid[row][col])
                    grid[row][col] = assignment[i]
                
                # Check if this partial solution is valid
                if is_partial_valid(grid, col_idx):
                    if backtrack(col_idx + 1):
                        return True
                
                # Backtrack
                for i, (row, col, expected) in enumerate(positions):
                    grid[row][col] = old_values[i]
        
        return False
    
    if backtrack(0):
        return grid
    return None

def is_partial_valid(grid, max_col):
    """Check if partial solution is valid up to max_col"""
    # Check rows up to max_col
    for row in range(HEIGHT):
        letters = []
        for col in range(min(max_col + 1, WIDTH)):
            if grid[row][col] and grid[row][col].isalpha():
                letters.append(grid[row][col])
        if len(letters) != len(set(letters)):
            return False
    
    # Check columns up to max_col
    for col in range(min(max_col + 1, WIDTH)):
        letters = [grid[row][col] for row in range(HEIGHT) if grid[row][col] and grid[row][col].isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    return True

if __name__ == "__main__":
    solution = solve_puzzle()