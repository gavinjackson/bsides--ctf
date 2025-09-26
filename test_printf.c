#include <stdio.h>

int main() {
    char c = 'a';  // ASCII 97
    
    // Test different format strings
    printf("Input: %c (ASCII %d)\n", c, c);
    printf("Direct %%c: %c\n", c);
    printf("ASCII - 32: %c\n", c - 32);
    
    return 0;
}