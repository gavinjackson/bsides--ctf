#!/usr/bin/env python3
"""
Final Pensig Solver - Solve for 10/10 points by satisfying all constraints
"""

import itertools
from collections import Counter

# The actual HTML table has 116 cells total (not 126 like QUOTE)
# The scoring function works on the 116-character string from the table

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

# Target words that need to be found in the 9x9 grid (positions 35-116 of the full string)
TARGET_WORDS = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']

# SKATEBOARD+CANINE positions in the 116-character string
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

# Template structure from the HTML/JS (what's fixed vs fillable)
# This is the 116-character template that corresponds to the table structure
TEMPLATE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNR"

WIDTH = 9

def create_grid_from_template():
    """Create a grid structure from the template"""
    grid = []
    fillable_positions = []
    
    for i, char in enumerate(TEMPLATE):
        row, col = i // WIDTH, i % WIDTH
        while len(grid) <= row:
            grid.append([None] * WIDTH)
            
        if char == ' ':
            grid[row][col] = None  # Blank/unfillable cell
        elif char.isalpha() and char.isupper():
            grid[row][col] = '?'  # Fillable cell
            fillable_positions.append((row, col, char))
        else:
            grid[row][col] = char  # Fixed character
    
    return grid, fillable_positions

def get_column_requirements():
    """Get what letters are needed for each column"""
    grid, fillable_positions = create_grid_from_template()
    column_requirements = {}
    
    for row, col, required_letter in fillable_positions:
        if col not in column_requirements:
            column_requirements[col] = []
        column_requirements[col].append((row, required_letter))
    
    return column_requirements

def grid_to_string(grid):
    """Convert grid to 116-character string like the scoring function expects"""
    result = ""
    for row in grid:
        for cell in row:
            if cell is None:
                result += " "
            else:
                result += str(cell)
    return result

def find_words_in_section(grid_string, words, start_pos=35, section_size=81):
    """Find words in the 9x9 section of the grid string"""
    # Extract the 9x9 section
    section = grid_string[start_pos:start_pos + section_size]
    if len(section) != 81:
        return []
    
    # Convert to 9x9 grid
    section_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            pos = i * 9 + j
            if pos < len(section):
                row.append(section[pos])
            else:
                row.append(' ')
        section_grid.append(row)
    
    found_words = []
    
    for word in words:
        # Check all positions and directions
        for start_row in range(9):
            for start_col in range(9):
                # Check 8 directions
                directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
                
                for dr, dc in directions:
                    if check_word_at_pos(section_grid, word, start_row, start_col, dr, dc):
                        found_words.append(word)
                        break
                if word in found_words:
                    break
            if word in found_words:
                break
    
    return list(set(found_words))

def check_word_at_pos(grid, word, start_row, start_col, dr, dc):
    """Check if word exists at position in direction"""
    for i, char in enumerate(word):
        row = start_row + i * dr
        col = start_col + i * dc
        
        if row < 0 or row >= 9 or col < 0 or col >= 9:
            return False
        
        if grid[row][col] != char:
            return False
    
    return True

def check_sudoku_constraints(grid_string, start_pos=35):
    """Check sudoku constraints on the 9x9 section"""
    section = grid_string[start_pos:start_pos + 81]
    if len(section) != 81:
        return False, False, False
    
    # Convert to 9x9 grid
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            pos = i * 9 + j
            char = section[pos] if pos < len(section) else ' '
            if char != ' ' and char.isalpha():
                row.append(char)
            else:
                row.append(None)
        grid.append(row)
    
    # Check rows
    rows_valid = True
    for row in grid:
        letters = [cell for cell in row if cell is not None]
        if len(letters) != len(set(letters)):
            rows_valid = False
            break
    
    # Check columns
    cols_valid = True
    for col in range(9):
        letters = [grid[row][col] for row in range(9) if grid[row][col] is not None]
        if len(letters) != len(set(letters)):
            cols_valid = False
            break
    
    # Check 3x3 boxes
    boxes_valid = True
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            letters = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if grid[r][c] is not None:
                        letters.append(grid[r][c])
            if len(letters) != len(set(letters)):
                boxes_valid = False
                break
        if not boxes_valid:
            break
    
    return rows_valid, cols_valid, boxes_valid

def check_skateboard_canine(grid_string):
    """Check if SKATEBOARD+CANINE constraint is satisfied"""
    if len(grid_string) != 116:
        return False
    
    extracted = ""
    for pos in SKATEBOARD_CANINE_POSITIONS:
        if pos < len(grid_string):
            extracted += grid_string[pos]
        else:
            return False
    
    return extracted == SKATEBOARD_CANINE

