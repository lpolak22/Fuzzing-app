#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_string(const char *input) {
    char buffer[16]; 
    
    if (!input || strlen(input) == 0) {
        fprintf(stderr, "Input is empty or NULL.\n");
        return;
    }
    
    fprintf(stderr, "Processing input string of length: %zu\n", strlen(input));

    strcpy(buffer, input); 

    fprintf(stderr, "Processing finished successfully.\n");
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <string_input>\n", argv[0]);
        return 1;
    }
    
    process_string(argv[1]);

    return 0;
}