#!/usr/bin/env python3
"""
Analyze the puzzle as a 9x9 grid
"""

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
WIDTH = 9

# From the JavaScript: the f function checks words in positions 35-116 (which is 81 characters = 9x9)
# This suggests the actual puzzle is the 9x9 section starting at position 35

def analyze_9x9_section():
    """Analyze the 9x9 section of the puzzle"""
    print("Analyzing 9x9 section...")
    
    # The 9x9 section starts at position 35 in the QUOTE
    section_start = 35
    section = QUOTE[section_start:section_start + 81]
    
    print(f"9x9 section: '{section}'")
    print(f"Length: {len(section)}")
    
    if len(section) == 81:
        print("\n9x9 Grid:")
        for row in range(9):
            row_chars = []
            for col in range(9):
                pos = row * 9 + col
                if pos < len(section):
                    char = section[pos]
                    row_chars.append(char)
                else:
                    row_chars.append('?')
            print(f"Row {row}: {' '.join(row_chars)}")
        
        # Count fillable positions in 9x9
        fillable_count = 0
        spaces_count = 0
        fixed_count = 0
        
        for char in section:
            if char == ' ':
                spaces_count += 1
            elif char.isalpha() and char.isupper():
                fillable_count += 1
            else:
                fixed_count += 1
        
        print(f"\n9x9 Section analysis:")
        print(f"Fillable positions: {fillable_count}")
        print(f"Spaces: {spaces_count}")
        print(f"Fixed characters: {fixed_count}")
        print(f"Total: {fillable_count + spaces_count + fixed_count}")
        
        return section
    else:
        print("ERROR: 9x9 section is not 81 characters")
        return None

def analyze_column_requirements_9x9():
    """Analyze what each column needs in the 9x9 grid"""
    section = QUOTE[35:35+81]
    
    if len(section) != 81:
        print("ERROR: Invalid 9x9 section")
        return
    
    print("\nColumn requirements for 9x9 grid:")
    print("="*50)
    
    column_requirements = {}
    
    for row in range(9):
        for col in range(9):
            pos = row * 9 + col
            char = section[pos]
            
            if char.isalpha() and char.isupper():
                if col not in column_requirements:
                    column_requirements[col] = []
                column_requirements[col].append((row, char))
    
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
    
    for col in range(9):
        if col in column_requirements:
            positions = column_requirements[col]
            required_letters = sorted([char for _, char in positions])
            available_letters = sorted(COLUMN_BAGS[col])
            
            print(f"\nColumn {col}:")
            print(f"  Positions: {len(positions)}")
            print(f"  Required:  {required_letters}")
            print(f"  Available: {available_letters}")
            
            # Check if they match
            if required_letters == available_letters:
                print(f"  ✓ Perfect match!")
            else:
                from collections import Counter
                req_count = Counter(required_letters)
                avail_count = Counter(available_letters)
                
                missing = []
                extra = []
                
                for letter in set(required_letters + available_letters):
                    req = req_count.get(letter, 0)
                    avail = avail_count.get(letter, 0)
                    if req > avail:
                        missing.extend([letter] * (req - avail))
                    elif avail > req:
                        extra.extend([letter] * (avail - req))
                
                if missing:
                    print(f"  Missing: {missing}")
                if extra:
                    print(f"  Extra: {extra}")
        else:
            print(f"\nColumn {col}: No fillable positions")

def check_skateboard_in_9x9():
    """Check SKATEBOARD+CANINE constraint in 9x9 context"""
    print("\nAnalyzing SKATEBOARD+CANINE in 9x9 context:")
    print("="*50)
    
    # The scoring function works on the full string, but f function checks 9x9 section
    # Let's see what the SKATEBOARD positions correspond to in a 9x9-only scenario
    
    SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
    SKATEBOARD_CANINE = "SKATEBOARDCANINE"
    
    # If we only have a 9x9 grid (81 characters), which positions are valid?
    valid_positions = [pos for pos in SKATEBOARD_CANINE_POSITIONS if pos < 81]
    
    print(f"SKATEBOARD+CANINE positions that fit in 9x9 grid:")
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required_char = SKATEBOARD_CANINE[i]
        if pos < 81:
            row, col = pos // 9, pos % 9
            print(f"  Pos {pos:2d} (row {row}, col {col}): need '{required_char}'")
        else:
            print(f"  Pos {pos:2d}: OUT OF BOUNDS for 9x9")
    
    print(f"\nValid positions in 9x9: {len(valid_positions)}/{len(SKATEBOARD_CANINE_POSITIONS)}")

if __name__ == "__main__":
    section = analyze_9x9_section()
    if section:
        analyze_column_requirements_9x9()
        check_skateboard_in_9x9()