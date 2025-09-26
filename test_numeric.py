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

# Try format strings with specific numbers related to ASCII conversion
candidates = []

# Generate candidates with different numbers
for i in range(33):  # 0 to 32
    candidates.extend([
        f"%{i}c",
        f"%-{i}c", 
        f"%+{i}c",
        f"%.{i}c",
        f"%{i}d",
        f"%-{i}d",
    ])

# Also try some specific patterns
additional = [
    "%32c",
    "%-32c", 
    "%+32c",
    "%.32c",
    "%32d",
    "%-32d",
    "%65c",  # ASCII of 'A'
    "%97c",  # ASCII of 'a'
]

candidates.extend(additional)

print("Testing numeric format strings...")
success = False
for fmt in candidates:
    if len(fmt) <= 30:
        # Check if it only contains allowed characters
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "
        if all(c in allowed for c in fmt):
            if test_format_string(fmt):
                print(f"SUCCESS! Format string: '{fmt}'")
                success = True
                break
        else:
            print(f"Skipping '{fmt}' - contains invalid characters")
    
    # Only show first few attempts to avoid spam
    if len([f for f in candidates[:10] if f == fmt]) > 0:
        continue

if not success:
    print("None of the tested format strings worked.")