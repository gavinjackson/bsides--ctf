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
        if result != "format string: incorrect!":
            print(f"'{fmt_str}' -> {result}")
            return "skbdg{" in result or "FLAG" in result
        
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")
        
    return False

# Try some more exotic format strings
candidates = [
    # Maybe there's a way to use the argument position creatively
    "%c%*c",  # Use * for width
    "%*c%c",
    "%*.c",
    "%.*c",
    "%*.*c",
    
    # Position-based with arithmetic-like patterns
    "%1$*c", 
    "%*1$c",
    "%1$*2$c",
    
    # Using multiple args in creative ways
    "%c%*d",
    "%*d%c",
    "%d%*c",
    
    # Maybe there's some format specifier I don't know about
    "%tc",  # Try with different letters
    "%bc",
    "%kc",
    "%mc",
    "%rc",
    "%uc",  # uppercase? (probably not valid)
    "%lc",  # long char
    "%Lc",  # long long char? 
    
    # Try with combinations
    "% %c",  # space flag
    "%##c",  # double hash
    "%++c",  # double plus
    "%--c",  # double minus
    
    # Try scientific notation style
    "%c32",
    "32%c",
    "%c+32",
    "%c-32",
    
    # Try hex patterns
    "%x%c",
    "%c%x",
    "%X%c",
    "%c%X",
]

print("Testing exotic format strings...")
for fmt in candidates:
    if len(fmt) <= 30:
        # Check if it only contains allowed characters
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "
        if all(c in allowed for c in fmt):
            if test_format_string(fmt):
                print(f"SUCCESS! Format string: '{fmt}'")
                break

print("Testing completed.")