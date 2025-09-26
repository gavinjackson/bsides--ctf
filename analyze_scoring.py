#!/usr/bin/env python3
"""
Analyze the scoring function to understand all constraints
"""

# The scoring function breakdown:
# score = res + 1 + f('BSIDES') + f('CANBERRA') + f('SCIENCE') + f('BRAINED') + g(x=>x/9|0) + g(x=>x%9) + g(x=>[x/27|0,x%9/3|0]) + h('SKATEBOARD'+'CANINE')

# Where:
# - res: SHA check of first 35 characters (1 point if correct)
# - 1: base point
# - f(word): 1 point if word found in any direction in the 9x9 grid (positions 35-116)
# - g(func): 1 point if Sudoku constraint satisfied (rows, columns, 3x3 boxes)
# - h(string): 1 point if specific positions spell "SKATEBOARDCANINE"

# Let's understand the h function:
# h=z=>z==[7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113].map(x=>s[x]).join('');

positions = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
target = "SKATEBOARDCANINE"

print("Function h analysis:")
print(f"Target string: {target}")
print(f"Positions: {positions}")
print(f"Length: {len(positions)} positions for {len(target)} characters")

# Let's understand the grid structure better
QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"

print(f"\nQUOTE length: {len(QUOTE)}")
print("First 35 characters (header):", QUOTE[:35])
print("Characters 35-116 (9x9 grid):", QUOTE[35:116])
print("Remaining characters:", QUOTE[116:])

print(f"\nGrid section length: {len(QUOTE[35:116])}")
print("Should be 81 for 9x9 grid")

# Check the specific positions for h function
print(f"\nPositions in h function (should spell SKATEBOARDCANINE):")
for i, pos in enumerate(positions):
    if pos < len(QUOTE):
        char = QUOTE[pos]
        expected = target[i] if i < len(target) else '?'
        print(f"Position {pos}: '{char}' (expected: '{expected}')")
    else:
        print(f"Position {pos}: OUT OF BOUNDS")

# Let's see the 9x9 grid structure
print(f"\n9x9 Grid structure (positions 35-116):")
grid_section = QUOTE[35:116]
if len(grid_section) == 81:
    for row in range(9):
        row_chars = []
        for col in range(9):
            pos = row * 9 + col
            char = grid_section[pos] if pos < len(grid_section) else '?'
            row_chars.append(char)
        print(f"Row {row}: {' '.join(row_chars)}")