#!/usr/bin/env python3

import subprocess

def test_format_string(fmt_str):
    """Test a format string with the original program"""
    try:
        process = subprocess.Popen(['python3', 'uppawcase.py'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        stdout, stderr = process.communicate(input=fmt_str)
        result = stdout.strip()
        print(f"'{fmt_str}' -> {result}")
        return "skbdg{" in result or "FLAG" in result
        
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")
        return False

# More advanced format string attempts
candidates = [
    # Character arithmetic through positioning or width
    "%32$c",  # Position 32
    "%1$32c", # Position 1, width 32
    
    # Using negative numbers (might cause underflow)
    "%-32$c",
    
    # Multiple characters or operations
    "%c%32c", 
    "%32c%c",
    
    # Scientific notation or special formats
    "%e",
    "%g",
    "%f",
    
    # Octal representation (might help with bit manipulation)
    "%o",
    
    # Using the star operator creatively  
    "%*.*c",
    "%*.c",
    "%.*c",
    
    # Combinations with numbers that might do arithmetic
    "%c32",
    "32%c",
    "%c%32d",
    "%32d%c",
    
    # Using space and other formatting
    "% c",
    "%c ",
    " %c",
]

print("Testing advanced format strings...")
for fmt in candidates:
    if len(fmt) <= 30:  # Respect the length constraint
        # Check if it only contains allowed characters
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "
        if all(c in allowed for c in fmt):
            if test_format_string(fmt):
                print(f"SUCCESS! Format string: '{fmt}'")
                break
        else:
            print(f"Skipping '{fmt}' - contains invalid characters")
else:
    print("None of the tested format strings worked.")