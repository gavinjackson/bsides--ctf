#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <char>\n", argv[0]);
        return 1;
    }
    
    char c = argv[1][0];
    printf("Testing with input: %c (ASCII %d)\n", c, c);
    printf("Target output: %c (ASCII %d)\n", c-32, c-32);
    
    // Try some potential format strings:
    
    // Simple character
    printf("%%c: ");
    printf("%c", c);
    printf("\n");
    
    // What about using arithmetic within constraints?
    // We need to subtract 32, which is 2^5
    
    // Let me try some creative approaches...
    
    return 0;
}