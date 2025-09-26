#!/usr/bin/env python3
"""
Complete Pensig Puzzle Solver
Uses constraint satisfaction and backtracking to find the full solution
"""

import hashlib
import base64
from typing import List, Dict, Tuple, Optional, Set
import copy
import itertools

class CompletePensigSolver:
    def __init__(self):
        self.QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
        self.WIDTH = 9
        self.HEIGHT = 14
        
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
        
        # Required positions for SKATEBOARD+CANINE
        self.required_positions = [
            (7, 'S'),   (11, 'K'),  (15, 'A'),  (16, 'T'),  (20, 'E'),  (23, 'B'),
            (31, 'O'),  (37, 'A'),  (47, 'R'),  (56, 'D'),  (70, 'C'),  (71, 'A'),
            (80, 'N'),  (90, 'I'),  (104, 'N'), (113, 'E')
        ]
        
        self.required_words = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']
        
        # Initialize grid and working state
        self.grid = self._initialize_grid()
        self.bags = [bag.copy() for bag in self.original_bags]
        
    def _initialize_grid(self) -> List[List[Optional[str]]]:
        """Initialize the grid based on the QUOTE string"""
        grid = []
        for i in range(len(self.QUOTE)):
            row = i // self.WIDTH
            col = i % self.WIDTH
            
            while len(grid) <= row:
                grid.append([None] * self.WIDTH)
                
            ch = self.QUOTE[i]
            if ch == ' ':
                grid[row][col] = None  # blank cell
            elif ch.isalpha() and ch.isupper():
                grid[row][col] = ''    # fillable cell
            else:
                grid[row][col] = ch    # fixed cell
                
        return grid
    
    def print_grid(self, title: str = "Grid"):
        """Print the current grid state"""
        print(f"\n{title}:")
        for r in range(len(self.grid)):
            row_str = f"{r:2d}: "
            for c in range(self.WIDTH):
                if r < len(self.grid) and c < len(self.grid[r]):
                    cell = self.grid[r][c]
                    if cell is None:
                        row_str += '█'
                    elif cell == '':
                        row_str += '.'
                    else:
                        row_str += cell
                else:
                    row_str += ' '
            print(row_str)
    
    def grid_to_string(self) -> str:
        """Convert grid to string for verification"""
        result = ''
        for r in range(len(self.grid)):
            for c in range(self.WIDTH):
                if r < len(self.grid) and c < len(self.grid[r]):
                    cell = self.grid[r][c]
                    result += cell if cell else ' '
                else:
                    result += ' '
        return result
    
    def place_letter(self, row: int, col: int, letter: str) -> bool:
        """Place a letter at position if valid"""
        if (row >= len(self.grid) or col >= self.WIDTH or 
            self.grid[row][col] != '' or letter not in self.bags[col]):
            return False
        
        self.grid[row][col] = letter
        self.bags[col].remove(letter)
        return True
    
    def remove_letter(self, row: int, col: int) -> Optional[str]:
        """Remove a letter from position and return it to bag"""
        if (row >= len(self.grid) or col >= self.WIDTH or 
            not self.grid[row][col] or self.grid[row][col] == ''):
            return None
        
        letter = self.grid[row][col]
        self.grid[row][col] = ''
        self.bags[col].append(letter)
        return letter
    
    def find_word_in_grid(self, word: str) -> Optional[Tuple[int, int, int, int]]:
        """Find a word in the grid (returns start position and direction)"""
        directions = [(0,1), (1,0), (1,1), (1,-1), (0,-1), (-1,0), (-1,-1), (-1,1)]
        
        for r in range(len(self.grid)):
            for c in range(self.WIDTH):
                for dr, dc in directions:
                    found = True
                    for i, target_letter in enumerate(word):
                        nr, nc = r + i * dr, c + i * dc
                        if (nr < 0 or nr >= len(self.grid) or nc < 0 or nc >= self.WIDTH or
                            self.grid[nr][nc] != target_letter):
                            found = False
                            break
                    if found:
                        return (r, c, dr, dc)
        return None
    
    def can_place_word(self, word: str, start_row: int, start_col: int, 
                      delta_row: int, delta_col: int) -> bool:
        """Check if word can be placed at position"""
        for i, letter in enumerate(word):
            r = start_row + i * delta_row
            c = start_col + i * delta_col
            
            if r < 0 or r >= len(self.grid) or c < 0 or c >= self.WIDTH:
                return False
            if self.grid[r][c] is None:  # blank cell
                return False
            if self.grid[r][c] != '' and self.grid[r][c] != letter:
                return False
            if self.grid[r][c] == '' and letter not in self.bags[c]:
                return False
        return True
    
    def place_word(self, word: str, start_row: int, start_col: int, 
                   delta_row: int, delta_col: int) -> List[Tuple[int, int]]:
        """Place word and return list of positions that were filled"""
        placed = []
        for i, letter in enumerate(word):
            r = start_row + i * delta_row
            c = start_col + i * delta_col
            
            if self.grid[r][c] == '':
                if self.place_letter(r, c, letter):
                    placed.append((r, c))
                else:
                    # Rollback
                    for pr, pc in placed:
                        self.remove_letter(pr, pc)
                    return []
        return placed
    
    def check_sudoku_valid(self) -> bool:
        """Check if sudoku constraints are satisfied"""
        # Check rows 5-13
        for r in range(5, 14):
            if r < len(self.grid):
                row_letters = [self.grid[r][c] for c in range(9) 
                             if self.grid[r][c] and self.grid[r][c] != '']
                if len(set(row_letters)) != len(row_letters):
                    return False
        
        # Check columns
        for c in range(9):
            col_letters = [self.grid[r][c] for r in range(5, 14) 
                          if r < len(self.grid) and self.grid[r][c] and self.grid[r][c] != '']
            if len(set(col_letters)) != len(col_letters):
                return False
        
        # Check 3x3 boxes
        for box_r in range(3):
            for box_c in range(3):
                box_letters = []
                for r in range(box_r * 3 + 5, box_r * 3 + 8):
                    for c in range(box_c * 3, box_c * 3 + 3):
                        if (r < len(self.grid) and self.grid[r][c] and 
                            self.grid[r][c] != ''):
                            box_letters.append(self.grid[r][c])
                if len(set(box_letters)) != len(box_letters):
                    return False
        
        return True
    
    def calculate_score(self) -> Tuple[int, Dict]:
        """Calculate current score and return details"""
        details = {
            'hash_valid': False,
            'words_found': [],
            'sudoku_valid': False,
            'skateboard_canine_valid': False
        }
        score = 0
        
        solution_str = self.grid_to_string()
        
        # Check hash (1 point)
        if len(solution_str) >= 35:
            first_35 = solution_str[:35]
            hash_obj = hashlib.sha256(first_35.encode())
            hash_b64 = base64.b64encode(hash_obj.digest()).decode()
            if hash_b64 == 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw=':
                details['hash_valid'] = True
                score += 1
        
        # Check words (4 points)
        for word in self.required_words:
            if self.find_word_in_grid(word):
                details['words_found'].append(word)
                score += 1
        
        # Check sudoku (3 points)
        if self.check_sudoku_valid():
            details['sudoku_valid'] = True
            score += 3
        
        # Check SKATEBOARD+CANINE (2 points)
        skateboard_canine = ''
        for idx, expected in self.required_positions:
            if idx < len(solution_str):
                skateboard_canine += solution_str[idx]
        
        if skateboard_canine == 'SKATEBOARDCANINE':
            details['skateboard_canine_valid'] = True
            score += 2
        
        return score, details
    
    def solve_step_by_step(self):
        """Solve the puzzle step by step"""
        print("🔍 Starting Pensig Puzzle Solution...")
        
        # Step 1: Place required SKATEBOARD+CANINE letters
        print("\n📍 Step 1: Placing required SKATEBOARD+CANINE letters")
        for idx, letter in self.required_positions:
            row = idx // self.WIDTH
            col = idx % self.WIDTH
            
            if (row < len(self.grid) and col < len(self.grid[row]) and 
                self.grid[row][col] == ''):
                if self.place_letter(row, col, letter):
                    print(f"  ✓ Placed {letter} at ({row},{col})")
                else:
                    print(f"  ✗ Could not place {letter} at ({row},{col}) - not available in column {col}")
        
        self.print_grid("After placing required letters")
        
        # Step 2: Try to place required words strategically
        print("\n🔤 Step 2: Placing required words")
        
        # Place SCIENCE first (most constrained)
        if self.can_place_word('SCIENCE', 9, 0, 0, 1):
            placed = self.place_word('SCIENCE', 9, 0, 0, 1)
            if placed:
                print("  ✓ Placed SCIENCE horizontally at row 9")
        
        # Try BSIDES vertically
        for start_row in range(5, 9):
            for col in range(9):
                if self.can_place_word('BSIDES', start_row, col, 1, 0):
                    placed = self.place_word('BSIDES', start_row, col, 1, 0)
                    if placed:
                        print(f"  ✓ Placed BSIDES vertically at ({start_row},{col})")
                        break
            if placed:
                break
        
        self.print_grid("After placing words")
        
        # Step 3: Fill remaining cells systematically
        print("\n🧩 Step 3: Filling remaining cells with sudoku constraints")
        self._fill_remaining_cells()
        
        # Final verification
        score, details = self.calculate_score()
        print(f"\n🎯 Final Score: {score}/10")
        
        if score == 10:
            print("🎉 PERFECT SOLUTION! All constraints satisfied!")
        else:
            print("📋 Score breakdown:")
            print(f"  Hash validation: {'✓' if details['hash_valid'] else '✗'}")
            print(f"  Words found: {details['words_found']} ({len(details['words_found'])}/4)")
            print(f"  Sudoku valid: {'✓' if details['sudoku_valid'] else '✗'}")
            print(f"  SKATEBOARD+CANINE: {'✓' if details['skateboard_canine_valid'] else '✗'}")
        
        return self.grid, score
    
    def _fill_remaining_cells(self):
        """Fill remaining cells using constraint satisfaction"""
        # Get all empty cells in sudoku region (rows 5-13)
        empty_cells = []
        for r in range(5, 14):
            for c in range(9):
                if r < len(self.grid) and self.grid[r][c] == '':
                    empty_cells.append((r, c))
        
        print(f"  Found {len(empty_cells)} empty cells to fill")
        
        # Try to fill cells one by one
        filled_count = 0
        for r, c in empty_cells:
            available_letters = self.bags[c].copy()
            
            for letter in available_letters:
                # Try placing this letter
                if self.place_letter(r, c, letter):
                    # Check if sudoku constraints are still valid
                    if self._is_placement_valid(r, c):
                        filled_count += 1
                        break
                    else:
                        # Remove and try next letter
                        self.remove_letter(r, c)
        
        print(f"  Successfully filled {filled_count} cells")
    
    def _is_placement_valid(self, row: int, col: int) -> bool:
        """Check if current placement maintains sudoku validity"""
        letter = self.grid[row][col]
        
        # Check row (only in sudoku region)
        if 5 <= row <= 13:
            row_letters = [self.grid[row][c] for c in range(9) 
                          if self.grid[row][c] and self.grid[row][c] != '']
            if row_letters.count(letter) > 1:
                return False
        
        # Check column (only in sudoku region)
        if 0 <= col <= 8:
            col_letters = [self.grid[r][col] for r in range(5, 14) 
                          if r < len(self.grid) and self.grid[r][col] and self.grid[r][col] != '']
            if col_letters.count(letter) > 1:
                return False
        
        # Check 3x3 box
        if 5 <= row <= 13 and 0 <= col <= 8:
            box_r = (row - 5) // 3
            box_c = col // 3
            box_letters = []
            for r in range(box_r * 3 + 5, box_r * 3 + 8):
                for c in range(box_c * 3, box_c * 3 + 3):
                    if (r < len(self.grid) and self.grid[r][c] and 
                        self.grid[r][c] != ''):
                        box_letters.append(self.grid[r][c])
            if box_letters.count(letter) > 1:
                return False
        
        return True

def main():
    solver = CompletePensigSolver()
    grid, score = solver.solve_step_by_step()
    
    print("\n" + "="*60)
    print("FINAL SOLUTION")
    print("="*60)
    solver.print_grid("Complete Solution")
    
    if score == 10:
        print("\n🎊 CONGRATULATIONS! Perfect solution achieved!")
        print("You can now input this solution into the web game to get 10/10 points!")
        
        # Print solution in a format easy to input
        print("\n📋 Solution for manual input:")
        for r in range(len(grid)):
            row_input = ""
            for c in range(solver.WIDTH):
                if r < len(grid) and c < len(grid[r]):
                    cell = grid[r][c]
                    if cell and cell != '' and cell != '█' and cell is not None:
                        row_input += cell
                    else:
                        row_input += "."
                else:
                    row_input += "."
            print(f"Row {r:2d}: {row_input}")

if __name__ == "__main__":
    main()