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
        
        stdout, stderr = process.communicate(input=fmt_str, timeout=5)
        result = stdout.strip()
        print(f"'{fmt_str}' -> {result}")
        return "skbdg{" in result or "FLAG" in result
        
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")
        return False

# Let me try some very specific combinations that might work
candidates = [
    # Maybe there's some way to use the width to do arithmetic?
    "%c%65c",  # Print char, then space-pad to column 65?
    "%97c",    # Use literal ASCII value
    "%65c",    # Use target ASCII value
    
    # What about using the difference directly?
    "%32c",    # The difference value
    "%-32c",   # Left-aligned with width 32
    "%+32c",   # With sign
    "% 32c",   # With space
    "%#32c",   # With alternate form
    
    # Try combinations with positioning and arithmetic-like patterns
    "%1$65c",  # Position 1, literal 65
    "%65$c",   # Position 65
    "%97$c",   # Position 97  
    "%32$c",   # Position 32
    
    # What about using multiple format specifiers?
    "%d%c",    # Print as int then char
    "%c%d",    # Print as char then int
    "%x%c",    # Print as hex then char
    "%c%x",    # Print as char then hex
    
    # Try some escape-like patterns
    "%%c",     # Literal % then c
    "%c%%",    # Char then literal %
    
    # What if there's some way to use precision or width creatively?
    "%.65c",   # Precision 65
    "%.32c",   # Precision 32
    "%.97c",   # Precision 97
    
    # Maybe there's some printf feature I don't know about?
    "%Lc",     # Long char
    "%hc",     # Short char
    "%llc",    # Long long char
    "%jc",     # intmax_t char
    "%zc",     # size_t char
    "%tc",     # ptrdiff_t char
]

print("Testing final candidate format strings...")
for fmt in candidates:
    if len(fmt) <= 30:
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "
        if all(c in allowed for c in fmt):
            if test_format_string(fmt):
                print(f"SUCCESS! Format string: '{fmt}'")
                break
        else:
            print(f"Skipping '{fmt}' - contains invalid characters")

print("Testing completed.")