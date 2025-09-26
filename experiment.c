#include <stdio.h>

int main() {
    char c = 'a';
    
    // Try different format approaches
    printf("Standard: %c\n", c);
    printf("As int: %d\n", c);
    printf("With arithmetic: %c\n", c - 32);
    
    // Try format string with positioning
    printf("Test format: %c\n", c);
    
    return 0;
}