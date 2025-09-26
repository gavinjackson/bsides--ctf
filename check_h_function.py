#!/usr/bin/env python3
"""
Check what the h function really does
"""

QUOTE = "AAAA AA A ABBABB ABAC BCCAB A BCDCB CB CDEDC DCDDEIDDCEDEDHIDEDHEIEIKEEEIFKENMEHIMINIONIINNNRNONNNRORSRRRRRSRSTSSRSSSSSUWUSUST"
SKATEBOARD_CANINE_POSITIONS = [7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113]
SKATEBOARD_CANINE = "SKATEBOARDCANINE"

# The HTML creates cells from QUOTE, but blank cells (spaces) get className="blank" and tabIndex=-1
# So document.querySelectorAll('td') might only return non-blank cells

# Let's simulate what the DOM would look like
def simulate_dom_cells():
    """Simulate what document.querySelectorAll('td') would return"""
    cells = []
    for i, char in enumerate(QUOTE):
        if char == ' ':
            # This becomes a blank cell with className="blank" and tabIndex=-1
            # It might still be in the DOM but not selected by querySelectorAll('td')
            # OR it might be selected but have empty textContent
            cells.append(' ')  # Let's assume it's in the DOM but empty
        elif char.isalpha() and char.isupper():
            # Fillable cell - starts with the required letter but can be changed
            cells.append(char)  # This will be changed by the player
        else:
            # Fixed cell
            cells.append(char)
    return cells

def check_h_function_with_all_cells():
    """Check h function assuming all 126 cells are included"""
    cells = simulate_dom_cells()
    print(f"Simulated DOM cells (all {len(cells)} cells):")
    
    # Check what positions 7,11,15,16,20,23,31,37,47,56,70,71,80,90,104,113 contain
    extracted = ""
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if pos < len(cells):
            char = cells[pos]
            required = SKATEBOARD_CANINE[i]
            extracted += char
            print(f"Pos {pos:3d}: '{char}' (need '{required}') {'✓' if char == required else '✗'}")
        else:
            print(f"Pos {pos:3d}: OUT OF BOUNDS")
    
    print(f"\nExtracted: '{extracted}'")
    print(f"Target:    '{SKATEBOARD_CANINE}'")
    print(f"h function would return: {extracted == SKATEBOARD_CANINE}")

def check_h_function_with_non_blank_cells():
    """Check h function assuming only non-blank cells are included"""
    cells = []
    cell_positions = []  # Map cell index back to QUOTE position
    
    for i, char in enumerate(QUOTE):
        if char != ' ':  # Only non-blank cells
            cells.append(char)
            cell_positions.append(i)
    
    print(f"\nSimulated DOM cells (only non-blank {len(cells)} cells):")
    print(f"Cell positions in QUOTE: {cell_positions[:20]}...")  # Show first 20
    
    # Now check what the h function positions correspond to
    extracted = ""
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        if pos < len(cells):
            char = cells[pos]
            original_quote_pos = cell_positions[pos] if pos < len(cell_positions) else None
            required = SKATEBOARD_CANINE[i]
            extracted += char
            print(f"Cell {pos:3d} (QUOTE pos {original_quote_pos}): '{char}' (need '{required}') {'✓' if char == required else '✗'}")
        else:
            print(f"Cell {pos:3d}: OUT OF BOUNDS")
    
    print(f"\nExtracted: '{extracted}'")
    print(f"Target:    '{SKATEBOARD_CANINE}'")
    print(f"h function would return: {extracted == SKATEBOARD_CANINE}")

# Let's also check what happens if we manually set the required letters
def check_if_solvable():
    """Check if we can make the h function return 1"""
    cells = []
    for i, char in enumerate(QUOTE):
        if char != ' ':
            cells.append('?')  # Placeholder for now
    
    print(f"\nCan we solve for h function to return 1?")
    print(f"We have {len(cells)} cells to work with")
    print(f"We need to set specific cells to spell SKATEBOARD+CANINE")
    
    # Check which cells need to be set
    for i, pos in enumerate(SKATEBOARD_CANINE_POSITIONS):
        required = SKATEBOARD_CANINE[i]
        if pos < len(cells):
            print(f"Cell {pos:3d}: need '{required}'")
        else:
            print(f"Cell {pos:3d}: OUT OF BOUNDS (impossible)")
    
    # Check if any positions are out of bounds
    max_valid_pos = max(p for p in SKATEBOARD_CANINE_POSITIONS if p < len(cells))
    invalid_positions = [p for p in SKATEBOARD_CANINE_POSITIONS if p >= len(cells)]
    
    print(f"\nMax valid position: {max_valid_pos}")
    print(f"Invalid positions: {invalid_positions}")
    
    if invalid_positions:
        print("IMPOSSIBLE: Some positions are out of bounds")
        return False
    else:
        print("POSSIBLE: All positions are within bounds")
        return True

if __name__ == "__main__":
    check_h_function_with_all_cells()
    check_h_function_with_non_blank_cells()
    check_if_solvable()