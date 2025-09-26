#!/usr/bin/env python3
"""
Pensig Puzzle Helper - Interactive Python Tool
Helps you build and verify the solution step by step
"""

import hashlib
import base64
from typing import List, Dict, Tuple, Optional
import json

class PensigHelper:
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
        
    def create_grid_template(self) -> List[List[str]]:
        """Create an empty grid template showing fillable positions"""
        grid = []
        for i in range(len(self.QUOTE)):
            row = i // self.WIDTH
            col = i % self.WIDTH
            
            while len(grid) <= row:
                grid.append([''] * self.WIDTH)
                
            ch = self.QUOTE[i]
            if ch == ' ':
                grid[row][col] = '█'  # blank
            elif ch.isalpha() and ch.isupper():
                grid[row][col] = '.'  # fillable
            else:
                grid[row][col] = ch   # fixed
                
        return grid
    
    def print_template(self):
        """Print the grid template with position markers"""
        print("PENSIG PUZZLE TEMPLATE")
        print("=" * 40)
        print("Legend: █ = blank, . = fillable, letter = fixed")
        print()
        
        template = self.create_grid_template()
        for r in range(len(template)):
            row_str = f"{r:2d}: "
            for c in range(self.WIDTH):
                row_str += template[r][c]
            print(row_str)
    
    def print_required_positions(self):
        """Print the required SKATEBOARD+CANINE positions"""
        print("\nREQUIRED SKATEBOARD+CANINE POSITIONS:")
        print("=" * 40)
        word = 'SKATEBOARDCANINE'
        for i, (idx, letter) in enumerate(self.required_positions):
            row = idx // self.WIDTH
            col = idx % self.WIDTH
            print(f"Position ({row:2d},{col}): {letter} (index {idx:3d}) - {word[:i+1]}")
    
    def print_column_bags(self):
        """Print the available letters in each column"""
        print("\nCOLUMN BAGS:")
        print("=" * 40)
        for i, bag in enumerate(self.original_bags):
            print(f"Column {i}: {' '.join(bag)}")
            print(f"         ({len(bag)} letters)")
    
    def print_word_requirements(self):
        """Print the required words"""
        print("\nREQUIRED WORDS:")
        print("=" * 40)
        for word in self.required_words:
            print(f"- {word}")
    
    def print_scoring_guide(self):
        """Print the scoring breakdown"""
        print("\nSCORING BREAKDOWN (10 points total):")
        print("=" * 40)
        print("1 point:  Hash validation (first 35 characters)")
        print("1 point:  BSIDES found in grid")
        print("1 point:  CANBERRA found in grid")
        print("1 point:  SCIENCE found in grid")
        print("1 point:  BRAINED found in grid")
        print("1 point:  Sudoku rows valid (rows 5-13)")
        print("1 point:  Sudoku columns valid (cols 0-8)")
        print("1 point:  Sudoku 3x3 boxes valid")
        print("2 points: SKATEBOARD+CANINE in correct positions")
    
    def verify_solution(self, solution_grid: List[List[str]]) -> Dict:
        """Verify a complete solution"""
        results = {
            'score': 0,
            'hash_valid': False,
            'words_found': [],
            'sudoku_rows': False,
            'sudoku_cols': False,
            'sudoku_boxes': False,
            'skateboard_canine': False,
            'details': []
        }
        
        # Convert grid to string
        solution_str = ''
        for r in range(len(solution_grid)):
            for c in range(self.WIDTH):
                if c < len(solution_grid[r]):
                    cell = solution_grid[r][c]
                    solution_str += cell if cell not in ['█', '.', ''] else ' '
                else:
                    solution_str += ' '
        
        # Check hash
        if len(solution_str) >= 35:
            first_35 = solution_str[:35]
            hash_obj = hashlib.sha256(first_35.encode())
            hash_b64 = base64.b64encode(hash_obj.digest()).decode()
            if hash_b64 == 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw=':
                results['hash_valid'] = True
                results['score'] += 1
                results['details'].append("✓ Hash validation passed")
            else:
                results['details'].append(f"✗ Hash validation failed (got: {hash_b64[:20]}...)")
        
        # Check words
        for word in self.required_words:
            if self._find_word_in_grid(word, solution_grid):
                results['words_found'].append(word)
                results['score'] += 1
                results['details'].append(f"✓ Found word: {word}")
            else:
                results['details'].append(f"✗ Word not found: {word}")
        
        # Check SKATEBOARD+CANINE
        skateboard_canine = ''
        for idx, expected in self.required_positions:
            if idx < len(solution_str):
                skateboard_canine += solution_str[idx]
        
        if skateboard_canine == 'SKATEBOARDCANINE':
            results['skateboard_canine'] = True
            results['score'] += 2
            results['details'].append("✓ SKATEBOARD+CANINE positions correct")
        else:
            results['details'].append(f"✗ SKATEBOARD+CANINE incorrect (got: {skateboard_canine})")
        
        return results
    
    def _find_word_in_grid(self, word: str, grid: List[List[str]]) -> bool:
        """Find a word in the grid (all 8 directions)"""
        directions = [(0,1), (1,0), (1,1), (1,-1), (0,-1), (-1,0), (-1,-1), (-1,1)]
        
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                for dr, dc in directions:
                    found = True
                    for i, letter in enumerate(word):
                        nr, nc = r + i * dr, c + i * dc
                        if (nr < 0 or nr >= len(grid) or 
                            nc < 0 or nc >= len(grid[nr]) or
                            grid[nr][nc] != letter):
                            found = False
                            break
                    if found:
                        return True
        return False
    
    def save_template(self, filename: str = "pensig_template.json"):
        """Save the puzzle template to a JSON file"""
        template_data = {
            'grid_template': self.create_grid_template(),
            'column_bags': self.original_bags,
            'required_positions': self.required_positions,
            'required_words': self.required_words,
            'width': self.WIDTH,
            'height': self.HEIGHT
        }
        
        with open(filename, 'w') as f:
            json.dump(template_data, f, indent=2)
        print(f"Template saved to {filename}")
    
    def load_solution(self, filename: str) -> Optional[List[List[str]]]:
        """Load a solution from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return data.get('solution_grid', None)
        except FileNotFoundError:
            print(f"File {filename} not found")
            return None
    
    def print_full_guide(self):
        """Print complete solving guide"""
        self.print_template()
        self.print_required_positions()
        self.print_column_bags()
        self.print_word_requirements()
        self.print_scoring_guide()

def main():
    helper = PensigHelper()
    
    print("PENSIG PUZZLE HELPER")
    print("=" * 50)
    print("This tool helps you understand and solve the Pensig puzzle.")
    print("Use the methods below to get different information:")
    print()
    print("helper.print_template()           - Show grid template")
    print("helper.print_required_positions() - Show SKATEBOARD+CANINE positions")
    print("helper.print_column_bags()        - Show available letters")
    print("helper.print_word_requirements()  - Show required words")
    print("helper.print_scoring_guide()      - Show scoring breakdown")
    print("helper.print_full_guide()         - Show everything")
    print("helper.save_template()            - Save template to JSON")
    print()
    print("Example usage in Python:")
    print("from pensig_helper import PensigHelper")
    print("helper = PensigHelper()")
    print("helper.print_full_guide()")
    
    # Show the full guide by default
    helper.print_full_guide()

if __name__ == "__main__":
    main()