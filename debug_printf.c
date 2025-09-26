#include <stdio.h>
#include <string.h>

int main() {
    char test_chars[] = "abcdefghijklmnopqrstuvwxyz";
    
    // Test what happens with different format strings
    printf("Testing character 'a' (ASCII 97):\n");
    
    char c = 'a';
    
    // Try some format strings and see what they do
    printf("%%c: %c\n", c);
    printf("%%d: %d\n", c);
    printf("%%x: %x\n", c);
    printf("%%o: %o\n", c);
    
    // Try arithmetic in C to verify
    printf("c-32 as char: %c\n", c-32);
    printf("c-32 as int: %d\n", c-32);
    
    // Now let's see if there's any format string that can do this...
    // The challenge is to find a format string that takes 97 and outputs 'A' (65)
    
    return 0;
}