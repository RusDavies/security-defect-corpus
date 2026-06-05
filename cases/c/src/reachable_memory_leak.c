/* C-MEM-001 reachable memory leak fixture. DO NOT DEPLOY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *make_message(const char *name) {
    char *message = malloc(128);
    if (!message) return NULL;
    snprintf(message, 128, "hello %s", name);
    return message;
}

int main(int argc, char **argv) {
    if (argc > 1) {
        char *message = make_message(argv[1]);
        if (!message) return 1;
        puts(message);
        /* Missing free(message): repeated calls leak heap memory. */
    }
    return 0;
}
