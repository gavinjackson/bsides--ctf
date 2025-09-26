#!/usr/bin/env python3
"""
Solve a 9x9 grid optimally using the provided column bags
"""

import itertools
from collections import Counter

# Your provided column bags
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

# SKATEBOARD+CANINE constraint positions for 9x9 grid
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

def solve_9x9_with_skateboard_priority():
    """Solve 9x9 grid prioritizing SKATEBOARD+CANINE constraint"""
    
    # Create empty 9x9 grid
    grid = [['?' for _ in range(9)] for _ in range(9)]
    
    print("Solving 9x9 grid with SKATEBOARD+CANINE priority...")
    
    # First, identify which grid positions need specific letters for SKATEBOARD
    skateboard_constraints = {}
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if i < len(SKATEBOARD_CANINE):
            row, col = pos // 9, pos % 9
            required_char = SKATEBOARD_CANINE[i]
            skateboard_constraints[(row, col)] = required_char
            print(f"Position {pos} -> ({row},{col}): need '{required_char}'")
    
    print(f"\nTotal SKATEBOARD constraints: {len(skateboard_constraints)}")
    
    # Group constraints by column
    constraints_by_column = {}
    for (row, col), char in skateboard_constraints.items():
        if col not in constraints_by_column:
            constraints_by_column[col] = []
        constraints_by_column[col].append((row, char))
    
    # For each column, try to satisfy SKATEBOARD constraints + fill remaining
    column_solutions = {}
    
    for col in range(9):
        available_letters = COLUMN_BAGS[col][:]
        
        if col in constraints_by_column:
            # This column has SKATEBOARD constraints
            constraints = constraints_by_column[col]
            constrained_positions = set(row for row, _ in constraints)
            
            print(f"\nColumn {col}: {len(constraints)} SKATEBOARD constraints")
            
            # Check if we can satisfy the constraints
            can_satisfy = True
            for row, required_char in constraints:
                if required_char in available_letters:
                    available_letters.remove(required_char)
                    print(f"  Row {row}: need '{required_char}' ✓")
                else:
                    print(f"  Row {row}: need '{required_char}' ✗ (not available)")
                    can_satisfy = False
            
            if can_satisfy:
                # Apply constraints
                for row, required_char in constraints:
                    grid[row][col] = required_char
                
                # Fill remaining positions in this column with remaining letters
                remaining_positions = [r for r in range(9) if r not in constrained_positions]
                
                if len(remaining_positions) <= len(available_letters):
                    # Use first available letters for remaining positions
                    for i, row in enumerate(remaining_positions):
                        if i < len(available_letters):
                            grid[row][col] = available_letters[i]
                
                column_solutions[col] = True
                print(f"  ✓ Column {col} solved with SKATEBOARD constraints")
            else:
                print(f"  ✗ Column {col} cannot satisfy SKATEBOARD constraints")
                column_solutions[col] = False
        else:
            # No SKATEBOARD constraints, fill with first 9 letters
            print(f"\nColumn {col}: no SKATEBOARD constraints")
            for row in range(9):
                if row < len(available_letters):
                    grid[row][col] = available_letters[row]
            column_solutions[col] = True
    
    # Print result
    print(f"\n9x9 Grid result:")
    for i, row in enumerate(grid):
        print(f"Row {i}: {' '.join(row)}")
    
    # Convert to string and test SKATEBOARD constraint
    grid_string = ""
    for row in grid:
        for cell in row:
            grid_string += cell
    
    print(f"\nGrid string: '{grid_string}' (length: {len(grid_string)})")
    
    # Test SKATEBOARD constraint
    extracted = ""
    matches = 0
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if pos < len(grid_string):
            required_char = SKATEBOARD_CANINE[i]
            actual_char = grid_string[pos]
            extracted += actual_char
            if actual_char == required_char:
                matches += 1
                print(f"Pos {pos:2d}: '{actual_char}' == '{required_char}' ✓")
            else:
                print(f"Pos {pos:2d}: '{actual_char}' != '{required_char}' ✗")
    
    print(f"\nSKATEBOARD result: '{extracted}'")
    print(f"Target:            '{SKATEBOARD_CANINE[:len(extracted)]}'")
    print(f"Matches: {matches}/{len(SKATEBOARD_CANINE_POSITIONS)} ({matches/len(SKATEBOARD_CANINE_POSITIONS)*100:.1f}%)")
    
    # Check for Sudoku violations
    sudoku_valid = check_sudoku_constraints(grid)
    print(f"Sudoku constraints: {'✓' if sudoku_valid else '✗'}")
    
    return grid, matches

def check_sudoku_constraints(grid):
    """Check basic Sudoku constraints (no duplicates in rows/columns)"""
    # Check rows
    for row in grid:
        letters = [cell for cell in row if cell != '?' and cell.isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    # Check columns
    for col in range(9):
        letters = [grid[row][col] for row in range(9) if grid[row][col] != '?' and grid[row][col].isalpha()]
        if len(letters) != len(set(letters)):
            return False
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            letters = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    cell = grid[r][c]
                    if cell != '?' and cell.isalpha():
                        letters.append(cell)
            if len(letters) != len(set(letters)):
                return False
    
    return True

def print_column_sequences(grid):
    """Print the column sequences for the solution"""
    print(f"\n" + "="*60)
    print("9x9 SOLUTION - Column sequences:")
    print("="*60)
    
    for col in range(9):
        sequence = [grid[row][col] for row in range(9)]
        # Remove '?' placeholders
        sequence = [cell for cell in sequence if cell != '?']
        
        print(f"\nColumn {col+1}:")
        for i, letter in enumerate(sequence):
            print(f"  Position {i+1}: {letter}")

if __name__ == "__main__":
    grid, matches = solve_9x9_with_skateboard_priority()
    
    if matches >= 10:  # If we get most SKATEBOARD letters right
        print("\n🎉 Good solution found!")
        print_column_sequences(grid)
    else:
        print(f"\n⚠️  Partial solution - {matches} SKATEBOARD matches")
        print_column_sequences(grid)