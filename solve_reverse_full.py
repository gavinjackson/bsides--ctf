#!/usr/bin/env python3
"""
Solve the full 14x9 matrix with SKATEBOARDCANINE in reverse
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

# Original constraint positions for the 116-character string
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE_REVERSE = "ENINACDRAOBTEKS"

def create_full_grid_structure():
    """Create the full 14x9 grid structure"""
    grid = []
    fillable_positions = []
    cell_index = 0
    
    for i, char in enumerate(QUOTE):
        row, col = i // WIDTH, i % WIDTH
        while len(grid) <= row:
            grid.append([None] * WIDTH)
        
        if char == ' ':
            grid[row][col] = None  # Blank cell (not counted in 116)
        elif char.isalpha() and char.isupper():
            grid[row][col] = '?'  # Fillable
            fillable_positions.append((row, col, char, cell_index))
            cell_index += 1
        else:
            grid[row][col] = char  # Fixed character
            cell_index += 1
    
    return grid, fillable_positions

def grid_to_116_string(grid):
    """Convert grid to 116-character string (skipping blank cells)"""
    result = ""
    for row in grid:
        for cell in row:
            if cell is not None:  # Skip blank cells
                result += str(cell)
    return result

def analyze_reverse_constraint():
    """Analyze what the reverse constraint needs"""
    grid, fillable_positions = create_full_grid_structure()
    
    print("Analyzing REVERSE SKATEBOARDCANINE constraint:")
    print("=" * 60)
    print(f"Original: SKATEBOARDCANINE")
    print(f"Reverse:  {SKATEBOARD_CANINE_REVERSE}")
    print()
    
    # Map cell positions to grid coordinates
    cell_to_grid = {}
    for row, col, orig_char, cell_idx in fillable_positions:
        cell_to_grid[cell_idx] = (row, col, orig_char)
    
    # Analyze reverse constraints
    reverse_constraints = {}
    constraints_by_column = {}
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if i < len(SKATEBOARD_CANINE_REVERSE):
            required_char = SKATEBOARD_CANINE_REVERSE[i]
            if pos in cell_to_grid:
                row, col, orig_char = cell_to_grid[pos]
                reverse_constraints[(row, col)] = required_char
                
                if col not in constraints_by_column:
                    constraints_by_column[col] = []
                constraints_by_column[col].append((row, required_char, orig_char))
                
                print(f"Cell {pos:3d} -> ({row:2d},{col}): need '{required_char}' (was '{orig_char}')")
    
    print(f"\nReverse constraints by column:")
    for col in sorted(constraints_by_column.keys()):
        constraints = constraints_by_column[col]
        needed_chars = [req_char for _, req_char, _ in constraints]
        available = COLUMN_BAGS[col]
        
        print(f"\nColumn {col}:")
        print(f"  Need: {needed_chars}")
        print(f"  Have: {available}")
        
        # Check availability
        available_count = Counter(available)
        needed_count = Counter(needed_chars)
        
        missing = []
        for char, count in needed_count.items():
            if available_count[char] < count:
                missing.extend([char] * (count - available_count[char]))
        
        if missing:
            print(f"  MISSING: {missing}")
        else:
            print(f"  ✓ Can satisfy reverse constraints")
    
    return reverse_constraints, constraints_by_column

def solve_with_reverse_constraint():
    """Solve the full matrix with reverse SKATEBOARDCANINE"""
    grid, fillable_positions = create_full_grid_structure()
    reverse_constraints, constraints_by_column = analyze_reverse_constraint()
    
    print(f"\n" + "="*60)
    print("Solving with REVERSE constraint...")
    print("="*60)
    
    # Group fillable positions by column
    column_positions = {}
    for row, col, required_char, cell_idx in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append((row, required_char))
    
    # Try to solve column by column
    def solve_column(col_idx):
        if col_idx >= WIDTH:
            return True  # All columns solved
        
        if col_idx not in column_positions:
            return solve_column(col_idx + 1)
        
        positions = column_positions[col_idx]
        available = COLUMN_BAGS[col_idx][:]
        
        # Separate constrained and unconstrained positions
        constrained_positions = []
        unconstrained_positions = []
        
        for row, required_char in positions:
            if (row, col_idx) in reverse_constraints:
                constraint_char = reverse_constraints[(row, col_idx)]
                constrained_positions.append((row, constraint_char))
                if constraint_char in available:
                    available.remove(constraint_char)
                else:
                    print(f"ERROR: Column {col_idx} needs '{constraint_char}' for reverse constraint but not available")
                    return False
            else:
                unconstrained_positions.append((row, required_char))
        
        # Check if remaining letters can satisfy unconstrained positions
        if unconstrained_positions:
            uncon_letters = [req_char for _, req_char in unconstrained_positions]
            uncon_count = Counter(uncon_letters)
            avail_count = Counter(available)
            
            for letter, count in uncon_count.items():
                if avail_count[letter] < count:
                    return False
            
            # Try all valid arrangements of unconstrained positions
            for arrangement in itertools.permutations(available, len(unconstrained_positions)):
                if sorted(arrangement) == sorted(uncon_letters):
                    # Apply this arrangement
                    old_values = []
                    
                    # Set constrained positions
                    for row, char in constrained_positions:
                        old_values.append((row, grid[row][col_idx]))
                        grid[row][col_idx] = char
                    
                    # Set unconstrained positions
                    for i, (row, _) in enumerate(unconstrained_positions):
                        old_values.append((row, grid[row][col_idx]))
                        grid[row][col_idx] = arrangement[i]
                    
                    # Recurse to next column
                    if solve_column(col_idx + 1):
                        return True
                    
                    # Backtrack
                    for row, old_val in old_values:
                        grid[row][col_idx] = old_val
        else:
            # All positions are constrained
            old_values = []
            for row, char in constrained_positions:
                old_values.append((row, grid[row][col_idx]))
                grid[row][col_idx] = char
            
            result = solve_column(col_idx + 1)
            
            # Backtrack
            for row, old_val in old_values:
                grid[row][col_idx] = old_val
            
            return result
        
        return False
    
    if solve_column(0):
        return grid
    else:
        return None

def test_reverse_solution(grid):
    """Test the reverse solution"""
    grid_string = grid_to_116_string(grid)
    
    print(f"\nTesting REVERSE solution:")
    print(f"Grid string length: {len(grid_string)}")
    
    # Test reverse SKATEBOARD+CANINE
    extracted = ""
    matches = 0
    
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if i < len(SKATEBOARD_CANINE_REVERSE):
            required_char = SKATEBOARD_CANINE_REVERSE[i]
            if pos < len(grid_string):
                actual_char = grid_string[pos]
                extracted += actual_char
                if actual_char == required_char:
                    matches += 1
                    print(f"Pos {pos:3d}: '{actual_char}' == '{required_char}' ✓")
                else:
                    print(f"Pos {pos:3d}: '{actual_char}' != '{required_char}' ✗")
    
    print(f"\nReverse extracted: '{extracted}'")
    print(f"Reverse target:    '{SKATEBOARD_CANINE_REVERSE}'")
    print(f"Matches: {matches}/{len(SKATEBOARD_CANINE_POSITIONS)} ({matches/len(SKATEBOARD_CANINE_POSITIONS)*100:.1f}%)")
    
    return matches

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
    """Print column sequences"""
    _, fillable_positions = create_full_grid_structure()
    
    # Group by column
    column_positions = {}
    for row, col, _, _ in fillable_positions:
        if col not in column_positions:
            column_positions[col] = []
        column_positions[col].append(row)
    
    print(f"\n" + "="*60)
    print("REVERSE SOLUTION - Column sequences:")
    print("="*60)
    
    for col in range(WIDTH):
        if col not in column_positions:
            continue
        
        rows = sorted(column_positions[col])
        sequence = [grid[row][col] for row in rows if grid[row][col] != '?']
        
        print(f"\nColumn {col+1}:")
        for i, letter in enumerate(sequence):
            print(f"  Position {i+1}: {letter}")

if __name__ == "__main__":
    print("Attempting to solve with REVERSE SKATEBOARDCANINE...")
    
    # First analyze the constraints
    reverse_constraints, constraints_by_column = analyze_reverse_constraint()
    
    # Try to solve
    solution = solve_with_reverse_constraint()
    
    if solution:
        print(f"\n🎉 REVERSE solution found!")
        print_grid(solution)
        
        matches = test_reverse_solution(solution)
        
        if matches >= 13:
            print(f"\n🎉 Excellent! {matches} matches with reverse constraint!")
            print_column_sequences(solution)
        else:
            print(f"\n⚠️  Partial reverse solution - {matches} matches")
            print_column_sequences(solution)
    else:
        print(f"\n❌ No reverse solution found")