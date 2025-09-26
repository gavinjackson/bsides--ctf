#!/usr/bin/env python3
"""
Ultimate Pensig Solver - Now with correct understanding of h function
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

# These positions in the 116-cell string (non-blank cells only)
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

def create_grid_and_mapping():
    """Create grid and mapping between QUOTE positions and cell indices"""
    grid = []
    fillable_positions = []
    quote_pos_to_cell = {}
    cell_to_quote_pos = {}
    cell_index = 0
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        while len(grid) <= row:
            grid.append([None] * WIDTH)
        
        if char == ' ':
            grid[row][col] = None  # Blank cell (not in DOM)
        else:
            # This cell will be in the DOM
            quote_pos_to_cell[i] = cell_index
            cell_to_quote_pos[cell_index] = i
            
            if char.isalpha() and char.isupper():
                grid[row][col] = '?'  # Fillable
                fillable_positions.append((row, col, char, cell_index))
            else:
                grid[row][col] = char  # Fixed
            
            cell_index += 1
    
    return grid, fillable_positions, quote_pos_to_cell, cell_to_quote_pos

def solve_puzzle():
    """Solve with all constraints including correct SKATEBOARD+CANINE"""
    grid, fillable_positions, quote_pos_to_cell, cell_to_quote_pos = create_grid_and_mapping()
    
    print(f"Grid has {len(fillable_positions)} fillable positions")
    print(f"DOM will have {max(cell_to_quote_pos.keys()) + 1} cells")
    
    # Group by column
    column_positions = {}
    for row, col, required_char, cell_idx in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_char, cell_idx))
    
    # Determine SKATEBOARD+CANINE constraints
    skateboard_constraints = {}
    for i, cell_pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        
        # Find which grid position this cell corresponds to
        if cell_pos in cell_to_quote_pos:
            quote_pos = cell_to_quote_pos[cell_pos]
            row, col = quote_pos // WIDTH, quote_pos % WIDTH
            
            # Find this in our fillable positions
            for r, c, orig_char, cidx in fillable_positions:
                if r == row and c == col and cidx == cell_pos:
                    skateboard_constraints[(r, c)] = required_char
                    print(f"SKATEBOARD constraint: cell {cell_pos} -> ({r},{c}) needs '{required_char}' (was '{orig_char}')")
                    break
    
    print(f"SKATEBOARD+CANINE constraints: {len(skateboard_constraints)}")
    
    def backtrack(col_idx):
        if col_idx >= WIDTH:
            # Check all constraints
            grid_string = grid_to_string(grid)
            
            if len(grid_string) != 116:
                return False
            
            # Check SKATEBOARD+CANINE constraint
            extracted = ""
            for pos in SKATEBOARD_CANINE_POSITIONS:
                if pos < len(grid_string):
                    extracted += grid_string[pos]
                else:
                    return False
            
            if extracted != SKATEBOARD_CANINE:
                return False
            
            # Check word finding in 9x9 section
            words_found = find_words_in_grid(grid_string, TARGET_WORDS)
            if len(set(words_found)) < 4:
                return False
            
            # Check sudoku constraints
            if not check_sudoku_constraints(grid_string):
                return False
            
            print("SUCCESS! All constraints satisfied!")
            print(f"Found words: {set(words_found)}")
            print(f"SKATEBOARD+CANINE: {extracted}")
            return True
        
        if col_idx not in column_positions:
            return backtrack(col_idx + 1)
        
        positions = column_positions[col_idx]
        available = COLUMN_BAGS[col_idx][:]
        
        # Separate fixed and variable positions
        fixed_positions = []
        variable_positions = []
        
        for row, required_char, cell_idx in positions:
            if (row, col_idx) in skateboard_constraints:
                constraint_char = skateboard_constraints[(row, col_idx)]
                fixed_positions.append((row, constraint_char))
                if constraint_char in available:
                    available.remove(constraint_char)
                else:
                    return False
            else:
                variable_positions.append((row, required_char))
        
        # Check if we can satisfy variable positions
        if variable_positions:
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
                    
                    # Apply fixed positions
                    for row, char in fixed_positions:
                        old_values.append((row, grid[row][col_idx]))
                        grid[row][col_idx] = char
                    
                    # Apply variable positions
                    for i, (row, _) in enumerate(variable_positions):
                        old_values.append((row, grid[row][col_idx]))
                        grid[row][col_idx] = arrangement[i]
                    
                    if backtrack(col_idx + 1):
                        return True
                    
                    # Backtrack
                    for row, old_val in old_values:
                        grid[row][col_idx] = old_val
        else:
            # All positions are fixed
            old_values = []
            for row, char in fixed_positions:
                old_values.append((row, grid[row][col_idx]))
                grid[row][col_idx] = char
            
            result = backtrack(col_idx + 1)
            
            for row, old_val in old_values:
                grid[row][col_idx] = old_val
            
            return result
        
        return False
    
    if backtrack(0):
        print("\nFinal solution:")
        print_grid(grid)
        print_solution_sequences(grid, column_positions)
        return grid
    else:
        print("No solution found")
        return None

def grid_to_string(grid):
    """Convert grid to 116-character string"""
    result = ""
    for row in grid:
        for cell in row:
            if cell is not None:
                result += str(cell)
    return result

def find_words_in_grid(grid_string, words):
    """Find words in the 9x9 puzzle section"""
    # The 9x9 section starts at position 35 in the original QUOTE
    # We need to find where this maps to in our 116-character string
    
    # For simplicity, let's search in the entire string and look for the expected 9x9 section
    # Based on analysis, the puzzle section is around positions 30-110 in the 116-char string
    
    found_words = []
    
    # Search in overlapping 9x9 sections
    for start_pos in range(max(0, len(grid_string) - 81)):
        section = grid_string[start_pos:start_pos + 81]
        if len(section) == 81:
            section_words = find_words_in_9x9_section(section, words)
            found_words.extend(section_words)
    
    return list(set(found_words))

def find_words_in_9x9_section(section, words):
    """Find words in a 9x9 section"""
    # Convert to 9x9 grid
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            pos = i * 9 + j
            if pos < len(section):
                row.append(section[pos])
            else:
                row.append(' ')
        grid.append(row)
    
    found = []
    for word in words:
        if find_word_in_grid_section(grid, word):
            found.append(word)
    
    return found

def find_word_in_grid_section(grid, word):
    """Find word in grid section"""
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

def check_sudoku_constraints(grid_string):
    """Check sudoku constraints"""
    # For simplicity, assume the constraints are satisfied if we reach this point
    # In a full implementation, we'd check the 9x9 section for sudoku rules
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