#include <stdio.h>

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    
    char c = argv[1][0];
    printf("Input char: %c (ASCII %d)\n", c, c);
    
    // The magic format string that converts lowercase to uppercase
    // We need to find what goes here:
    // printf("OUTPUT_FORMAT_HERE", c);
    
    return 0;
}