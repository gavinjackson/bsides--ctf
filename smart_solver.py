#!/usr/bin/env python3
"""
Smart Pensig Solver with Advanced Constraint Propagation
Uses intelligent heuristics to dramatically reduce search space
"""

import hashlib
import base64
from typing import List, Dict, Tuple, Optional, Set
import random

class SmartPensigSolver:
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
        
        # Required positions
        self.required_indices = [
            (7, 'S'), (11, 'K'), (15, 'A'), (16, 'T'), (20, 'E'), (23, 'B'),
            (31, 'O'), (37, 'A'), (47, 'R'), (56, 'D'), (70, 'C'), (71, 'A'),
            (80, 'N'), (90, 'I'), (104, 'N'), (113, 'E')
        ]
        
        self.required_words = ['SCIENCE', 'BSIDES', 'CANBERRA', 'BRAINED']
        self.target_hash = 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw='
        
        # Initialize
        self.grid_template = self._create_grid_template()
        
    def _create_grid_template(self):
        """Create grid template"""
        grid = []
        for i in range(len(self.QUOTE)):
            row = i // self.WIDTH
            col = i % self.WIDTH
            
            while len(grid) <= row:
                grid.append([None] * self.WIDTH)
            
            ch = self.QUOTE[i]
            if ch == ' ':
                grid[row][col] = None
            elif ch.isupper():
                grid[row][col] = ''
            else:
                grid[row][col] = ch
        
        return grid
    
    def solve_with_known_patterns(self):
        """Use known patterns and constraints to solve efficiently"""
        print("🧠 Using smart constraint-based solving...")
        
        # Start with most constrained approach - focus on hash first
        print("🔍 Focusing on hash constraint as primary filter...")
        
        # The hash constraint is the most restrictive - only specific first 35 chars work
        # Let's work backwards from what we know about successful puzzle patterns
        
        # Try known working patterns for CTF puzzles
        working_patterns = self._generate_smart_patterns()
        
        for i, pattern in enumerate(working_patterns):
            print(f"Testing pattern {i+1}/{len(working_patterns)}...")
            
            grid = self._apply_pattern(pattern)
            if grid and self._verify_complete_solution(grid):
                print(f"✅ Found solution with pattern {i+1}!")
                return grid
        
        print("❌ No solution found with known patterns")
        return None
    
    def _generate_smart_patterns(self):
        """Generate intelligent patterns based on constraint analysis"""
        patterns = []
        
        # Pattern 1: Start with SCIENCE placement and build around it
        pattern1 = {
            # Place SCIENCE first
            (9, 0): 'S', (9, 1): 'C', (9, 2): 'I', (9, 3): 'E', 
            (9, 4): 'N', (9, 5): 'C', (9, 6): 'E',
            
            # Required SKATEBOARD+CANINE positions
            (1, 2): 'K', (1, 6): 'A', (2, 2): 'E', (2, 5): 'B',
            (3, 4): 'O', (4, 1): 'A', (5, 2): 'R', (6, 2): 'D',
            (7, 7): 'C', (7, 8): 'A', (8, 8): 'N', (10, 0): 'I',
            (11, 5): 'N', (12, 5): 'E',
            
            # Strategic placements for hash constraint
            (0, 0): 'S', (0, 1): 'C', (0, 2): 'I', (0, 3): 'E',
            (0, 5): 'N', (0, 6): 'C',
        }
        patterns.append(pattern1)
        
        # Pattern 2: Different hash approach
        pattern2 = {
            # Different first row to try different hash
            (0, 0): 'B', (0, 1): 'S', (0, 2): 'I', (0, 3): 'D',
            (0, 5): 'E', (0, 6): 'S',
            
            # Still place required positions
            (1, 2): 'K', (1, 6): 'A', (2, 2): 'E', (2, 5): 'B',
            (3, 4): 'O', (4, 1): 'A', (5, 2): 'R', (6, 2): 'D',
            (7, 7): 'C', (7, 8): 'A', (8, 8): 'N', (10, 0): 'I',
            (11, 5): 'N', (12, 5): 'E',
            
            # SCIENCE elsewhere
            (9, 0): 'S', (9, 1): 'C', (9, 2): 'I', (9, 3): 'E', 
            (9, 4): 'N', (9, 5): 'C', (9, 6): 'E',
        }
        patterns.append(pattern2)
        
        # Pattern 3: Focus on making words findable
        pattern3 = {
            # Required positions
            (1, 2): 'K', (1, 6): 'A', (2, 2): 'E', (2, 5): 'B',
            (3, 4): 'O', (4, 1): 'A', (5, 2): 'R', (6, 2): 'D',
            (7, 7): 'C', (7, 8): 'A', (8, 8): 'N', (10, 0): 'I',
            (11, 5): 'N', (12, 5): 'E',
            
            # Try to place BSIDES vertically
            (8, 7): 'B', (9, 7): 'S', (10, 7): 'I', (11, 7): 'D', (12, 7): 'E', (13, 7): 'S',
            
            # SCIENCE horizontally  
            (9, 0): 'S', (9, 1): 'C', (9, 2): 'I', (9, 3): 'E', 
            (9, 4): 'N', (9, 5): 'C', (9, 6): 'E',
        }
        patterns.append(pattern3)
        
        return patterns
    
    def _apply_pattern(self, pattern):
        """Apply a pattern to create a grid, then try to complete it"""
        grid = [row.copy() for row in self.grid_template]
        
        # Apply the pattern
        for (row, col), letter in pattern.items():
            if (row < len(grid) and col < len(grid[row]) and 
                grid[row][col] == ''):  # fillable position
                
                # Check if letter is available
                current_bags = self._get_current_bags(grid)
                if letter in current_bags[col]:
                    grid[row][col] = letter
                else:
                    print(f"  Letter {letter} not available for ({row},{col})")
                    return None
        
        # Now try to complete the grid intelligently
        return self._complete_grid_intelligently(grid)
    
    def _complete_grid_intelligently(self, grid):
        """Complete the grid using intelligent strategies"""
        # Get all unfilled positions
        unfilled = []
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == '':
                    unfilled.append((r, c))
        
        print(f"  Need to fill {len(unfilled)} positions")
        
        # Try to fill each position with available letters
        max_attempts = 1000
        for attempt in range(max_attempts):
            test_grid = [row.copy() for row in grid]
            success = True
            
            for r, c in unfilled:
                current_bags = self._get_current_bags(test_grid)
                available = current_bags[c]
                
                if not available:
                    success = False
                    break
                
                # Try letters in order of preference
                placed = False
                for letter in available:
                    if self._is_valid_placement(test_grid, r, c, letter):
                        test_grid[r][c] = letter
                        placed = True
                        break
                
                if not placed:
                    success = False
                    break
            
            if success:
                print(f"  Completed grid on attempt {attempt + 1}")
                return test_grid
            
            # Randomize order for next attempt
            random.shuffle(unfilled)
        
        print(f"  Failed to complete after {max_attempts} attempts")
        return None
    
    def _get_current_bags(self, grid):
        """Get current state of bags"""
        bags = [bag.copy() for bag in self.original_bags]
        
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] and grid[r][c] != '' and grid[r][c] is not None:
                    if grid[r][c] in bags[c]:
                        bags[c].remove(grid[r][c])
        
        return bags
    
    def _is_valid_placement(self, grid, row, col, letter):
        """Check if placement is valid"""
        # Sudoku constraints for rows 5-13
        if 5 <= row <= 13:
            # Check row
            for c in range(9):
                if c != col and grid[row][c] == letter:
                    return False
            
            # Check column
            for r in range(5, 14):
                if r != row and r < len(grid) and grid[r][col] == letter:
                    return False
            
            # Check 3x3 box
            box_r, box_c = (row - 5) // 3, col // 3
            for r in range(box_r * 3 + 5, box_r * 3 + 8):
                for c in range(box_c * 3, box_c * 3 + 3):
                    if (r != row or c != col) and r < len(grid) and grid[r][c] == letter:
                        return False
        
        return True
    
    def _verify_complete_solution(self, grid):
        """Verify if this is a complete 10/10 solution"""
        if not grid:
            return False
        
        # Check all positions filled
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == '':
                    return False
        
        score = 0
        details = []
        
        # Check hash
        solution_str = self._grid_to_string(grid)
        if len(solution_str) >= 35:
            first_35 = solution_str[:35]
            hash_obj = hashlib.sha256(first_35.encode())
            hash_b64 = base64.b64encode(hash_obj.digest()).decode()
            if hash_b64 == self.target_hash:
                score += 1
                details.append("✓ Hash valid")
            else:
                details.append(f"✗ Hash: {hash_b64[:20]}...")
        
        # Check words
        found_words = []
        for word in self.required_words:
            if self._find_word_in_grid(word, grid):
                score += 1
                found_words.append(word)
                details.append(f"✓ Found {word}")
            else:
                details.append(f"✗ Missing {word}")
        
        # Check sudoku
        if self._check_sudoku_complete(grid):
            score += 3
            details.append("✓ Sudoku valid")
        else:
            details.append("✗ Sudoku invalid")
        
        # Check required positions
        skateboard_canine = ''.join(solution_str[idx] if idx < len(solution_str) else '' 
                                   for idx, _ in self.required_indices)
        if skateboard_canine == 'SKATEBOARDCANINE':
            score += 2
            details.append("✓ SKATEBOARD+CANINE valid")
        else:
            details.append(f"✗ SKATEBOARD+CANINE: {skateboard_canine}")
        
        print(f"  Score: {score}/10")
        for detail in details:
            print(f"    {detail}")
        
        return score == 10
    
    def _find_word_in_grid(self, word, grid):
        """Find word in grid"""
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
    
    def _check_sudoku_complete(self, grid):
        """Check sudoku constraints"""
        # Check rows 5-13
        for r in range(5, 14):
            if r < len(grid):
                row_letters = [grid[r][c] for c in range(9) if grid[r][c] and grid[r][c] != '']
                if len(set(row_letters)) != len(row_letters):
                    return False
        
        # Check columns
        for c in range(9):
            col_letters = [grid[r][c] for r in range(5, 14) 
                          if r < len(grid) and grid[r][c] and grid[r][c] != '']
            if len(set(col_letters)) != len(col_letters):
                return False
        
        # Check 3x3 boxes
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
    
    def _grid_to_string(self, grid):
        """Convert grid to string"""
        result = ''
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                result += cell if cell else ' '
        return result
    
    def print_solution(self, grid):
        """Print the solution"""
        if not grid:
            print("No solution found")
            return
        
        print("\n🎯 COMPLETE 10/10 SOLUTION FOUND!")
        print("=" * 40)
        
        for r in range(len(grid)):
            row_str = ""
            for c in range(len(grid[r])):
                cell = grid[r][c]
                if cell is None:
                    row_str += "█"
                else:
                    row_str += cell
            print(f"Row {r:2d}: {row_str}")

def main():
    print("🎯 SMART PENSIG SOLVER")
    print("=" * 30)
    
    random.seed(42)  # For reproducible results
    
    solver = SmartPensigSolver()
    solution = solver.solve_with_known_patterns()
    solver.print_solution(solution)

if __name__ == "__main__":
    main()