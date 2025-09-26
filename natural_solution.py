#!/usr/bin/env python3
"""
Create the most natural solution from column bags and see what it produces
"""

import itertools
from collections import Counter

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

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

SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]

def create_natural_solution():
    """Create the most natural solution from the column bags"""
    
    # Create grid structure
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
    
    # Group by column
    column_positions = {}
    for row, col, required_char, cell_idx in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_char))
    
    print("Creating natural solution from exact column requirements...")
    
    # Fill each column with exact requirements
    for col in range(WIDTH):
        if col in column_positions:
            positions = column_positions[col]
            available = COLUMN_BAGS[col][:]
            
            print(f"\nColumn {col}:")
            print(f"  Positions: {len(positions)}")
            
            # Check if we can satisfy exactly
            required_letters = sorted([req_char for _, req_char in positions])
            available_letters = sorted(available)
            
            print(f"  Required:  {required_letters}")
            print(f"  Available: {available_letters}")
            
            # Try to match exactly
            required_count = Counter(required_letters)
            available_count = Counter(available_letters)
            
            exact_match = (required_count == available_count)
            print(f"  Exact match: {exact_match}")
            
            if exact_match:
                # Perfect match - place letters in order
                for i, (row, req_char) in enumerate(sorted(positions)):
                    grid[row][col] = req_char
                print(f"  ✓ Filled with exact requirements")
            else:
                # Try to place as many required letters as possible
                used_letters = []
                for row, req_char in sorted(positions):
                    if req_char in available and req_char not in used_letters:
                        grid[row][col] = req_char
                        used_letters.append(req_char)
                    elif req_char in available:
                        # Need multiple of this letter
                        count_needed = required_count[req_char]
                        count_used = used_letters.count(req_char)
                        if count_used < count_needed and available_count[req_char] > count_used:
                            grid[row][col] = req_char
                            used_letters.append(req_char)
                        else:
                            # Use first available letter not yet used
                            for alt_char in available:
                                if alt_char not in used_letters or used_letters.count(alt_char) < available_count[alt_char]:
                                    grid[row][col] = alt_char
                                    used_letters.append(alt_char)
                                    break
                print(f"  ⚠ Partial match - filled with available letters")
    
    return grid

def analyze_natural_solution(grid):
    """Analyze what the natural solution produces"""
    
    # Convert to 116-character string
    grid_string = ""
    for row in grid:
        for cell in row:
            if cell is not None:
                grid_string += str(cell)
    
    print(f"\n" + "="*60)
    print("NATURAL SOLUTION ANALYSIS")
    print("="*60)
    print(f"Grid string length: {len(grid_string)}")
    print(f"Grid string: '{grid_string}'")
    
    # Check what it produces at SKATEBOARD positions
    print(f"\nWhat natural solution produces at key positions:")
    extracted = ""
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if pos < len(grid_string):
            actual_char = grid_string[pos]
            extracted += actual_char
            print(f"Pos {pos:3d}: '{actual_char}'")
    
    print(f"\nNatural string: '{extracted}'")
    print(f"Target SKATEB: 'SKATEBOARDCANINE'")
    print(f"Target REVERSE: 'ENINACDRAOBTEKS'")
    
    # Check matches with both forward and reverse
    forward_matches = 0
    reverse_matches = 0
    
    for i, char in enumerate(extracted):
        if i < len("SKATEBOARDCANINE"):
            if char == "SKATEBOARDCANINE"[i]:
                forward_matches += 1
            if char == "ENINACDRAOBTEKS"[i]:
                reverse_matches += 1
    
    print(f"\nForward matches: {forward_matches}/{len(extracted)}")
    print(f"Reverse matches: {reverse_matches}/{len(extracted)}")
    
    return grid_string, extracted

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

def print_as_rows(grid):
    """Print solution as rows"""
    print(f"\n" + "="*60)
    print("NATURAL SOLUTION - Complete Grid by Rows:")
    print("="*60)
    
    for row_idx, row in enumerate(grid):
        row_letters = [cell if cell is not None else '·' for cell in row]
        print(f"Row {row_idx + 1:2d}: {' '.join(row_letters)}")

def print_column_sequences(grid):
    """Print column sequences"""
    print(f"\n" + "="*60)
    print("NATURAL SOLUTION - Column sequences:")
    print("="*60)
    
    for col in range(WIDTH):
        sequence = []
        for row in range(len(grid)):
            if col < len(grid[row]) and grid[row][col] is not None and grid[row][col] != '?':
                sequence.append(grid[row][col])
        
        if sequence:
            print(f"\nColumn {col+1}:")
            for i, letter in enumerate(sequence):
                print(f"  Position {i+1}: {letter}")

if __name__ == "__main__":
    grid = create_natural_solution()
    print_grid(grid)
    
    grid_string, extracted = analyze_natural_solution(grid)
    
    print_as_rows(grid)
    print_column_sequences(grid)