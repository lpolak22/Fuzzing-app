#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void secret_vulnerability(const char* data, size_t len) {
    if (len >= 30 && strncmp(data, "START_CONFIG_V2_0", 17) == 0) {
        if (strstr(data + 17, "CRITICAL_MODE")) {
            if (len == 256) {
                fprintf(stderr, "FOUND CRITICAL PATH. Triggering vulnerability...\n");
                char buffer[16];
                strcpy(buffer, data); 
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "rb");
    if (!f) return 0;

    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *buffer = malloc(fsize + 1);
    if (!buffer) return 0;

    fread(buffer, fsize, 1, f);
    fclose(f);

    buffer[fsize] = 0;

    if (fsize > 20) {
        if (buffer[0] == 'A' && buffer[1] == 'F' && buffer[2] == 'L') {
            secret_vulnerability(buffer, fsize);
        }
    }

    free(buffer);
    return 0;
}