#!/usr/bin/env python3
"""
Brute Force Pensig Solver
Tries all possible combinations until all preconditions are met
"""

import hashlib
import base64
import itertools
from typing import List, Dict, Tuple, Optional, Set
import sys

class BruteForcePensigSolver:
    def __init__(self):
        self.QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
        self.WIDTH = 9
        
        # Column bags
        self.original_bags = [
            ['I','D','S','O','M','H','E','A','R','B','N','C'],
            ['A','S','A','D','I','B','E','R','N','A','F','A','S','C'],
            ['I','K','R','E','D','S','N','A','T','U','B','C'],
            ['D','D','S','B','R','B','W','N','E','A','E','I','C'],
            ['D','R','I','B','U','S','H','O','N','C','O','A','E'],
            ['I','N','K','I','R','E','M','A','D','R','N','B','S','C'],
            ['D','I','E','U','B','C','D','E','S','A','N','D','R','C'],
            ['R','A','E','S','H','S','E','N','D','I','B','C'],
            ['S','B','R','S','I','D','A','E','A','T','N','C']
        ]
        
        # Required SKATEBOARD+CANINE indices and letters
        self.required_indices = [
            (7, 'S'), (11, 'K'), (15, 'A'), (16, 'T'), (20, 'E'), (23, 'B'),
            (31, 'O'), (37, 'A'), (47, 'R'), (56, 'D'), (70, 'C'), (71, 'A'),
            (80, 'N'), (90, 'I'), (104, 'N'), (113, 'E')
        ]
        
        self.required_words = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']
        self.target_hash = 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw='
        
        # Initialize grid template
        self.grid_template = self._create_grid_template()
        self.fillable_positions = self._get_fillable_positions()
        
        print(f"Initialized solver with {len(self.fillable_positions)} fillable positions")
        
    def _create_grid_template(self):
        """Create grid template from QUOTE"""
        grid = []
        for i in range(len(self.QUOTE)):
            row = i // self.WIDTH
            col = i % self.WIDTH
            
            while len(grid) <= row:
                grid.append([None] * self.WIDTH)
            
            ch = self.QUOTE[i]
            if ch == ' ':
                grid[row][col] = None  # blank
            elif ch.isupper():
                grid[row][col] = ''    # fillable
            else:
                grid[row][col] = ch    # fixed
        
        return grid
    
    def _get_fillable_positions(self):
        """Get all fillable positions with their constraints"""
        positions = []
        for i, ch in enumerate(self.QUOTE):
            if ch.isupper():  # fillable
                row, col = i // self.WIDTH, i % self.WIDTH
                positions.append((row, col, i))
        return positions
    
    def _is_valid_placement(self, grid, row, col, letter):
        """Check if placing a letter at position is valid"""
        # Check if letter is available in column bag
        current_bags = self._get_current_bags(grid)
        if letter not in current_bags[col]:
            return False
        
        # Check sudoku constraints if in sudoku region (rows 5-13)
        if 5 <= row <= 13 and 0 <= col <= 8:
            # Make temporary placement
            original = grid[row][col]
            grid[row][col] = letter
            
            # Check row constraint
            row_letters = [grid[row][c] for c in range(9) if grid[row][c] and grid[row][c] != '']
            if len(set(row_letters)) != len(row_letters):
                grid[row][col] = original
                return False
            
            # Check column constraint
            col_letters = [grid[r][col] for r in range(5, 14) 
                          if r < len(grid) and grid[r][col] and grid[r][col] != '']
            if len(set(col_letters)) != len(col_letters):
                grid[row][col] = original
                return False
            
            # Check 3x3 box constraint
            box_r, box_c = (row - 5) // 3, col // 3
            box_letters = []
            for r in range(box_r * 3 + 5, box_r * 3 + 8):
                for c in range(box_c * 3, box_c * 3 + 3):
                    if r < len(grid) and grid[r][c] and grid[r][c] != '':
                        box_letters.append(grid[r][c])
            if len(set(box_letters)) != len(box_letters):
                grid[row][col] = original
                return False
            
            # Restore original
            grid[row][col] = original
        
        return True
    
    def _get_current_bags(self, grid):
        """Get current state of bags based on placed letters"""
        bags = [bag.copy() for bag in self.original_bags]
        
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] and grid[r][c] != '' and grid[r][c] is not None:
                    if grid[r][c] in bags[c]:
                        bags[c].remove(grid[r][c])
        
        return bags
    
    def _check_required_positions(self, grid):
        """Check if required SKATEBOARD+CANINE positions are satisfied"""
        solution_str = self._grid_to_string(grid)
        
        skateboard_canine = ''
        for idx, expected in self.required_indices:
            if idx < len(solution_str):
                skateboard_canine += solution_str[idx]
        
        return skateboard_canine == 'SKATEBOARDCANINE'
    
    def _check_words(self, grid):
        """Check if all required words are present"""
        for word in self.required_words:
            if not self._find_word_in_grid(word, grid):
                return False
        return True
    
    def _check_hash(self, grid):
        """Check if hash constraint is satisfied"""
        solution_str = self._grid_to_string(grid)
        if len(solution_str) < 35:
            return False
        
        first_35 = solution_str[:35]
        hash_obj = hashlib.sha256(first_35.encode())
        hash_b64 = base64.b64encode(hash_obj.digest()).decode()
        
        return hash_b64 == self.target_hash
    
    def _find_word_in_grid(self, word, grid):
        """Find word in grid (8 directions)"""
        directions = [(0,1), (1,0), (1,1), (1,-1), (0,-1), (-1,0), (-1,-1), (-1,1)]
        
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                for dr, dc in directions:
                    found = True
                    for i, letter in enumerate(word):
                        nr, nc = r + i * dr, c + i * dc
                        if (nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[nr]) or
                            grid[nr][nc] != letter):
                            found = False
                            break
                    if found:
                        return True
        return False
    
    def _grid_to_string(self, grid):
        """Convert grid to string"""
        result = ''
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                result += cell if cell else ' '
        return result
    
    def _check_sudoku_complete(self, grid):
        """Check if sudoku constraints are fully satisfied"""
        # Check all rows 5-13 have unique letters
        for r in range(5, 14):
            if r < len(grid):
                row_letters = [grid[r][c] for c in range(9) if grid[r][c] and grid[r][c] != '']
                if len(set(row_letters)) != len(row_letters):
                    return False
        
        # Check all columns 0-8 have unique letters
        for c in range(9):
            col_letters = [grid[r][c] for r in range(5, 14) 
                          if r < len(grid) and grid[r][c] and grid[r][c] != '']
            if len(set(col_letters)) != len(col_letters):
                return False
        
        # Check all 3x3 boxes have unique letters
        for box_r in range(3):
            for box_c in range(3):
                box_letters = []
                for r in range(box_r * 3 + 5, box_r * 3 + 8):
                    for c in range(box_c * 3, box_c * 3 + 3):
                        if r < len(grid) and grid[r][c] and grid[r][c] != '':
                            box_letters.append(grid[r][c])
                if len(set(box_letters)) != len(box_letters):
                    return False
        
        return True
    
    def _is_complete_solution(self, grid):
        """Check if grid is a complete 10/10 solution"""
        # Check all fillable positions are filled
        for row, col, _ in self.fillable_positions:
            if not grid[row][col] or grid[row][col] == '':
                return False
        
        # Check all constraints
        return (self._check_required_positions(grid) and
                self._check_words(grid) and
                self._check_hash(grid) and
                self._check_sudoku_complete(grid))
    
    def solve_backtrack(self, grid, position_index=0):
        """Backtracking solver"""
        if position_index >= len(self.fillable_positions):
            if self._is_complete_solution(grid):
                return grid
            return None
        
        row, col, _ = self.fillable_positions[position_index]
        current_bags = self._get_current_bags(grid)
        
        # Try each available letter for this position
        for letter in current_bags[col]:
            if self._is_valid_placement(grid, row, col, letter):
                # Place letter
                grid[row][col] = letter
                
                # Recurse
                result = self.solve_backtrack(grid, position_index + 1)
                if result is not None:
                    return result
                
                # Backtrack
                grid[row][col] = ''
        
        return None
    
    def solve_with_constraints(self):
        """Solve with smart constraint ordering"""
        print("🔍 Starting constraint-based solving...")
        
        # Start with grid template
        grid = [row.copy() for row in self.grid_template]
        
        # First, place required SKATEBOARD+CANINE letters where possible
        print("📍 Placing required SKATEBOARD+CANINE letters...")
        required_count = 0
        for idx, letter in self.required_indices:
            row, col = idx // self.WIDTH, idx % self.WIDTH
            
            if (row < len(grid) and col < len(grid[row]) and 
                grid[row][col] == ''):  # fillable position
                current_bags = self._get_current_bags(grid)
                if letter in current_bags[col]:
                    grid[row][col] = letter
                    required_count += 1
                    print(f"  ✓ Placed {letter} at ({row},{col})")
        
        print(f"Placed {required_count} required letters")
        
        # Try to solve with backtracking
        print("🔄 Starting backtracking search...")
        solution = self.solve_backtrack(grid)
        
        if solution:
            print("\n🎉 SOLUTION FOUND!")
            return solution
        else:
            print("\n❌ No solution found with current constraints")
            return None
    
    def print_solution(self, grid):
        """Print each row of the solution to standard out"""
        if not grid:
            print("No solution to print")
            return
        
        print("\n🎯 COMPLETE SOLUTION:")
        print("=" * 30)
        
        for r in range(len(grid)):
            row_str = ""
            for c in range(len(grid[r])):
                cell = grid[r][c]
                if cell is None:
                    row_str += "█"
                else:
                    row_str += cell
            print(f"Row {r:2d}: {row_str}")
        
        # Verify it's actually a 10/10 solution
        print("\n✅ VERIFICATION:")
        print("-" * 15)
        print(f"Hash valid: {self._check_hash(grid)}")
        print(f"Words found: {[w for w in self.required_words if self._find_word_in_grid(w, grid)]}")
        print(f"Sudoku valid: {self._check_sudoku_complete(grid)}")
        print(f"Required positions: {self._check_required_positions(grid)}")
        
        solution_str = self._grid_to_string(grid)
        skateboard_canine = ''.join(solution_str[idx] if idx < len(solution_str) else '?' 
                                   for idx, _ in self.required_indices)
        print(f"SKATEBOARD+CANINE: {skateboard_canine}")

def main():
    print("🎯 BRUTE FORCE PENSIG SOLVER")
    print("=" * 40)
    print("Trying all combinations until 10/10 solution found...")
    print()
    
    solver = BruteForcePensigSolver()
    solution = solver.solve_with_constraints()
    solver.print_solution(solution)

if __name__ == "__main__":
    main()