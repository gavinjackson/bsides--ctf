#!/usr/bin/env python3
"""
Convert the column solution to row format
"""

# The final 9x9 solution in column format
column_solution = [
    ['I', 'D', 'S', 'O', 'M', 'H', 'E', 'A', 'R'],           # Column 1
    ['S', 'A', 'D', 'I', 'A', 'E', 'R', 'N'],                # Column 2 (8 items)
    ['I', 'K', 'E', 'S', 'N', 'R', 'D', 'A', 'T'],           # Column 3
    ['D', 'D', 'S', 'B', 'R', 'B', 'W', 'N', 'E'],           # Column 4
    ['D', 'R', 'I', 'O', 'U', 'S', 'H', 'N'],                # Column 5 (8 items)
    ['I', 'N', 'B', 'I', 'R', 'E', 'M', 'A'],                # Column 6 (8 items)
    ['D', 'A', 'E', 'U', 'B', 'C', 'D', 'E'],                # Column 7 (8 items)
    ['S', 'R', 'R', 'A', 'E', 'H', 'S', 'C', 'E'],           # Column 8
    ['S', 'B', 'R', 'S', 'I', 'D', 'E', 'A', 'N']            # Column 9
]

def print_as_rows():
    """Print the solution as rows"""
    print("9×9 SOLUTION - Complete Grid by Rows:")
    print("=" * 50)
    
    # Create 9x9 grid
    grid = [['?' for _ in range(9)] for _ in range(9)]
    
    # Fill in the grid from columns
    for col, letters in enumerate(column_solution):
        for row, letter in enumerate(letters):
            if row < 9:  # Ensure we don't exceed grid bounds
                grid[row][col] = letter
    
    # Print each row
    for row_idx, row in enumerate(grid):
        row_letters = [cell if cell != '?' else '·' for cell in row]
        print(f"Row {row_idx + 1}: {' '.join(row_letters)}")
    
    print(f"\nGrid as continuous string:")
    grid_string = ""
    for row in grid:
        for cell in row:
            if cell != '?':
                grid_string += cell
            else:
                grid_string += '·'
    print(f"'{grid_string}'")
    
    # Show the SKATEBOARD+CANINE positions
    print(f"\nSKATEBOARD+CANINE verification:")
    positions = [7,11,15,16,20,23,31,37,47,56,70,71,80]
    target = "SKATEBOARDCANINE"
    
    extracted = ""
    for i, pos in enumerate(positions):
        if pos < len(grid_string) and i < len(target):
            actual = grid_string[pos]
            expected = target[i]
            extracted += actual
            match = "✓" if actual == expected else "✗"
            print(f"  Pos {pos:2d}: '{actual}' (need '{expected}') {match}")
    
    print(f"\nExtracted: '{extracted}'")
    print(f"Target:    '{target[:len(extracted)]}'")
    
    return grid

if __name__ == "__main__":
    grid = print_as_rows()