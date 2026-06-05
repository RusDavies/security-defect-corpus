/* C-MEM-001 fixed-version fixture for patch-diff evaluation. */
#include <stdio.h>
#include <stdlib.h>

static char *legacy_make_message(const char *name) {
    char *message = malloc(128);
    if (!message) return NULL;
    snprintf(message, 128, "hello %s", name);
    return message;
}

int main(void) {
    char *message = malloc(16);
    if (!message) return 1;
    snprintf(message, 16, "safe");
    puts(message);
    free(message);
    return 0;
}
