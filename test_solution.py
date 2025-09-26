#!/usr/bin/env python3

import subprocess
import sys

def test_format_string(fmt_str):
    """Test a format string with the original program"""
    try:
        # Run the original program with the format string
        process = subprocess.Popen(['python3', 'uppawcase.py'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        stdout, stderr = process.communicate(input=fmt_str)
        print(f"Format string: '{fmt_str}'")
        print(f"Output: {stdout.strip()}")
        if stderr:
            print(f"Error: {stderr.strip()}")
        print("-" * 40)
        
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")

if __name__ == "__main__":
    # Test some potential format strings
    candidates = [
        "%c",
        "%d", 
        "%.c",
        "%*c",
        "%#c",
        "%+c",
        "%-c",
        "%32c",
        "%c%c",
    ]
    
    for fmt in candidates:
        test_format_string(fmt)