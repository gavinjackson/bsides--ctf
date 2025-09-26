#!/usr/bin/env python3
"""
Extract the column bags for just the 9x9 section
"""

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

# Your provided column bags (for the full 14x9 grid)
FULL_COLUMN_BAGS = [
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

def extract_9x9_requirements():
    """Extract what the 9x9 section actually needs vs what we have"""
    
    # Get the 9x9 section (starts at position 35)
    section_start = 35
    section = QUOTE[section_start:section_start + 81]
    
    # Extract fillable positions for each column in the 9x9 section
    ninex9_requirements = {}
    
    for row in range(9):
        for col in range(9):
            pos = row * 9 + col
            if pos < len(section):
                char = section[pos]
                if char.isalpha() and char.isupper():
                    if col not in ninex9_requirements:
                        ninex9_requirements[col] = []
                    ninex9_requirements[col].append(char)
    
    print("9x9 section requirements vs full column bags:")
    print("="*60)
    
    ninex9_bags = {}
    
    for col in range(9):
        if col in ninex9_requirements:
            required_9x9 = sorted(ninex9_requirements[col])
            full_bag = sorted(FULL_COLUMN_BAGS[col])
            
            print(f"\nColumn {col}:")
            print(f"  9x9 needs:    {required_9x9} ({len(required_9x9)} letters)")
            print(f"  Full bag has: {full_bag} ({len(full_bag)} letters)")
            
            # See if we can extract the 9x9 requirements from the full bag
            remaining_bag = full_bag[:]
            can_satisfy = True
            extracted_bag = []
            
            for letter in required_9x9:
                if letter in remaining_bag:
                    remaining_bag.remove(letter)
                    extracted_bag.append(letter)
                else:
                    can_satisfy = False
                    break
            
            if can_satisfy:
                print(f"  ✓ Can extract: {sorted(extracted_bag)}")
                print(f"  Remaining:     {sorted(remaining_bag)}")
                ninex9_bags[col] = sorted(extracted_bag)
            else:
                print(f"  ✗ Cannot satisfy from full bag")
        else:
            print(f"\nColumn {col}: No requirements in 9x9 section")
    
    return ninex9_bags

def solve_9x9_with_extracted_bags():
    """Try to solve with the extracted 9x9 bags"""
    ninex9_bags = extract_9x9_requirements()
    
    print(f"\n" + "="*60)
    print("Attempting to solve 9x9 with extracted bags:")
    print("="*60)
    
    # Get the 9x9 section
    section = QUOTE[35:35+81]
    
    # Create 9x9 grid
    grid = []
    fillable_positions = {}
    
    for row in range(9):
        grid_row = []
        for col in range(9):
            pos = row * 9 + col
            if pos < len(section):
                char = section[pos]
                if char == ' ':
                    grid_row.append(None)  # Space
                elif char.isalpha() and char.isupper():
                    grid_row.append('?')  # Fillable
                    if col not in fillable_positions:
                        fillable_positions[col] = []
                    fillable_positions[col].append((row, char))
                else:
                    grid_row.append(char)  # Fixed
            else:
                grid_row.append('?')
        grid.append(grid_row)
    
    # Try to fill the grid
    for col in range(9):
        if col in fillable_positions and col in ninex9_bags:
            positions = fillable_positions[col]
            available = ninex9_bags[col][:]
            
            # Simple assignment - place required letters in order
            for i, (row, required_char) in enumerate(sorted(positions)):
                if required_char in available:
                    available.remove(required_char)
                    grid[row][col] = required_char
                else:
                    print(f"ERROR: {required_char} not available in column {col}")
    
    # Print result
    print("\n9x9 Grid result:")
    for i, row in enumerate(grid):
        cells = []
        for cell in row:
            if cell is None:
                cells.append('.')
            else:
                cells.append(str(cell))
        print(f"Row {i}: {' '.join(cells)}")
    
    # Test SKATEBOARD constraint
    grid_string = ""
    for row in grid:
        for cell in row:
            if cell is not None:
                grid_string += str(cell)
    
    print(f"\n9x9 grid string: '{grid_string}' (length: {len(grid_string)})")
    
    # Check SKATEBOARD+CANINE for positions that fit in 9x9
    SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80]
    SKATEBOARD_CANINE = "SKATEBOARDCANINE"
    
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
    
    print(f"\nSKATEBOARD (partial): '{extracted}'")
    print(f"Target (partial):     '{SKATEBOARD_CANINE[:len(extracted)]}'")
    print(f"Matches: {matches}/{len(SKATEBOARD_CANINE_POSITIONS)}")
    
    return grid, ninex9_bags

if __name__ == "__main__":
    grid, bags = solve_9x9_with_extracted_bags()
    
    print(f"\nExtracted 9x9 column bags:")
    for col, bag in bags.items():
        print(f"Column {col+1}: {bag}")