#!/usr/bin/env python3
"""
Targeted solver - Apply SKATEBOARD constraints to the basic solution
"""

import itertools
from collections import Counter

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

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

SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

def create_grid_structure():
    """Create the basic grid structure"""
    grid = []
    fillable_positions = []
    cell_index = 0
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        while len(grid) <= row:
            grid.append([None] * WIDTH)
        
        if char == ' ':
            grid[row][col] = None  # Blank
        elif char.isalpha() and char.isupper():
            grid[row][col] = '?'  # Fillable
            fillable_positions.append((row, col, char, cell_index))
            cell_index += 1
        else:
            grid[row][col] = char  # Fixed
            cell_index += 1
    
    return grid, fillable_positions

def grid_to_cell_string(grid):
    """Convert grid to the cell string (116 chars)"""
    result = ""
    for row in grid:
        for cell in row:
            if cell is not None:
                result += str(cell)
    return result

def get_skateboard_constraints():
    """Get the SKATEBOARD+CANINE constraints mapped to grid positions"""
    grid, fillable_positions = create_grid_structure()
    
    # Map cell indices to grid positions
    cell_to_grid = {}
    for row, col, _, cell_idx in fillable_positions:
        cell_to_grid[cell_idx] = (row, col)
    
    constraints = {}
    for i, cell_pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if cell_pos in cell_to_grid:
            row, col = cell_to_grid[cell_pos]
            constraints[(row, col)] = required_char
    
    return constraints

def solve_with_skateboard_constraints():
    """Solve applying SKATEBOARD+CANINE constraints"""
    grid, fillable_positions = create_grid_structure()
    skateboard_constraints = get_skateboard_constraints()
    
    # Group fillable positions by column
    column_positions = {}
    for row, col, required_char, cell_idx in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_char))
    
    print("Applying SKATEBOARD+CANINE constraints...")
    print(f"Total constraints: {len(skateboard_constraints)}")
    
    def solve_column(col_idx):
        if col_idx >= WIDTH:
            return True  # All columns solved
        
        if col_idx not in column_positions:
            return solve_column(col_idx + 1)
        
        positions = column_positions[col_idx]
        available = COLUMN_BAGS[col_idx][:]
        
        # Separate constrained and unconstrained positions
        constrained_positions = []
        unconstrained_positions = []
        
        for row, required_char in positions:
            if (row, col_idx) in skateboard_constraints:
                constraint_char = skateboard_constraints[(row, col_idx)]
                constrained_positions.append((row, constraint_char))
                if constraint_char in available:
                    available.remove(constraint_char)
                else:
                    print(f"ERROR: Column {col_idx} needs '{constraint_char}' but not available")
                    return False
            else:
                unconstrained_positions.append((row, required_char))
        
        # Check if remaining letters can satisfy unconstrained positions
        if unconstrained_positions:
            uncon_letters = [req_char for _, req_char in unconstrained_positions]
            uncon_count = Counter(uncon_letters)
            avail_count = Counter(available)
            
            for letter, count in uncon_count.items():
                if avail_count[letter] < count:
                    print(f"ERROR: Column {col_idx} needs {count} '{letter}' but only {avail_count[letter]} available")
                    return False
            
            # Try all valid arrangements of unconstrained positions
            for arrangement in itertools.permutations(available, len(unconstrained_positions)):
                if sorted(arrangement) == sorted(uncon_letters):
                    # Apply this arrangement
                    old_values = []
                    
                    # Set constrained positions
                    for row, char in constrained_positions:
                        old_values.append((row, grid[row][col_idx]))
                        grid[row][col_idx] = char
                    
                    # Set unconstrained positions
                    for i, (row, _) in enumerate(unconstrained_positions):
                        old_values.append((row, grid[row][col_idx]))
                        grid[row][col_idx] = arrangement[i]
                    
                    # Recurse to next column
                    if solve_column(col_idx + 1):
                        return True
                    
                    # Backtrack
                    for row, old_val in old_values:
                        grid[row][col_idx] = old_val
        else:
            # All positions are constrained
            old_values = []
            for row, char in constrained_positions:
                old_values.append((row, grid[row][col_idx]))
                grid[row][col_idx] = char
            
            result = solve_column(col_idx + 1)
            
            # Backtrack
            for row, old_val in old_values:
                grid[row][col_idx] = old_val
            
            return result
        
        return False
    
    if solve_column(0):
        return grid
    else:
        return None

def test_solution(grid):
    """Test the solution against all constraints"""
    cell_string = grid_to_cell_string(grid)
    
    print(f"\nTesting solution:")
    print(f"Cell string length: {len(cell_string)}")
    
    # Test SKATEBOARD+CANINE
    extracted = ""
    matches = 0
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos < len(cell_string):
            actual_char = cell_string[pos]
            extracted += actual_char
            if actual_char == required_char:
                matches += 1
    
    print(f"SKATEBOARD+CANINE: {extracted}")
    print(f"Target:            {SKATEBOARD_CANINE}")
    print(f"Matches: {matches}/{len(SKATEBOARD_CANINE)} ({matches/len(SKATEBOARD_CANINE)*100:.1f}%)")
    
    return matches == len(SKATEBOARD_CANINE)

def print_grid(grid):
    """Print the grid"""
    for i, row in enumerate(grid):
        cells = []
        for cell in row:
            if cell is None:
                cells.append('.')
            else:
                cells.append(str(cell))
        print(f"Row {i+1:2d}: {' '.join(cells)}")

def print_column_sequences(grid):
    """Print the final column sequences"""
    _, fillable_positions = create_grid_structure()
    
    # Group by column
    column_positions = {}
    for row, col, _, _ in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append(row)
    
    print("\n" + "="*60)
    print("FINAL SOLUTION - Column sequences:")
    print("="*60)
    
    for col in range(WIDTH):
        if col not in column_positions:
            continue
        
        rows = sorted(column_positions[col])
        sequence = [grid[row][col] for row in rows]
        
        print(f"\nColumn {col+1}:")
        for i, letter in enumerate(sequence):
            print(f"  Position {i+1}: {letter}")
        
        print(f"  Full sequence: {', '.join(sequence)}")

if __name__ == "__main__":
    solution = solve_with_skateboard_constraints()
    
    if solution:
        print("\nSolution found!")
        print_grid(solution)
        
        if test_solution(solution):
            print("\n🎉 SUCCESS! All constraints satisfied!")
            print_column_sequences(solution)
        else:
            print("\n❌ Solution found but doesn't satisfy all constraints")
    else:
        print("\n❌ No solution found")