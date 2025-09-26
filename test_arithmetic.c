#include <stdio.h>

int main() {
    char c = 'a';  // ASCII 97
    
    // We want to get to 'A' which is ASCII 65
    // Difference is 32
    
    // Let's try various format string approaches
    printf("Original: %c (%d)\n", c, c);
    
    // What if we use width/precision creatively?
    printf("With width: %5c\n", c);
    printf("With precision: %.1c\n", c);
    
    // What about using the value in different ways?
    printf("As char: %c\n", c);
    printf("As int: %d\n", c);
    
    // Target
    printf("Target: %c (%d)\n", c-32, c-32);
    
    return 0;
}