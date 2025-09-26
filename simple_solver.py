#!/usr/bin/env python3
"""
Simple Pensig Solver - Direct approach using the given column bags
"""

# Constants from the puzzle
QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

# Column letter bags provided by user
COLUMN_BAGS = [
    ['I','D','S','O','M','H','E','A','R','B','N','C'],         # Col 1
    ['A','S','A','D','I','B','E','R','N','A','F','A','S','C'], # Col 2  
    ['I','K','R','E','D','S','N','A','T','U','B','C'],         # Col 3
    ['D','D','S','B','R','B','W','N','E','A','E','I','C'],     # Col 4
    ['D','R','I','B','U','S','H','O','N','C','O','A','E'],     # Col 5
    ['I','N','K','I','R','E','M','A','D','R','N','B','S','C'], # Col 6
    ['D','I','E','U','B','C','D','E','S','A','N','D','R','C'], # Col 7
    ['R','A','E','S','H','S','E','N','D','I','B','C'],         # Col 8
    ['S','B','R','S','I','D','A','E','A','T','N','C']          # Col 9
]

def parse_grid():
    """Parse the QUOTE string into a grid showing fixed and fillable positions"""
    grid = []
    fillable_positions = []
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        if len(grid) <= row:
            grid.append([None] * WIDTH)
            
        if char == ' ':
            grid[row][col] = None  # Blank cell (unfillable)
        elif char.isalpha() and char.isupper():
            grid[row][col] = '?'  # Fillable cell - we need to determine this
            fillable_positions.append((row, col, char))  # (row, col, required_letter)
        else:
            grid[row][col] = char  # Fixed cell
    
    return grid, fillable_positions

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

def get_column_positions():
    """Get fillable positions organized by column"""
    grid, fillable_positions = parse_grid()
    column_positions = {}
    
    for row, col, required_letter in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_letter))
    
    return column_positions

def solve_puzzle():
    """Solve the puzzle by matching letters from bags to required positions"""
    grid, fillable_positions = parse_grid()
    column_positions = get_column_positions()
    
    print("Initial grid structure:")
    print_grid(grid)
    print()
    
    # For each column, arrange the letters from the bag to match required positions
    solution_grid = [row[:] for row in grid]  # Deep copy
    
    for col in range(WIDTH):
        if col not in column_positions:
            continue
            
        positions = column_positions[col]
        available_letters = COLUMN_BAGS[col][:]
        
        print(f"Column {col}:")
        print(f"  Positions and required letters: {positions}")
        print(f"  Available letters: {available_letters}")
        
        # Extract required letters in order of rows
        required_letters = [letter for row, letter in sorted(positions)]
        
        # Check if we have exactly what we need
        from collections import Counter
        available_count = Counter(available_letters)
        required_count = Counter(required_letters)
        
        print(f"  Required: {dict(required_count)}")
        print(f"  Available: {dict(available_count)}")
        
        if available_count != required_count:
            print(f"  ERROR: Mismatch in column {col}!")
            return None
        
        # Place letters in their required positions
        for i, (row, required_letter) in enumerate(sorted(positions)):
            # Find the required letter in available letters
            if required_letter in available_letters:
                available_letters.remove(required_letter)
                solution_grid[row][col] = required_letter
            else:
                print(f"  ERROR: Cannot find {required_letter} for position ({row}, {col})")
                return None
        
        print(f"  Successfully placed letters in column {col}")
        print()
    
    print("Final solution:")
    print_grid(solution_grid)
    
    # Convert to string format for verification
    solution_string = ""
    for row in solution_grid:
        for cell in row:
            if cell is None:
                solution_string += " "
            else:
                solution_string += str(cell)
    
    print(f"\nSolution string length: {len(solution_string)}")
    print(f"Expected length: {len(QUOTE)}")
    
    return solution_grid, solution_string

def print_column_sequence():
    """Print the correct sequence for each column"""
    column_positions = get_column_positions()
    
    print("SOLUTION - Correct sequence for each column:")
    print("="*50)
    
    for col in range(WIDTH):
        if col not in column_positions:
            print(f"Column {col+1}: No fillable positions")
            continue
            
        positions = column_positions[col]
        available_letters = COLUMN_BAGS[col][:]
        
        # Extract required letters in order of rows
        required_letters = [letter for row, letter in sorted(positions)]
        
        print(f"Column {col+1}:")
        for i, letter in enumerate(required_letters):
            print(f"  Position {i+1}: {letter}")
        print()

if __name__ == "__main__":
    solution = solve_puzzle()
    if solution:
        print_column_sequence()