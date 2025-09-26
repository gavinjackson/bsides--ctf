#include <stdio.h>

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    
    char c = argv[1][0];
    printf("Input: %c\n", c);
    
    // Try various format strings
    printf("%%c: ");
    printf("%c", c);
    printf("\n");
    
    printf("%%d: ");
    printf("%d", c);
    printf("\n");
    
    // This is what we want to achieve
    printf("Target: %c\n", c - 32);
    
    return 0;
}