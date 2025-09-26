#!/usr/bin/env python3
"""
Pensig Puzzle Solver - Python Version
Solves the sudoku-like word game to achieve 10/10 points
"""

import hashlib
import base64
from typing import List, Dict, Tuple, Optional, Set
import copy

class PensigSolver:
    def __init__(self):
        # Game constants
        self.QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
        self.WIDTH = 9
        self.HEIGHT = len(self.QUOTE) // self.WIDTH + (1 if len(self.QUOTE) % self.WIDTH else 0)
        
        # Column bags as provided
        self.bags = [
            ['I','D','S','O','M','H','E','A','R','B','N','C'],           # col 0
            ['A','S','A','D','I','B','E','R','N','A','F','A','S','C'],   # col 1
            ['I','K','R','E','D','S','N','A','T','U','B','C'],           # col 2
            ['D','D','S','B','R','B','W','N','E','A','E','I','C'],       # col 3
            ['D','R','I','B','U','S','H','O','N','C','O','A','E'],       # col 4
            ['I','N','K','I','R','E','M','A','D','R','N','B','S','C'],   # col 5
            ['D','I','E','U','B','C','D','E','S','A','N','D','R','C'],   # col 6
            ['R','A','E','S','H','S','E','N','D','I','B','C'],           # col 7
            ['S','B','R','S','I','D','A','E','A','T','N','C']            # col 8
        ]
        
        # Required positions for SKATEBOARD+CANINE in final solution string
        self.required_positions = [
            (7, 'S'),   (11, 'K'),  (15, 'A'),  (16, 'T'),  (20, 'E'),  (23, 'B'),
            (31, 'O'),  (37, 'A'),  (47, 'R'),  (56, 'D'),  (70, 'C'),  (71, 'A'),
            (80, 'N'),  (90, 'I'),  (104, 'N'), (113, 'E')
        ]
        
        # Required words to find
        self.required_words = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']
        
        # Initialize grid
        self.solution = self._initialize_grid()
        
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
        for r in range(len(self.solution)):
            row_str = f"{r:2d}: "
            for c in range(self.WIDTH):
                if r < len(self.solution) and c < len(self.solution[r]):
                    cell = self.solution[r][c]
                    if cell is None:
                        row_str += '█'
                    elif cell == '':
                        row_str += '.'
                    else:
                        row_str += cell
                else:
                    row_str += ' '
            print(row_str)
    
    def print_bags(self):
        """Print remaining letters in column bags"""
        print("\nRemaining letters in bags:")
        for i, bag in enumerate(self.bags):
            print(f"Col {i}: {','.join(bag)}")
    
    def can_place_letter(self, row: int, col: int, letter: str) -> bool:
        """Check if a letter can be placed at the given position"""
        if row >= len(self.solution) or col >= len(self.solution[row]):
            return False
        if self.solution[row][col] != '':
            return False
        if letter not in self.bags[col]:
            return False
        return True
    
    def place_letter(self, row: int, col: int, letter: str) -> bool:
        """Place a letter at the given position"""
        if not self.can_place_letter(row, col, letter):
            return False
        
        self.solution[row][col] = letter
        self.bags[col].remove(letter)
        return True
    
    def place_required_letters(self):
        """Place the required SKATEBOARD+CANINE letters"""
        print("Placing required SKATEBOARD+CANINE letters:")
        
        for idx, letter in self.required_positions:
            row = idx // self.WIDTH
            col = idx % self.WIDTH
            
            if row < len(self.solution) and col < len(self.solution[row]):
                if self.solution[row][col] == '':  # fillable cell
                    if self.place_letter(row, col, letter):
                        print(f"Placed {letter} at ({row},{col})")
                    else:
                        print(f"ERROR: Cannot place {letter} at ({row},{col})")
                else:
                    print(f"Position ({row},{col}) is not fillable for {letter}")
    
    def can_place_word(self, word: str, start_row: int, start_col: int, 
                      delta_row: int, delta_col: int) -> bool:
        """Check if a word can be placed at the given position and direction"""
        for i, letter in enumerate(word):
            r = start_row + i * delta_row
            c = start_col + i * delta_col
            
            if r < 0 or r >= len(self.solution) or c < 0 or c >= self.WIDTH:
                return False
            if self.solution[r][c] is None:  # blank cell
                return False
            if self.solution[r][c] != '' and self.solution[r][c] != letter:
                return False
            if self.solution[r][c] == '' and letter not in self.bags[c]:
                return False
        return True
    
    def place_word(self, word: str, start_row: int, start_col: int, 
                   delta_row: int, delta_col: int) -> List[Tuple[int, int, str]]:
        """Place a word at the given position and direction"""
        placed = []
        for i, letter in enumerate(word):
            r = start_row + i * delta_row
            c = start_col + i * delta_col
            
            if self.solution[r][c] == '':
                if self.place_letter(r, c, letter):
                    placed.append((r, c, letter))
                else:
                    # Rollback
                    for pr, pc, pl in placed:
                        self.solution[pr][pc] = ''
                        self.bags[pc].append(pl)
                    return []
        return placed
    
    def find_word_in_grid(self, word: str) -> Optional[Tuple[int, int, int, int]]:
        """Find a word in the current grid"""
        directions = [(0,1), (1,0), (1,1), (1,-1), (0,-1), (-1,0), (-1,-1), (-1,1)]
        
        for r in range(len(self.solution)):
            for c in range(self.WIDTH):
                for dr, dc in directions:
                    found = True
                    for i, letter in enumerate(word):
                        nr, nc = r + i * dr, c + i * dc
                        if (nr < 0 or nr >= len(self.solution) or 
                            nc < 0 or nc >= self.WIDTH or
                            self.solution[nr][nc] != letter):
                            found = False
                            break
                    if found:
                        return (r, c, dr, dc)
        return None
    
    def try_place_words(self):
        """Try to place all required words"""
        print("\nAttempting to place required words:")
        
        # Try SCIENCE horizontally at row 9
        if self.can_place_word('SCIENCE', 9, 0, 0, 1):
            placed = self.place_word('SCIENCE', 9, 0, 0, 1)
            if placed:
                print(f"Placed SCIENCE horizontally at row 9")
        
        # Try other words at various positions
        word_placements = [
            ('BSIDES', 7, 5, 1, 0),   # vertically in column 5
            ('CANBERRA', 11, 0, 0, 1), # horizontally at row 11
            ('BRAINED', 5, 0, 1, 1),   # diagonally
        ]
        
        for word, sr, sc, dr, dc in word_placements:
            if self.can_place_word(word, sr, sc, dr, dc):
                placed = self.place_word(word, sr, sc, dr, dc)
                if placed:
                    print(f"Placed {word} at ({sr},{sc}) direction ({dr},{dc})")
    
    def check_sudoku_constraints(self) -> Dict[str, bool]:
        """Check if the 9x9 sudoku portion (rows 5-13) satisfies constraints"""
        results = {'rows': True, 'cols': True, 'boxes': True}
        
        # Check rows 5-13
        for r in range(5, 14):
            if r < len(self.solution):
                row_letters = [self.solution[r][c] for c in range(9) 
                             if self.solution[r][c] and self.solution[r][c] != '']
                if len(set(row_letters)) != len(row_letters):
                    results['rows'] = False
        
        # Check columns
        for c in range(9):
            col_letters = [self.solution[r][c] for r in range(5, 14) 
                          if r < len(self.solution) and self.solution[r][c] and self.solution[r][c] != '']
            if len(set(col_letters)) != len(col_letters):
                results['cols'] = False
        
        # Check 3x3 boxes
        for box_r in range(3):
            for box_c in range(3):
                box_letters = []
                for r in range(box_r * 3 + 5, box_r * 3 + 8):
                    for c in range(box_c * 3, box_c * 3 + 3):
                        if (r < len(self.solution) and self.solution[r][c] and 
                            self.solution[r][c] != ''):
                            box_letters.append(self.solution[r][c])
                if len(set(box_letters)) != len(box_letters):
                    results['boxes'] = False
        
        return results
    
    def calculate_score(self) -> int:
        """Calculate the puzzle score"""
        score = 0
        
        # Convert grid to string
        solution_str = ''
        for r in range(len(self.solution)):
            for c in range(self.WIDTH):
                if r < len(self.solution) and c < len(self.solution[r]):
                    cell = self.solution[r][c]
                    solution_str += cell if cell else ' '
                else:
                    solution_str += ' '
        
        if len(solution_str) != 116:
            return 0
        
        # Check hash (first 35 characters)
        first_35 = solution_str[:35]
        hash_obj = hashlib.sha256(first_35.encode())
        hash_b64 = base64.b64encode(hash_obj.digest()).decode()
        if hash_b64 == 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw=':
            score += 1
        
        # Check words (4 points)
        for word in self.required_words:
            if self.find_word_in_grid(word):
                score += 1
        
        # Check sudoku constraints (3 points)
        sudoku_check = self.check_sudoku_constraints()
        if sudoku_check['rows']:
            score += 1
        if sudoku_check['cols']:
            score += 1
        if sudoku_check['boxes']:
            score += 1
        
        # Check SKATEBOARD+CANINE positions (2 points)
        skateboard_canine = ''
        for idx, expected in self.required_positions:
            if idx < len(solution_str):
                skateboard_canine += solution_str[idx]
        if skateboard_canine == 'SKATEBOARDCANINE':
            score += 2
        
        return score
    
    def solve(self):
        """Main solving function"""
        print("=" * 50)
        print("PENSIG PUZZLE SOLVER")
        print("=" * 50)
        
        self.print_grid("Initial grid layout")
        
        # Step 1: Place required letters
        self.place_required_letters()
        self.print_grid("Grid after placing required letters")
        
        # Step 2: Try to place words
        self.try_place_words()
        self.print_grid("Grid after placing words")
        self.print_bags()
        
        # Step 3: Check constraints
        print("\nChecking constraints:")
        sudoku_check = self.check_sudoku_constraints()
        print(f"Sudoku rows valid: {sudoku_check['rows']}")
        print(f"Sudoku cols valid: {sudoku_check['cols']}")
        print(f"Sudoku boxes valid: {sudoku_check['boxes']}")
        
        # Step 4: Check words
        print("\nWord check:")
        for word in self.required_words:
            found = self.find_word_in_grid(word)
            print(f"{word}: {'Found' if found else 'Not found'}")
        
        # Step 5: Calculate score
        score = self.calculate_score()
        print(f"\nCurrent score: {score}/10")
        
        return score

def main():
    solver = PensigSolver()
    score = solver.solve()
    
    print("\n" + "=" * 50)
    print("SOLUTION SUMMARY")
    print("=" * 50)
    print(f"Final Score: {score}/10")
    
    if score == 10:
        print("🎉 PERFECT! You achieved full points!")
    else:
        print("Need to continue working on the solution...")
        print("\nTo achieve 10/10 points you need:")
        print("1. Hash validation (1 pt)")
        print("2. BSIDES word (1 pt)")
        print("3. CANBERRA word (1 pt)")
        print("4. SCIENCE word (1 pt)")
        print("5. BRAINED word (1 pt)")
        print("6. Valid sudoku rows (1 pt)")
        print("7. Valid sudoku columns (1 pt)")
        print("8. Valid sudoku 3x3 boxes (1 pt)")
        print("9. SKATEBOARD+CANINE positions (2 pts)")

if __name__ == "__main__":
    main()