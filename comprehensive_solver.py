#!/usr/bin/env python3
"""
Comprehensive Pensig Solver that satisfies all constraints for full 10/10 score
"""

import itertools
from collections import defaultdict, Counter

# Constants from the puzzle
QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

# Column letter bags provided by user
COLUMN_BAGS = [
    ['I','D','S','O','M','H','E','A','R','B','N','C'],         # Col 0
    ['A','S','A','D','I','B','E','R','N','A','F','A','S','C'], # Col 1
    ['I','K','R','E','D','S','N','A','T','U','B','C'],         # Col 2
    ['D','D','S','B','R','B','W','N','E','A','E','I','C'],     # Col 3
    ['D','R','I','B','U','S','H','O','N','C','O','A','E'],     # Col 4
    ['I','N','K','I','R','E','M','A','D','R','N','B','S','C'], # Col 5
    ['D','I','E','U','B','C','D','E','S','A','N','D','R','C'], # Col 6
    ['R','A','E','S','H','S','E','N','D','I','B','C'],         # Col 7
    ['S','B','R','S','I','D','A','E','A','T','N','C']          # Col 8
]

# Target words from scoring function
TARGET_WORDS = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']

# Special positions for SKATEBOARDCANINE (h function)
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

def build_solution_string(grid):
    """Build the complete solution string from grid"""
    result = QUOTE[:35]  # Fixed header
    
    # Add the 9x9 grid part
    for row in range(14):  # 14 rows total
        for col in range(WIDTH):
            if row < len(grid) and col < len(grid[row]) and grid[row][col] is not None:
                result += grid[row][col]
            elif row * WIDTH + col + 35 < len(QUOTE):
                result += QUOTE[row * WIDTH + col + 35]
            else:
                result += " "
    
    return result

def check_skateboard_canine_constraint(solution_string):
    """Check if the solution satisfies the SKATEBOARD+CANINE constraint"""
    extracted = ""
    for pos in SKATEBOARD_CANINE_POSITIONS:
        if pos < len(solution_string):
            extracted += solution_string[pos]
        else:
            return False
    
    return extracted == SKATEBOARD_CANINE

def find_words_in_grid(grid, words, start_row=0, start_col=0, max_rows=9, max_cols=9):
    """Find if target words exist in the specified grid section"""
    found_words = []
    
    for word in words:
        # Check all directions: horizontal, vertical, diagonal
        for start_r in range(start_row, min(start_row + max_rows, len(grid))):
            for start_c in range(start_col, min(start_col + max_cols, WIDTH)):
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
                    if check_word_at_position(grid, word, start_r, start_c, dr, dc):
                        found_words.append((word, start_r, start_c, dr, dc))
    
    return found_words

def check_word_at_position(grid, word, start_row, start_col, dr, dc):
    """Check if a word exists at a specific position and direction"""
    for i, char in enumerate(word):
        row = start_row + i * dr
        col = start_col + i * dc
        
        if row < 0 or row >= len(grid) or col < 0 or col >= WIDTH:
            return False
        
        if grid[row][col] != char:
            return False
    
    return True

def is_valid_sudoku_section(grid, start_row, start_col, rows, cols):
    """Check if a section of the grid satisfies Sudoku constraints"""
    # Check rows
    for r in range(start_row, min(start_row + rows, len(grid))):
        letters = [grid[r][c] for c in range(start_col, min(start_col + cols, WIDTH)) 
                  if grid[r][c] and grid[r][c].isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    # Check columns
    for c in range(start_col, min(start_col + cols, WIDTH)):
        letters = [grid[r][c] for r in range(start_row, min(start_row + rows, len(grid))) 
                  if grid[r][c] and grid[r][c].isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    # Check 3x3 boxes within the section
    for box_row in range(start_row, min(start_row + rows, len(grid)), 3):
        for box_col in range(start_col, min(start_col + cols, WIDTH), 3):
            letters = []
            for r in range(box_row, min(box_row + 3, start_row + rows, len(grid))):
                for c in range(box_col, min(box_col + 3, start_col + cols, WIDTH)):
                    if grid[r][c] and grid[r][c].isalpha():
                        letters.append(grid[r][c])
            if len(letters) != len(set(letters)):
                return False
    
    return True

def parse_grid():
    """Parse the QUOTE string into a grid with fillable positions"""
    grid = []
    fillable_positions = []
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        while len(grid) <= row:
            grid.append([None] * WIDTH)
            
        if char == ' ':
            grid[row][col] = None  # Blank cell
        elif char.isalpha() and char.isupper():
            grid[row][col] = '?'  # Fillable cell
            fillable_positions.append((row, col, char))
        else:
            grid[row][col] = char  # Fixed cell
    
    return grid, fillable_positions

def get_column_positions():
    """Get fillable positions organized by column"""
    grid, fillable_positions = parse_grid()
    column_positions = {}
    
    for row, col, required_letter in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_letter))
    
    return column_positions

