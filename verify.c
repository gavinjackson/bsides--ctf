#include <stdio.h>

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Need argument\n");
        return 1;
    }
    
    printf("argv[1] = %s\n", argv[1]);
    printf("argv[1][0] = %c\n", argv[1][0]);
    printf("argv[1][0] as int = %d\n", argv[1][0]);
    
    return 0;
}