def solve_puzzle():
    """Main solving function"""
    grid, fillable_positions = create_grid_from_template()
    column_requirements = get_column_requirements()
    
    print("Solving with all constraints...")
    print(f"Template length: {len(TEMPLATE)}")
    print(f"Fillable positions: {len(fillable_positions)}")
    
    # Show SKATEBOARD+CANINE requirements
    skateboard_constraints = {}
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos < len(TEMPLATE):
            current_char = TEMPLATE[pos]
            if current_char.isalpha() and current_char.isupper():
                # This position is fillable
                row, col = pos // WIDTH, pos % WIDTH
                skateboard_constraints[(row, col)] = required_char
                print(f"SKATEBOARD constraint: position {pos} (row {row}, col {col}) needs '{required_char}'")
    
    print(f"Total SKATEBOARD+CANINE constraints: {len(skateboard_constraints)}")
    
    # Solve using backtracking
    def backtrack(col_idx):
        if col_idx >= WIDTH:
            # Check all constraints
            grid_string = grid_to_string(grid)
            
            # Check SKATEBOARD+CANINE
            if not check_skateboard_canine(grid_string):
                return False
            
            # Check word finding
            found_words = find_words_in_section(grid_string, TARGET_WORDS)
            if len(found_words) < 4:
                return False
            
            # Check sudoku constraints
            rows_ok, cols_ok, boxes_ok = check_sudoku_constraints(grid_string)
            if not (rows_ok and cols_ok and boxes_ok):
                return False
            
            print(f"SOLUTION FOUND!")
            print(f"Found words: {found_words}")
            print(f"Sudoku valid: rows={rows_ok}, cols={cols_ok}, boxes={boxes_ok}")
            return True
        
        if col_idx not in column_requirements:
            return backtrack(col_idx + 1)
        
        positions = column_requirements[col_idx]
        available_letters = COLUMN_BAGS[col_idx][:]
        
        # Apply SKATEBOARD+CANINE constraints
        fixed_assignments = {}
        for row, required_letter in positions:
            if (row, col_idx) in skateboard_constraints:
                constraint_letter = skateboard_constraints[(row, col_idx)]
                if constraint_letter != required_letter:
                    print(f"Conflict at ({row}, {col_idx}): template needs {required_letter}, SKATEBOARD needs {constraint_letter}")
                    return False
                fixed_assignments[row] = constraint_letter
                if constraint_letter in available_letters:
                    available_letters.remove(constraint_letter)
                else:
                    return False
        
        # Get remaining positions to fill
        remaining_positions = [(row, req_letter) for row, req_letter in positions 
                             if row not in fixed_assignments]
        
        if not remaining_positions:
            # All positions are fixed by SKATEBOARD constraint
            for row in fixed_assignments:
                grid[row][col_idx] = fixed_assignments[row]
            result = backtrack(col_idx + 1)
            # Backtrack
            for row in fixed_assignments:
                grid[row][col_idx] = '?'
            return result
        
        # Check if we can satisfy remaining requirements
        remaining_letters = [req_letter for _, req_letter in remaining_positions]
        available_count = Counter(available_letters)
        needed_count = Counter(remaining_letters)
        
        for letter, count in needed_count.items():
            if available_count[letter] < count:
                return False
        
        # Try all valid arrangements
        for arrangement in itertools.permutations(available_letters, len(remaining_positions)):
            if sorted(arrangement) == sorted(remaining_letters):
                # Apply assignment
                old_values = []
                
                # Apply fixed assignments
                for row in fixed_assignments:
                    old_values.append((row, grid[row][col_idx]))
                    grid[row][col_idx] = fixed_assignments[row]
                
                # Apply variable assignments
                for i, (row, _) in enumerate(remaining_positions):
                    old_values.append((row, grid[row][col_idx]))
                    grid[row][col_idx] = arrangement[i]
                
                if backtrack(col_idx + 1):
                    return True
                
                # Backtrack
                for row, old_val in old_values:
                    grid[row][col_idx] = old_val
        
        return False
    
    if backtrack(0):
        return grid
    else:
        print("No solution found")
        return None

def print_solution(grid):
    """Print the solution in the required format"""
    column_requirements = get_column_requirements()
    
    print("\n" + "="*60)
    print("FINAL SOLUTION - Correct sequence for each column:")
    print("="*60)
    
    for col in range(WIDTH):
        if col not in column_requirements:
            continue
            
        positions = column_requirements[col]
        print(f"\nColumn {col+1}:")
        
        sequence = []
        for row, _ in sorted(positions):
            letter = grid[row][col]
            sequence.append(letter)
        
        for i, letter in enumerate(sequence):
            print(f"  Position {i+1}: {letter}")
        
        print(f"  Full sequence: {', '.join(sequence)}")

if __name__ == "__main__":
    solution = solve_puzzle()
    if solution:
        print_solution(solution)
    else:
        print("Failed to find a solution that satisfies all constraints.")