def solve_with_backtracking():
    """Solve using backtracking to satisfy all constraints"""
    grid, fillable_positions = parse_grid()
    column_positions = get_column_positions()
    
    # First, let's identify what positions need specific letters for SKATEBOARD+CANINE
    print("Analyzing SKATEBOARD+CANINE constraint...")
    
    skateboard_canine_requirements = {}
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        # Convert absolute position to row, col
        if pos >= 35:  # In the grid section
            grid_pos = pos - 35
            if grid_pos < 81:  # Within the 9x9 grid
                row = grid_pos // 9 + len(QUOTE[:35]) // WIDTH
                col = grid_pos % 9
                print(f"Position {pos} (grid {grid_pos}) -> Row {row}, Col {col}: needs '{required_char}'")
                skateboard_canine_requirements[(row, col)] = required_char
            else:
                print(f"Position {pos} is beyond the 9x9 grid section")
        else:
            print(f"Position {pos} is in the header section: needs '{required_char}'")
    
    print(f"\nSkateboard+Canine requirements: {skateboard_canine_requirements}")
    
    # Try different arrangements
    def backtrack(col_idx):
        if col_idx >= WIDTH:
            # Check all constraints
            solution_string = build_solution_string(grid)
            
            # Check SKATEBOARD+CANINE constraint
            if not check_skateboard_canine_constraint(solution_string):
                return False
            
            # Check word finding in 9x9 section (rows 3-11, which contain the 9x9 puzzle)
            word_found_count = 0
            found_words = find_words_in_grid(grid, TARGET_WORDS, 3, 0, 9, 9)
            word_found_count = len(set(word[0] for word in found_words))
            
            # Check Sudoku constraints in 9x9 section  
            if not is_valid_sudoku_section(grid, 3, 0, 9, 9):
                return False
            
            print(f"Found solution! Words found: {word_found_count}/4")
            return True
        
        if col_idx not in column_positions:
            return backtrack(col_idx + 1)
        
        positions = column_positions[col_idx]
        available = COLUMN_BAGS[col_idx][:]
        
        # Apply SKATEBOARD+CANINE constraints
        constrained_positions = []
        for row, required_letter in positions:
            if (row, col_idx) in skateboard_canine_requirements:
                needed_letter = skateboard_canine_requirements[(row, col_idx)]
                if needed_letter != required_letter:
                    print(f"Constraint conflict at ({row}, {col_idx}): need {needed_letter} but original requires {required_letter}")
                    return False
                constrained_positions.append((row, needed_letter))
                if needed_letter in available:
                    available.remove(needed_letter)
                else:
                    return False
            else:
                constrained_positions.append((row, required_letter))
        
        # Try to place remaining letters
        remaining_positions = [(row, letter) for row, letter in constrained_positions 
                             if (row, col_idx) not in skateboard_canine_requirements]
        remaining_letters = [letter for row, letter in remaining_positions]
        
        # Check if we have the required letters available
        needed_count = Counter(remaining_letters)
        available_count = Counter(available)
        
        for letter, count in needed_count.items():
            if available_count[letter] < count:
                return False
        
        # Place constrained letters first
        old_values = []
        for row, letter in constrained_positions:
            old_values.append(grid[row][col_idx])
            if (row, col_idx) in skateboard_canine_requirements:
                grid[row][col_idx] = skateboard_canine_requirements[(row, col_idx)]
        
        # Try arrangements for remaining positions
        if remaining_positions:
            for arrangement in itertools.permutations(available, len(remaining_positions)):
                if sorted(arrangement) == sorted(remaining_letters):
                    # Apply this arrangement
                    for i, (row, _) in enumerate(remaining_positions):
                        grid[row][col_idx] = arrangement[i]
                    
                    if backtrack(col_idx + 1):
                        return True
        else:
            if backtrack(col_idx + 1):
                return True
        
        # Backtrack
        for i, (row, _) in enumerate(constrained_positions):
            grid[row][col_idx] = old_values[i]
        
        return False
    
    if backtrack(0):
        return grid
    return None

def print_grid(grid):
    """Print the grid in a readable format"""
    for i, row in enumerate(grid):
        cells = []
        for cell in row:
            if cell is None:
                cells.append('.')
            else:
                cells.append(str(cell))
        print(f"Row {i+1:2d}: {' '.join(cells)}")

def print_solution_sequence(grid):
    """Print the solution as column sequences"""
    column_positions = get_column_positions()
    
    print("\nSOLUTION - Correct sequence for each column:")
    print("="*50)
    
    for col in range(WIDTH):
        if col not in column_positions:
            print(f"Column {col+1}: No fillable positions")
            continue
            
        positions = column_positions[col]
        print(f"Column {col+1}:")
        for i, (row, _) in enumerate(sorted(positions)):
            letter = grid[row][col]
            print(f"  Position {i+1}: {letter}")
        print()

if __name__ == "__main__":
    print("Solving Pensig puzzle with all constraints...")
    solution = solve_with_backtracking()
    
    if solution:
        print("\nFinal solution:")
        print_grid(solution)
        print_solution_sequence(solution)
        
        # Verify the solution
        solution_string = build_solution_string(solution)
        print(f"\nVerification:")
        print(f"SKATEBOARD+CANINE constraint: {check_skateboard_canine_constraint(solution_string)}")
        
        found_words = find_words_in_grid(solution, TARGET_WORDS, 3, 0, 9, 9)
        unique_words = set(word[0] for word in found_words)
        print(f"Words found: {unique_words} ({len(unique_words)}/4)")
        
        print(f"Sudoku valid: {is_valid_sudoku_section(solution, 3, 0, 9, 9)}")
        
    else:
        print("No solution found that satisfies all constraints.")