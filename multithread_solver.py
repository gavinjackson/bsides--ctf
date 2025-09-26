#!/usr/bin/env python3
"""
Multi-threaded Pensig Solver with Optimized Constraint Propagation
Uses parallel processing and smart pruning to find the 10/10 solution quickly
"""

import hashlib
import base64
import itertools
import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Tuple, Optional, Set
import multiprocessing
import copy

class OptimizedPensigSolver:
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
        
        # Required SKATEBOARD+CANINE positions
        self.required_indices = [
            (7, 'S'), (11, 'K'), (15, 'A'), (16, 'T'), (20, 'E'), (23, 'B'),
            (31, 'O'), (37, 'A'), (47, 'R'), (56, 'D'), (70, 'C'), (71, 'A'),
            (80, 'N'), (90, 'I'), (104, 'N'), (113, 'E')
        ]
        
        self.required_words = ['BSIDES', 'CANBERRA', 'SCIENCE', 'BRAINED']
        self.target_hash = 'f2wY/HdX9INIR1BoLQV4Xp0HMMhUn8XZLYxlAfm1vRw='
        
        # Thread-safe solution storage
        self.solution_found = threading.Event()
        self.solution_lock = threading.Lock()
        self.found_solution = None
        
        # Initialize
        self.grid_template = self._create_grid_template()
        self.fillable_positions = self._get_fillable_positions()
        self.priority_positions = self._get_priority_positions()
        
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
        """Get all fillable positions"""
        positions = []
        for i, ch in enumerate(self.QUOTE):
            if ch.isupper():  # fillable
                row, col = i // self.WIDTH, i % self.WIDTH
                positions.append((row, col, i))
        return positions
    
    def _get_priority_positions(self):
        """Get positions ordered by constraint priority"""
        # Start with required SKATEBOARD+CANINE positions
        priority = []
        
        # Add fillable required positions first
        for idx, letter in self.required_indices:
            row, col = idx // self.WIDTH, idx % self.WIDTH
            if row < len(self.grid_template) and col < len(self.grid_template[row]):
                if self.grid_template[row][col] == '':  # fillable
                    priority.append((row, col, idx, letter, True))  # True = required
        
        # Add other fillable positions
        for row, col, idx in self.fillable_positions:
            if not any(r == row and c == col for r, c, _, _, _ in priority):
                priority.append((row, col, idx, None, False))  # False = not required
        
        return priority
    
    def _get_valid_letters(self, grid, row, col, required_letter=None):
        """Get valid letters for a position"""
        current_bags = self._get_current_bags(grid)
        
        if required_letter:
            return [required_letter] if required_letter in current_bags[col] else []
        
        valid = []
        for letter in current_bags[col]:
            if self._is_valid_placement(grid, row, col, letter):
                valid.append(letter)
        
        return valid
    
    def _is_valid_placement(self, grid, row, col, letter):
        """Quick validity check"""
        # Sudoku constraints only for rows 5-13
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
    
    def _get_current_bags(self, grid):
        """Get current state of bags"""
        bags = [bag.copy() for bag in self.original_bags]
        
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] and grid[r][c] != '' and grid[r][c] is not None:
                    if grid[r][c] in bags[c]:
                        bags[c].remove(grid[r][c])
        
        return bags
    
    def _quick_validate(self, grid):
        """Quick validation for early pruning"""
        # Check if required letters can still be placed
        current_bags = self._get_current_bags(grid)
        
        for idx, letter in self.required_indices:
            row, col = idx // self.WIDTH, idx % self.WIDTH
            if (row < len(grid) and col < len(grid[row]) and 
                grid[row][col] == '' and letter not in current_bags[col]):
                return False
        
        return True
    
    def solve_chunk(self, start_combination, chunk_size, thread_id):
        """Solve a chunk of the search space"""
        print(f"Thread {thread_id}: Starting chunk of size {chunk_size}")
        
        # Create base grid with required positions filled where possible
        base_grid = [row.copy() for row in self.grid_template]
        
        # Place required letters first
        required_placed = 0
        for idx, letter in self.required_indices:
            row, col = idx // self.WIDTH, idx % self.WIDTH
            if (row < len(base_grid) and col < len(base_grid[row]) and 
                base_grid[row][col] == ''):
                current_bags = self._get_current_bags(base_grid)
                if letter in current_bags[col]:
                    base_grid[row][col] = letter
                    required_placed += 1
        
        print(f"Thread {thread_id}: Placed {required_placed} required letters")
        
        # Get remaining positions to fill
        remaining_positions = []
        for row, col, idx in self.fillable_positions:
            if base_grid[row][col] == '':
                remaining_positions.append((row, col, idx))
        
        # Try different combinations for the first few positions
        if len(remaining_positions) > 20:  # If too many, just try a subset
            remaining_positions = remaining_positions[:20]
        
        attempts = 0
        for combo_offset in range(chunk_size):
            if self.solution_found.is_set():
                print(f"Thread {thread_id}: Solution found by another thread, stopping")
                return
            
            attempts += 1
            if attempts % 1000 == 0:
                print(f"Thread {thread_id}: Tried {attempts} combinations")
            
            # Try this specific combination
            test_grid = [row.copy() for row in base_grid]
            
            # Fill positions with a deterministic pattern based on offset
            valid = True
            for i, (row, col, idx) in enumerate(remaining_positions):
                current_bags = self._get_current_bags(test_grid)
                if not current_bags[col]:
                    valid = False
                    break
                
                # Use offset to select different letters deterministically
                letter_idx = (combo_offset + i) % len(current_bags[col])
                letter = current_bags[col][letter_idx]
                
                if self._is_valid_placement(test_grid, row, col, letter):
                    test_grid[row][col] = letter
                else:
                    valid = False
                    break
            
            if valid and self._is_complete_solution(test_grid):
                with self.solution_lock:
                    if not self.solution_found.is_set():
                        self.found_solution = test_grid
                        self.solution_found.set()
                        print(f"Thread {thread_id}: SOLUTION FOUND after {attempts} attempts!")
                        return test_grid
        
        print(f"Thread {thread_id}: Finished chunk, tried {attempts} combinations")
        return None
    
    def solve_parallel(self, num_threads=None):
        """Solve using multiple threads"""
        if num_threads is None:
            num_threads = min(multiprocessing.cpu_count(), 8)
        
        print(f"🚀 Starting parallel solve with {num_threads} threads")
        
        # Calculate chunk size
        total_combinations = 10000  # Reasonable limit
        chunk_size = total_combinations // num_threads
        
        print(f"Each thread will try {chunk_size} combinations")
        
        # Start threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                start_combo = i * chunk_size
                future = executor.submit(self.solve_chunk, start_combo, chunk_size, i)
                futures.append(future)
            
            # Monitor progress
            start_time = time.time()
            while not self.solution_found.is_set():
                time.sleep(1)
                elapsed = time.time() - start_time
                print(f"Elapsed: {elapsed:.1f}s - Still searching...")
                
                if elapsed > 300:  # 5 minute timeout
                    print("Timeout reached, stopping search")
                    break
            
            # Cancel remaining futures if solution found
            if self.solution_found.is_set():
                for future in futures:
                    future.cancel()
        
        return self.found_solution
    
    def _is_complete_solution(self, grid):
        """Check if solution is complete and valid"""
        # Quick check - all positions filled
        for row, col, _ in self.fillable_positions:
            if not grid[row][col] or grid[row][col] == '':
                return False
        
        # Check hash constraint (most restrictive)
        solution_str = self._grid_to_string(grid)
        if len(solution_str) >= 35:
            first_35 = solution_str[:35]
            hash_obj = hashlib.sha256(first_35.encode())
            hash_b64 = base64.b64encode(hash_obj.digest()).decode()
            if hash_b64 != self.target_hash:
                return False
        else:
            return False
        
        # Check required positions
        skateboard_canine = ''.join(solution_str[idx] if idx < len(solution_str) else '' 
                                   for idx, _ in self.required_indices)
        if skateboard_canine != 'SKATEBOARDCANINE':
            return False
        
        # Check words
        for word in self.required_words:
            if not self._find_word_in_grid(word, grid):
                return False
        
        # Check sudoku
        if not self._check_sudoku_complete(grid):
            return False
        
        return True
    
    def _find_word_in_grid(self, word, grid):
        """Find word in grid"""
        directions = [(0,1), (1,0), (1,1), (1,-1), (0,-1), (-1,0), (-1,-1), (-1,1)]
        
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                for dr, dc in directions:
                    if self._check_word_at_position(word, grid, r, c, dr, dc):
                        return True
        return False
    
    def _check_word_at_position(self, word, grid, start_r, start_c, dr, dc):
        """Check if word exists at specific position and direction"""
        for i, letter in enumerate(word):
            r, c = start_r + i * dr, start_c + i * dc
            if (r < 0 or r >= len(grid) or c < 0 or c >= len(grid[r]) or
                grid[r][c] != letter):
                return False
        return True
    
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
        """Print each row of the solution to standard out"""
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
        
        # Verify it's actually 10/10
        print(f"\n✅ VERIFICATION: {self._is_complete_solution(grid)}")

def main():
    print("🎯 MULTI-THREADED PENSIG SOLVER")
    print("=" * 45)
    
    solver = OptimizedPensigSolver()
    
    print(f"Grid has {len(solver.fillable_positions)} fillable positions")
    print(f"Using up to {min(multiprocessing.cpu_count(), 8)} threads")
    print()
    
    solution = solver.solve_parallel()
    solver.print_solution(solution)

if __name__ == "__main__":
    main()