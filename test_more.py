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
        return "skbdg{" in result  # Check if we got the flag
        
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")
        return False

# Let me try some more creative format strings
candidates = [
    # Basic attempts
    "%c",
    "%d",
    
    # Arithmetic-looking attempts
    "%97c",  # Using ASCII value
    "%65c",  # Target ASCII value
    
    # Using positioning
    "%1$c",
    
    # Using multiple specifiers with math-like patterns
    "%d %c",
    "%97d",
    "%65d", 
    
    # Creative width/precision
    "%*32c",
    "%-32c",
    "%+32c",
    
    # Hexadecimal (might allow different manipulation)
    "%x",
    "%X",
]

print("Testing format strings...")
for fmt in candidates:
    if len(fmt) <= 30:  # Respect the length constraint
        if test_format_string(fmt):
            print(f"SUCCESS! Format string: '{fmt}'")
            break
else:
    print("None of the tested format strings worked.")