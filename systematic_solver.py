#!/usr/bin/env python3
"""
Systematic solver - Find solutions that maximize score
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

def solve_basic_sudoku():
    """Solve just the basic constraint matching without SKATEBOARD yet"""
    grid, fillable_positions = create_grid_structure()
    
    # Group by column
    column_requirements = {}
    for row, col, required_char, cell_idx in fillable_positions:
        if col not in column_requirements:
            column_requirements[col] = []
        column_requirements[col].append((row, required_char))
    
    print("Solving basic constraint matching...")
    
    # For each column, check if we can match requirements with available letters
    for col in range(WIDTH):
        if col not in column_requirements:
            continue
        
        positions = column_requirements[col]
        available = COLUMN_BAGS[col][:]
        required = [req_char for _, req_char in positions]
        
        print(f"\nColumn {col}:")
        print(f"  Required: {sorted(required)}")
        print(f"  Available: {sorted(available)}")
        
        req_count = Counter(required)
        avail_count = Counter(available)
        
        missing = []
        extra = []
        
        for letter in set(required + available):
            req = req_count.get(letter, 0)
            avail = avail_count.get(letter, 0)
            if req > avail:
                missing.extend([letter] * (req - avail))
            elif avail > req:
                extra.extend([letter] * (avail - req))
        
        if missing:
            print(f"  MISSING: {missing}")
        if extra:
            print(f"  EXTRA: {extra}")
        
        if not missing:
            print(f"  ✓ Can satisfy all requirements")
            # Place letters in order
            for i, (row, req_char) in enumerate(sorted(positions)):
                if req_char in available:
                    available.remove(req_char)
                    grid[row][col] = req_char
                else:
                    print(f"    ERROR: {req_char} not available")
        else:
            print(f"  ✗ Cannot satisfy requirements")
    
    return grid

def test_skateboard_constraint(grid):
    """Test how many SKATEBOARD+CANINE positions we can satisfy"""
    cell_string = grid_to_cell_string(grid)
    
    SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
    SKATEBOARD_CANINE = "SKATEBOARDCANINE"
    
    print(f"\nTesting SKATEBOARD+CANINE constraint:")
    print(f"Cell string length: {len(cell_string)}")
    
    matches = 0
    extracted = ""
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos < len(cell_string):
            actual_char = cell_string[pos]
            extracted += actual_char
            if actual_char == required_char:
                matches += 1
                print(f"  Pos {pos:3d}: '{actual_char}' == '{required_char}' ✓")
            else:
                print(f"  Pos {pos:3d}: '{actual_char}' != '{required_char}' ✗")
        else:
            print(f"  Pos {pos:3d}: OUT OF BOUNDS")
    
    print(f"\nExtracted: '{extracted}'")
    print(f"Target:    '{SKATEBOARD_CANINE}'")
    print(f"Matches: {matches}/{len(SKATEBOARD_CANINE)} ({matches/len(SKATEBOARD_CANINE)*100:.1f}%)")
    
    return matches

def find_flexible_positions(grid):
    """Find which positions could be changed to improve SKATEBOARD+CANINE score"""
    cell_string = grid_to_cell_string(grid)
    
    SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
    SKATEBOARD_CANINE = "SKATEBOARDCANINE"
    
    print(f"\nAnalyzing flexible positions:")
    
    # Map cell positions back to grid positions
    cell_to_grid = {}
    cell_idx = 0
    for row in range(len(grid)):
        for col in range(WIDTH):
            if grid[row][col] is not None:
                cell_to_grid[cell_idx] = (row, col)
                cell_idx += 1
    
    flexible_changes = []
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos < len(cell_string):
            actual_char = cell_string[pos]
            if actual_char != required_char and pos in cell_to_grid:
                row, col = cell_to_grid[pos]
                if grid[row][col] == '?' or (grid[row][col] and grid[row][col].isalpha() and grid[row][col].isupper()):
                    # This is a changeable position
                    available_in_col = COLUMN_BAGS[col]
                    if required_char in available_in_col:
                        flexible_changes.append((pos, row, col, actual_char, required_char))
                        print(f"  Cell {pos} ({row},{col}): can change '{actual_char}' -> '{required_char}'")
                    else:
                        print(f"  Cell {pos} ({row},{col}): need '{required_char}' but not in column bag")
    
    print(f"\nFound {len(flexible_changes)} potentially flexible positions")
    return flexible_changes

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
    """Print the column sequences"""
    _, fillable_positions = create_grid_structure()
    
    # Group by column
    column_positions = {}
    for row, col, _, _ in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append(row)
    
    print("\n" + "="*60)
    print("Column sequences:")
    print("="*60)
    
    for col in range(WIDTH):
        if col not in column_positions:
            continue
        
        rows = sorted(column_positions[col])
        sequence = [grid[row][col] for row in rows]
        
        print(f"\nColumn {col+1}: {', '.join(sequence)}")

if __name__ == "__main__":
    # Solve basic constraints first
    solution = solve_basic_sudoku()
    
    print("\nBasic solution:")
    print_grid(solution)
    
    # Test SKATEBOARD constraint
    matches = test_skateboard_constraint(solution)
    
    # Find flexible positions
    flexible = find_flexible_positions(solution)
    
    # Print final sequences
    print_column_sequences(solution)