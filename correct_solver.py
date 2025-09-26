#!/usr/bin/env python3
"""
Correct Pensig Solver - Understanding the real structure
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

TARGET_WORDS = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

def create_cell_mapping():
    """Create mapping between QUOTE positions and cell indices in the 116-cell string"""
    quote_to_cell = {}
    cell_to_quote = {}
    cell_index = 0
    
    for i, char in enumerate(QUOTE):
        if char != ' ':  # Non-blank cells
            quote_to_cell[i] = cell_index
            cell_to_quote[cell_index] = i
            cell_index += 1
    
    return quote_to_cell, cell_to_quote

def get_grid_structure():
    """Get the grid structure with fillable positions"""
    rows = []
    fillable_positions = []
    quote_to_cell, cell_to_quote = create_cell_mapping()
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        while len(rows) <= row:
            rows.append([])
        
        if char == ' ':
            rows[row].append(None)  # Blank cell
        elif char.isalpha() and char.isupper():
            rows[row].append('?')  # Fillable
            fillable_positions.append((row, col, char, quote_to_cell[i]))
        else:
            rows[row].append(char)  # Fixed
    
    return rows, fillable_positions

def grid_to_string(grid):
    """Convert grid to the 116-character string that scoring function expects"""
    result = ""
    for row in grid:
        for cell in row:
            if cell is not None:  # Skip blank cells
                result += str(cell)
    return result

def solve_puzzle():
    """Solve the puzzle with all constraints"""
    grid, fillable_positions = get_grid_structure()
    quote_to_cell, cell_to_quote = create_cell_mapping()
    
    print(f"Grid structure: {len(grid)} rows")
    print(f"Fillable positions: {len(fillable_positions)}")
    
    # Group fillable positions by column
    column_positions = {}
    for row, col, required_char, cell_idx in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_char, cell_idx))
    
    # Determine SKATEBOARD+CANINE constraints
    skateboard_constraints = {}
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos in quote_to_cell:
            cell_idx = quote_to_cell[pos]
            # Find which row/col this corresponds to
            for row, col, orig_char, cidx in fillable_positions:
                if cidx == cell_idx:
                    skateboard_constraints[(row, col)] = required_char
                    print(f"SKATEBOARD constraint: pos {pos} -> cell {cell_idx} -> ({row},{col}) needs '{required_char}' (was '{orig_char}')")
                    break
    
    print(f"SKATEBOARD+CANINE constraints: {len(skateboard_constraints)}")
    
    def backtrack(col_idx):
        if col_idx >= WIDTH:
            # Verify all constraints
            grid_string = grid_to_string(grid)
            
            if len(grid_string) != 116:
                return False
            
            # Check SKATEBOARD+CANINE
            extracted = ""
            for pos in SKATEBOARD_CANINE_POSITIONS:
                if pos in quote_to_cell:
                    cell_idx = quote_to_cell[pos]
                    if cell_idx < len(grid_string):
                        extracted += grid_string[cell_idx]
                    else:
                        return False
                else:
                    # Position is a space in original QUOTE, this breaks the constraint
                    return False
            
            if extracted != SKATEBOARD_CANINE:
                return False
            
            # Check word finding in the 9x9 section (positions 35-116 in QUOTE = cells ??? in string)
            # First find where the 9x9 section starts in the cell string
            start_cell = None
            if 35 in quote_to_cell:
                start_cell = quote_to_cell[35]
            
            if start_cell is not None:
                section = grid_string[start_cell:start_cell+81]
                if len(section) == 81:
                    words_found = find_words_in_9x9(section, TARGET_WORDS)
                    if len(set(words_found)) < 4:
                        return False
            
            # Check Sudoku constraints
            if not check_sudoku_in_section(grid_string, start_cell):
                return False
            
            print("SUCCESS! All constraints satisfied!")
            return True
        
        if col_idx not in column_positions:
            return backtrack(col_idx + 1)
        
        positions = column_positions[col_idx]
        available = COLUMN_BAGS[col_idx][:]
        
        # Apply SKATEBOARD constraints
        fixed_positions = []
        variable_positions = []
        
        for row, required_char, cell_idx in positions:
            if (row, col_idx) in skateboard_constraints:
                constraint_char = skateboard_constraints[(row, col_idx)]
                if constraint_char != required_char:
                    print(f"CONFLICT at ({row},{col_idx}): need {required_char} but SKATEBOARD needs {constraint_char}")
                    return False
                fixed_positions.append((row, constraint_char))
                if constraint_char in available:
                    available.remove(constraint_char)
                else:
                    return False
            else:
                variable_positions.append((row, required_char))
        
        if not variable_positions:
            # All positions fixed
            for row, char in fixed_positions:
                grid[row][col_idx] = char
            result = backtrack(col_idx + 1)
            for row, char in fixed_positions:
                grid[row][col_idx] = '?'
            return result
        
        # Check if we can satisfy variable positions
        var_letters = [req_char for _, req_char in variable_positions]
        var_count = Counter(var_letters)
        avail_count = Counter(available)
        
        for letter, count in var_count.items():
            if avail_count[letter] < count:
                return False
        
        # Try arrangements
        for arrangement in itertools.permutations(available, len(variable_positions)):
            if sorted(arrangement) == sorted(var_letters):
                # Apply assignment
                old_values = []
                
                for row, char in fixed_positions:
                    old_values.append((row, grid[row][col_idx]))
                    grid[row][col_idx] = char
                
                for i, (row, _) in enumerate(variable_positions):
                    old_values.append((row, grid[row][col_idx]))
                    grid[row][col_idx] = arrangement[i]
                
                if backtrack(col_idx + 1):
                    return True
                
                # Backtrack
                for row, old_val in old_values:
                    grid[row][col_idx] = old_val
        
        return False
    
    if backtrack(0):
        print("\nFinal grid:")
        print_grid(grid)
        print_solution_sequences(grid, column_positions)
        return True
    else:
        print("No solution found")
        return False

def find_words_in_9x9(section, words):
    """Find words in 9x9 section"""
    if len(section) != 81:
        return []
    
    # Convert to 9x9 grid
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            pos = i * 9 + j
            row.append(section[pos])
        grid.append(row)
    
    found = []
    for word in words:
        if find_word_in_grid(grid, word):
            found.append(word)
    return found

def find_word_in_grid(grid, word):
    """Find word in grid in any direction"""
    for row in range(9):
        for col in range(9):
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            for dr, dc in directions:
                if check_word_at_position(grid, word, row, col, dr, dc):
                    return True
    return False

def check_word_at_position(grid, word, start_row, start_col, dr, dc):
    """Check if word exists at position"""
    for i, char in enumerate(word):
        row = start_row + i * dr
        col = start_col + i * dc
        if row < 0 or row >= 9 or col < 0 or col >= 9:
            return False
        if grid[row][col] != char:
            return False
    return True

def check_sudoku_in_section(grid_string, start_pos):
    """Check sudoku constraints in 9x9 section"""
    if start_pos is None:
        return False
    
    section = grid_string[start_pos:start_pos+81]
    if len(section) != 81:
        return False
    
    # Convert to 9x9 and check constraints
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            pos = i * 9 + j
            char = section[pos]
            if char.isalpha():
                row.append(char)
            else:
                row.append(None)
        grid.append(row)
    
    # Check rows, columns, boxes
    for i in range(9):
        # Check row
        row_letters = [grid[i][j] for j in range(9) if grid[i][j] is not None]
        if len(row_letters) != len(set(row_letters)):
            return False
        
        # Check column
        col_letters = [grid[j][i] for j in range(9) if grid[j][i] is not None]
        if len(col_letters) != len(set(col_letters)):
            return False
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_letters = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if grid[r][c] is not None:
                        box_letters.append(grid[r][c])
            if len(box_letters) != len(set(box_letters)):
                return False
    
    return True

def print_grid(grid):
    """Print grid"""
    for i, row in enumerate(grid):
        cells = []
        for cell in row:
            if cell is None:
                cells.append('.')
            else:
                cells.append(str(cell))
        print(f"Row {i+1:2d}: {' '.join(cells)}")

def print_solution_sequences(grid, column_positions):
    """Print column sequences"""
    print("\n" + "="*60)
    print("SOLUTION - Correct sequence for each column:")
    print("="*60)
    
    for col in range(WIDTH):
        if col not in column_positions:
            continue
        
        positions = column_positions[col]
        print(f"\nColumn {col+1}:")
        
        sequence = []
        for row, _, _ in sorted(positions):
            letter = grid[row][col]
            sequence.append(letter)
        
        for i, letter in enumerate(sequence):
            print(f"  Position {i+1}: {letter}")

if __name__ == "__main__":
    solve_puzzle()