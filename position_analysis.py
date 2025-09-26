#!/usr/bin/env python3
"""
Analyze the position mapping more carefully
"""

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

print("Full QUOTE analysis:")
print(f"Length: {len(QUOTE)}")
print()

# Show the complete string with positions
for i, char in enumerate(QUOTE):
    if i in SKATEBOARD_CANINE_POSITIONS:
        idx = SKATEBOARD_CANINE_POSITIONS.index(i)
        expected = SKATEBOARD_CANINE[idx]
        print(f"Pos {i:3d}: '{char}' -> NEEDS '{expected}' {'✓' if char == expected else '✗'}")
    else:
        print(f"Pos {i:3d}: '{char}'")

print("\n" + "="*50)
print("SKATEBOARD+CANINE constraint analysis:")

total_matches = 0
for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
    if pos < len(QUOTE):
        current_char = QUOTE[pos]
        expected_char = SKATEBOARD_CANINE[i]
        match = current_char == expected_char
        if match:
            total_matches += 1
        print(f"Pos {pos:3d}: '{current_char}' -> need '{expected_char}' {'✓' if match else '✗'}")

print(f"\nCurrent matches: {total_matches}/{len(SKATEBOARD_CANINE)}")

# Let's see which positions are in the fillable part
print(f"\nAnalyzing which positions are fillable:")
fillable_positions = []
for i, char in enumerate(QUOTE):
    if char.isalpha() and char.isupper():
        fillable_positions.append(i)

print(f"Total fillable positions: {len(fillable_positions)}")

skateboard_fillable = []
for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
    if pos in fillable_positions:
        skateboard_fillable.append((pos, SKATEBOARD_CANINE[i]))

print(f"SKATEBOARD+CANINE positions that are fillable: {len(skateboard_fillable)}")
for pos, needed_char in skateboard_fillable:
    print(f"  Position {pos}: need '{needed_char}'")

# Check current string constraint satisfaction
current_extracted = ""
for pos in SKATEBOARD_CANINE_POSITIONS:
    if pos < len(QUOTE):
        current_extracted += QUOTE[pos]

print(f"\nCurrent extracted string: '{current_extracted}'")
print(f"Target string:           '{SKATEBOARD_CANINE}'")
print(f"Matches: {current_extracted == SKATEBOARD_CANINE}")

# Let's try to understand the grid layout better
print(f"\nGrid layout analysis:")
print("Positions 0-34 (header section):")
header = QUOTE[:35]
for i in range(0, len(header), 9):
    row_chars = header[i:i+9]
    positions = [str(j) for j in range(i, min(i+9, len(header)))]
    print(f"Positions {i:2d}-{min(i+8, len(header)-1):2d}: {' '.join(positions)}")
    print(f"Chars:     {' '.join(row_chars)}")
    print()

print("Positions 35+ (main grid section):")
main_section = QUOTE[35:]
for i in range(0, min(81, len(main_section)), 9):
    row_chars = main_section[i:i+9]
    positions = [str(j+35) for j in range(i, min(i+9, len(main_section)))]
    print(f"Positions {i+35:2d}-{min(i+8+35, len(QUOTE)-1):2d}: {' '.join(positions)}")
    print(f"Chars:     {' '.join(row_chars)}")
    print()