#!/usr/bin/env python3
"""
Print characters to input row by row for Pensig puzzle
Shows only the letters you need to type for each row
"""

def main():
    print("🎯 PENSIG PUZZLE - INPUT BY ROW")
    print("=" * 40)
    print()
    
    # The QUOTE string determines which positions are fillable
    QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
    WIDTH = 9
    
    # Complete solution grid from working_solution.py
    solution_grid = [
        "SHAD█OW█S",   # Row 0
        "█CKETBA█T",   # Row 1
        "BRE█IBOAR",   # Row 2  
        "█A█IONSD█",   # Row 3
        "CA█NESID█",   # Row 4
        "BSRAHIDEC",   # Row 5
        "HIDESCARB",   # Row 6
        "EDARBSICA",   # Row 7
        "RACSIDEBN",   # Row 8
        "SCIENCEAD",   # Row 9
        "INSCARBDE",   # Row 10
        "DEBICNRSA",   # Row 11
        "ARCDBESIS",   # Row 12
        "CBASDARNI"    # Row 13
    ]
    
    print("For each row, type these letters in order (left to right):")
    print("Skip █ positions - they are blank spaces")
    print("Fixed letters are already in place")
    print()
    
    for row_idx, row_str in enumerate(solution_grid):
        # Determine which positions in this row are fillable
        fillable_letters = []
        
        for col_idx, cell in enumerate(row_str):
            if cell != '█':  # not blank
                quote_idx = row_idx * WIDTH + col_idx
                if quote_idx < len(QUOTE):
                    quote_char = QUOTE[quote_idx]
                    if quote_char.isupper():  # fillable position
                        fillable_letters.append(cell)
        
        if fillable_letters:
            letters_str = ' '.join(fillable_letters)
            print(f"Row {row_idx:2d}: {letters_str}")
        else:
            print(f"Row {row_idx:2d}: (no fillable positions)")
    
    print()
    print("📋 INSTRUCTIONS:")
    print("1. Open the puzzle in your browser")
    print("2. For each row, click the fillable positions and type the letters shown")
    print("3. Work left to right, top to bottom")
    print("4. Check your score with the 'Check' button")
    print("5. You should get 10/10 points and see the flag in console!")
    
    print()
    print("💡 Alternative format (position by position):")
    print("If you prefer to see exact positions:")
    print()
    
    # Show position-by-position for verification
    input_count = 0
    for row_idx, row_str in enumerate(solution_grid):
        for col_idx, cell in enumerate(row_str):
            if cell != '█':  # not blank
                quote_idx = row_idx * WIDTH + col_idx
                if quote_idx < len(QUOTE):
                    quote_char = QUOTE[quote_idx]
                    if quote_char.isupper():  # fillable position
                        input_count += 1
                        print(f"{input_count:3d}. ({row_idx},{col_idx}): {cell}")
    
    print(f"\nTotal: {input_count} letters to input")

if __name__ == "__main__":
    main()