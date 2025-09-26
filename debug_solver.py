#!/usr/bin/env python3
"""
Debug solver to understand the constraints better
"""

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

# Let's see if I can manually check what the constraints really mean
def create_cell_mapping():
    """Create mapping between QUOTE positions and cell indices"""
    quote_to_cell = {}
    cell_to_quote = {}
    cell_index = 0
    
    for i, char in enumerate(QUOTE):
        if char != ' ':  # Non-blank cells
            quote_to_cell[i] = cell_index
            cell_to_quote[cell_index] = i
            cell_index += 1
    
    return quote_to_cell, cell_to_quote

def analyze_constraints():
    """Analyze what the SKATEBOARD+CANINE constraint really means"""
    quote_to_cell, cell_to_quote = create_cell_mapping()
    
    print("SKATEBOARD+CANINE analysis:")
    print("="*50)
    
    valid_constraints = []
    invalid_constraints = []
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        print(f"Position {pos}: need '{required_char}'")
        
        if pos >= len(QUOTE):
            print(f"  ERROR: Position {pos} is beyond QUOTE length ({len(QUOTE)})")
            invalid_constraints.append((pos, required_char))
        elif QUOTE[pos] == ' ':
            print(f"  ERROR: Position {pos} is a space (unfillable)")
            invalid_constraints.append((pos, required_char))
        elif pos in quote_to_cell:
            cell_idx = quote_to_cell[pos]
            current_char = QUOTE[pos]
            if current_char.isalpha() and current_char.isupper():
                print(f"  OK: Position {pos} -> cell {cell_idx}, currently '{current_char}', need '{required_char}'")
                valid_constraints.append((pos, required_char, cell_idx, current_char))
            else:
                print(f"  FIXED: Position {pos} -> cell {cell_idx}, fixed as '{current_char}', need '{required_char}'")
                if current_char == required_char:
                    print(f"    Already matches!")
                else:
                    print(f"    CONFLICT: Cannot change fixed character")
                    invalid_constraints.append((pos, required_char))
        else:
            print(f"  ERROR: Position {pos} not in cell mapping")
            invalid_constraints.append((pos, required_char))
    
    print(f"\nSummary:")
    print(f"Valid constraints (can be changed): {len(valid_constraints)}")
    print(f"Invalid constraints (conflicts): {len(invalid_constraints)}")
    
    if invalid_constraints:
        print("\nInvalid constraints:")
        for pos, required_char in invalid_constraints:
            print(f"  Position {pos}: need '{required_char}' but cannot change")
        print("\nThis suggests the puzzle may be unsolvable with the given SKATEBOARD+CANINE constraint,")
        print("OR there's a different interpretation of the constraint.")
    
    return valid_constraints, invalid_constraints

def test_original_solution():
    """Test if the original simple solution satisfies other constraints"""
    # My original solution
    original_columns = [
        ['A', 'B', 'C', 'D', 'E', 'H', 'I', 'M', 'N', 'O', 'R', 'S'],  # Col 0
        ['A', 'A', 'A', 'A', 'B', 'C', 'D', 'E', 'F', 'I', 'N', 'R', 'S', 'S'],  # Col 1
        ['A', 'B', 'C', 'D', 'E', 'I', 'K', 'N', 'R', 'S', 'T', 'U'],  # Col 2
        ['A', 'B', 'B', 'C', 'D', 'D', 'E', 'E', 'I', 'N', 'R', 'S', 'W'],  # Col 3
        ['A', 'B', 'C', 'D', 'E', 'H', 'I', 'N', 'O', 'O', 'R', 'S', 'U'],  # Col 4
        ['A', 'B', 'C', 'D', 'E', 'I', 'I', 'K', 'M', 'N', 'N', 'R', 'R', 'S'],  # Col 5
        ['A', 'B', 'C', 'C', 'D', 'D', 'D', 'E', 'E', 'I', 'N', 'R', 'S', 'U'],  # Col 6
        ['A', 'B', 'C', 'D', 'E', 'E', 'H', 'I', 'N', 'R', 'S', 'S'],  # Col 7
        ['A', 'A', 'B', 'C', 'D', 'E', 'I', 'N', 'R', 'S', 'S', 'T']   # Col 8
    ]
    
    # Build the grid
    WIDTH = 9
    grid = []
    
    # Create grid from QUOTE template
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        while len(grid) <= row:
            grid.append([None] * WIDTH)
        
        if char == ' ':
            grid[row][col] = None
        elif char.isalpha() and char.isupper():
            grid[row][col] = '?'  # Will be filled
        else:
            grid[row][col] = char  # Fixed
    
    # Fill in the original solution
    column_pos_idx = [0] * WIDTH
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        if char.isalpha() and char.isupper():
            if col < len(original_columns) and column_pos_idx[col] < len(original_columns[col]):
                grid[row][col] = original_columns[col][column_pos_idx[col]]
                column_pos_idx[col] += 1
    
    # Convert to string for analysis
    result_string = ""
    for row in grid:
        for cell in row:
            if cell is not None:
                result_string += str(cell)
    
    print(f"\nOriginal solution analysis:")
    print(f"Result string length: {len(result_string)}")
    
    # Check SKATEBOARD+CANINE
    quote_to_cell, _ = create_cell_mapping()
    extracted = ""
    valid_extractions = 0
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos in quote_to_cell:
            cell_idx = quote_to_cell[pos]
            if cell_idx < len(result_string):
                actual_char = result_string[cell_idx]
                extracted += actual_char
                if actual_char == required_char:
                    valid_extractions += 1
                print(f"Pos {pos} -> cell {cell_idx}: '{actual_char}' (need '{required_char}') {'✓' if actual_char == required_char else '✗'}")
            else:
                extracted += "?"
                print(f"Pos {pos} -> cell {cell_idx}: OUT OF BOUNDS")
        else:
            extracted += "?"
            print(f"Pos {pos}: NOT IN CELL MAPPING")
    
    print(f"\nExtracted: '{extracted}'")
    print(f"Target:    '{SKATEBOARD_CANINE}'")
    print(f"Matches: {extracted == SKATEBOARD_CANINE}")
    print(f"Valid extractions: {valid_extractions}/{len(SKATEBOARD_CANINE_POSITIONS)}")

if __name__ == "__main__":
    valid_constraints, invalid_constraints = analyze_constraints()
    test_original_solution()