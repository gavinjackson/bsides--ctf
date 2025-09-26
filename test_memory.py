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

# Try format strings that might access memory or use advanced features
candidates = [
    # Stack-based access (common in format string exploits)
    "%p",
    "%s",
    "%n",
    
    # Position-based access
    "%1$p",
    "%2$p", 
    "%1$s",
    "%2$s",
    "%1$c",
    "%2$c",
    
    # Try some that might use the stack to do arithmetic
    "%1$d",
    "%2$d",
    
    # Maybe there's a way to use multiple arguments implicitly
    "%c%c",
    "%d%c", 
    "%c%d",
    
    # Length modifiers
    "%hc",
    "%lc",
    "%hhc",
    
    # Try format strings with unusual width specifiers
    "%0c",
    "%1c",
    "%2c",
]

print("Testing memory/stack access format strings...")
for fmt in candidates:
    if len(fmt) <= 30:
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