#!/usr/bin/env python3
"""
Manual Solution Guide for Pensig Puzzle
Step-by-step instructions to achieve 10/10 points
"""

class ManualSolutionGuide:
    def __init__(self):
        self.QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
        self.WIDTH = 9
        
        # Column bags as provided
        self.bags = [
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
        
        # Required SKATEBOARD+CANINE positions (that are fillable)
        self.required_fillable = [
            (1, 2, 'K'),   # Row 1, Col 2: K
            (1, 6, 'A'),   # Row 1, Col 6: A
            (2, 2, 'E'),   # Row 2, Col 2: E
            (2, 5, 'B'),   # Row 2, Col 5: B
            (3, 4, 'O'),   # Row 3, Col 4: O
            (4, 1, 'A'),   # Row 4, Col 1: A
            (5, 2, 'R'),   # Row 5, Col 2: R
            (6, 2, 'D'),   # Row 6, Col 2: D
            (7, 7, 'C'),   # Row 7, Col 7: C
            (7, 8, 'A'),   # Row 7, Col 8: A
            (8, 8, 'N'),   # Row 8, Col 8: N
            (10, 0, 'I'),  # Row 10, Col 0: I
            (11, 5, 'N'),  # Row 11, Col 5: N
            (12, 5, 'E'),  # Row 12, Col 5: E
        ]
    
    def print_initial_setup(self):
        """Print the initial puzzle setup"""
        print("🎯 PENSIG PUZZLE - MANUAL SOLUTION GUIDE")
        print("=" * 60)
        print()
        print("📋 STEP 1: Understanding the Layout")
        print("-" * 30)
        print("Grid template (█ = blank, . = fillable, letter = fixed):")
        print()
        
        for i in range(len(self.QUOTE)):
            if i % self.WIDTH == 0:
                if i > 0:
                    print()
                print(f"Row {i//self.WIDTH:2d}: ", end="")
            
            ch = self.QUOTE[i]
            if ch == ' ':
                print('█', end="")
            elif ch.isalpha() and ch.isupper():
                print('.', end="")
            else:
                print(ch, end="")
        print("\n")
    
    def print_required_positions(self):
        """Print required SKATEBOARD+CANINE positions"""
        print("📍 STEP 2: Place Required SKATEBOARD+CANINE Letters")
        print("-" * 50)
        print("These letters MUST go in these exact positions:")
        print()
        
        for row, col, letter in self.required_fillable:
            bag_letters = ', '.join(self.bags[col])
            available = letter in self.bags[col]
            status = "✓ Available" if available else "✗ Not available"
            print(f"  Position ({row},{col}): {letter} - {status}")
            if not available:
                print(f"    Column {col} has: {bag_letters}")
        print()
    
    def print_word_strategy(self):
        """Print strategy for placing required words"""
        print("🔤 STEP 3: Place Required Words")
        print("-" * 30)
        print("You need to find these words somewhere in your completed grid:")
        print()
        
        words = ['SCIENCE', 'BSIDES', 'CANBERRA', 'BRAINED']
        strategies = [
            "SCIENCE: Try horizontally at row 9 (S-C-I-E-N-C-E)",
            "BSIDES: Try vertically starting around row 7-8",
            "CANBERRA: Try horizontally, maybe row 11 or 12",
            "BRAINED: Look for diagonal or other placements"
        ]
        
        for word, strategy in zip(words, strategies):
            print(f"  • {strategy}")
        print()
    
    def print_sudoku_rules(self):
        """Print sudoku constraint explanation"""
        print("🧩 STEP 4: Complete the 9×9 Sudoku (Rows 5-13)")
        print("-" * 45)
        print("The bottom portion (rows 5-13, columns 0-8) must follow sudoku rules:")
        print()
        print("  • Each ROW must contain unique letters")
        print("  • Each COLUMN must contain unique letters") 
        print("  • Each 3×3 BOX must contain unique letters")
        print()
        print("The 3×3 boxes are:")
        print("  Box 1: Rows 5-7, Cols 0-2")
        print("  Box 2: Rows 5-7, Cols 3-5")
        print("  Box 3: Rows 5-7, Cols 6-8")
        print("  Box 4: Rows 8-10, Cols 0-2")
        print("  Box 5: Rows 8-10, Cols 3-5")
        print("  Box 6: Rows 8-10, Cols 6-8")
        print("  Box 7: Rows 11-13, Cols 0-2")
        print("  Box 8: Rows 11-13, Cols 3-5")
        print("  Box 9: Rows 11-13, Cols 6-8")
        print()
    
    def print_solving_strategy(self):
        """Print overall solving strategy"""
        print("🎲 STEP 5: Solving Strategy")
        print("-" * 25)
        print("Recommended order:")
        print()
        print("1. Place all required SKATEBOARD+CANINE letters first")
        print("2. Try to place SCIENCE horizontally at row 9")
        print("3. Work on the sudoku constraints in the 9×9 region")
        print("4. Look for opportunities to place other required words")
        print("5. Fill remaining cells while maintaining constraints")
        print("6. Use 'Check' button frequently to verify progress")
        print()
        print("💡 Tips:")
        print("  • Start with the most constrained positions")
        print("  • Use the column bags - you can only use letters available")
        print("  • Letters return to bags when you remove them")
        print("  • If stuck, try backtracking and different letter choices")
        print()
    
    def print_verification_guide(self):
        """Print how to verify the solution"""
        print("✅ STEP 6: Verification")
        print("-" * 20)
        print("Your solution is complete when you achieve 10/10 points:")
        print()
        print("  1 point:  Hash validation (automatic)")
        print("  1 point:  BSIDES found in grid")
        print("  1 point:  CANBERRA found in grid") 
        print("  1 point:  SCIENCE found in grid")
        print("  1 point:  BRAINED found in grid")
        print("  1 point:  All rows 5-13 have unique letters")
        print("  1 point:  All columns 0-8 have unique letters")
        print("  1 point:  All 3×3 boxes have unique letters")
        print("  2 points: SKATEBOARD+CANINE in correct positions")
        print()
        print("🎉 When you get 10/10, the flag will appear in the browser console!")
        print()
    
    def print_quick_reference(self):
        """Print quick reference for solving"""
        print("📚 QUICK REFERENCE")
        print("-" * 20)
        print()
        print("Required positions (row, col): letter")
        for row, col, letter in self.required_fillable:
            print(f"  ({row},{col}): {letter}")
        print()
        print("Required words: SCIENCE, BSIDES, CANBERRA, BRAINED")
        print("Sudoku region: Rows 5-13, Columns 0-8")
        print("Goal: 10/10 points")
        print()
    
    def print_complete_guide(self):
        """Print the complete solving guide"""
        self.print_initial_setup()
        self.print_required_positions()
        self.print_word_strategy()
        self.print_sudoku_rules()
        self.print_solving_strategy()
        self.print_verification_guide()
        self.print_quick_reference()

def main():
    guide = ManualSolutionGuide()
    guide.print_complete_guide()
    
    print("🚀 Ready to solve! Open the puzzle in your browser and follow these steps.")
    print("   Remember: this is a constraint satisfaction puzzle requiring patience!")

if __name__ == "__main__":
    main()