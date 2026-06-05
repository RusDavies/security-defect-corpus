/* C-BOF-001 reachable vulnerable fixture. DO NOT DEPLOY. */
#include <stdio.h>
#include <string.h>

void greet(const char *name) {
    char buffer[16];
    strcpy(buffer, name);
    printf("Hello %s\n", buffer);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        greet(argv[1]);
    }
    return 0;
}
