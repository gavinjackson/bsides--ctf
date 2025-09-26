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
        print(f"'{fmt_str}' -> {result}")
        return "skbdg{" in result or "FLAG" in result
        
    except subprocess.TimeoutExpired:
        print(f"'{fmt_str}' -> TIMEOUT")
        return False
    except Exception as e:
        print(f"Error testing '{fmt_str}': {e}")
        return False

# Focus on the * operator which can use the argument as width/precision
candidates = [
    # The * operator uses the next argument as width
    # But wait... we only have one argument: argv[1][0]
    # What if the format string uses the character value as width somehow?
    
    # Try using the input character as width for some other character
    "%*c",   # This should use argv[1][0] as width, but what's the character?
    "% *c",  # With space flag
    "%+*c",  # With plus flag
    "%-*c",  # With minus flag
    "%#*c",  # With hash flag
    
    # What if we combine with numbers?
    "%*1c",  # Width from arg, then literal 1 as char?
    "%*65c", # Width from arg, then literal 65 (ASCII 'A') as char?
    "%*97c", # Width from arg, then literal 97 (ASCII 'a') as char?
    
    # Or with precision
    "%.*c",  # Precision from arg
    "% .*c", 
    "%+.*c",
    "%-.*c", 
    "%#.*c",
    
    # Combined width and precision
    "%*.*c",
    "% *.*c",
    "%+*.*c", 
    "%-*.*c",
    "%#*.*c",
    
    # Maybe there's some way to use positioning
    "%1$*c",  # Position 1 as width
    "%1$.*c", # Position 1 as precision
    "%*1$c",  # Width from position 1
    "%.*1$c", # Precision from position 1
]

print("Testing * operator format strings...")
for fmt in candidates:
    if len(fmt) <= 30:
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%$*.#-+ "
        if all(c in allowed for c in fmt):
            if test_format_string(fmt):
                print(f"SUCCESS! Format string: '{fmt}'")
                break

print("Testing completed.")