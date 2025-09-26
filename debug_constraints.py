#!/usr/bin/env python3
"""
Debug the constraint mapping
"""

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

def debug_constraints():
    """Debug the constraint mapping"""
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
    
    # Map cell indices to grid positions
    cell_to_grid = {}
    for row, col, orig_char, cell_idx in fillable_positions:
        cell_to_grid[cell_idx] = (row, col, orig_char)
    
    print("SKATEBOARD+CANINE constraint mapping:")
    print("="*50)
    
    constraints_by_column = {}
    
    for i, cell_pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if cell_pos in cell_to_grid:
            row, col, orig_char = cell_to_grid[cell_pos]
            print(f"Cell {cell_pos:3d} -> ({row:2d},{col}) needs '{required_char}' (was '{orig_char}')")
            
            if col not in constraints_by_column:
                constraints_by_column[col] = []
            constraints_by_column[col].append((row, required_char, orig_char))
        else:
            print(f"Cell {cell_pos:3d} -> NOT FOUND in fillable positions")
    
    print(f"\nConstraints by column:")
    for col in sorted(constraints_by_column.keys()):
        constraints = constraints_by_column[col]
        print(f"\nColumn {col}:")
        for row, req_char, orig_char in constraints:
            print(f"  Row {row}: need '{req_char}' (was '{orig_char}')")
    
    # Now check which columns have issues
    from collections import Counter
    
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
    
    # Get original requirements for each column
    column_requirements = {}
    for row, col, orig_char, cell_idx in fillable_positions:
        if col not in column_requirements:
            column_requirements[col] = []
        column_requirements[col].append(orig_char)
    
    print(f"\nColumn analysis:")
    for col in range(WIDTH):
        if col in column_requirements:
            orig_req = sorted(column_requirements[col])
            available = sorted(COLUMN_BAGS[col])
            
            print(f"\nColumn {col}:")
            print(f"  Original requirements: {orig_req}")
            print(f"  Available letters:     {available}")
            
            if col in constraints_by_column:
                constraints = constraints_by_column[col]
                constraint_chars = [req_char for _, req_char, _ in constraints]
                remaining_req = orig_req[:]
                
                # Remove constraint chars from original requirements
                for req_char in constraint_chars:
                    for orig_char in constraints:
                        if orig_char[1] == req_char:
                            # This position changes from orig_char[2] to req_char
                            if orig_char[2] in remaining_req:
                                remaining_req.remove(orig_char[2])
                            break
                
                # Add constraint chars
                remaining_req.extend(constraint_chars)
                remaining_req.sort()
                
                print(f"  With SKATEBOARD constraints: {remaining_req}")
                
                # Check if available can satisfy new requirements
                req_count = Counter(remaining_req)
                avail_count = Counter(available)
                
                conflicts = []
                for letter, count in req_count.items():
                    if avail_count[letter] < count:
                        conflicts.append(f"need {count} '{letter}', have {avail_count[letter]}")
                
                if conflicts:
                    print(f"  CONFLICTS: {', '.join(conflicts)}")
                else:
                    print(f"  ✓ Can satisfy all requirements")
            else:
                print(f"  No SKATEBOARD constraints")

if __name__ == "__main__":
    debug_constraints()