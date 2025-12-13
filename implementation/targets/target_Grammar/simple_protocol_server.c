#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 9999
#define BUFFER_SIZE 1024
#define PROTOCOL_MAGIC "CMD:"

void process_input(char *buffer, int len) {
    if (strncmp(buffer, PROTOCOL_MAGIC, strlen(PROTOCOL_MAGIC)) != 0) {
        fprintf(stderr, "Invalid protocol header. Ignoring...\n");
        return; 
    }

    fprintf(stderr, "Valid protocol header received. Length: %d\n", len);

    if (len > 30 && buffer[5] == 'F' && buffer[6] == 'U' && buffer[7] == 'Z' && buffer[8] == 'Z') {
        fprintf(stderr, "Secret path reached! Triggering vulnerability.\n");
        char small_buf[16];
        strcpy(small_buf, buffer + 10);
    }
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    int opt = 1;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }
    
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("Setsockopt failed");
        exit(EXIT_FAILURE);
    }
    
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }
    
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }
    printf("Server listening on port %d...\n", PORT);

    while(1) {
        char buffer[BUFFER_SIZE] = {0};

        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue;
        }
        
        int valread = read(new_socket, buffer, BUFFER_SIZE - 1);
        if (valread > 0) {
            buffer[valread] = '\0';
            printf("Received: %s\n", buffer);
            process_input(buffer, valread);
        }
        close(new_socket);
    }

    return 0;
}