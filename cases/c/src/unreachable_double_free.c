/* C-DFREE-001 safe paired fixture. */
#include <stdlib.h>

static void legacy_double_free(void) {
    char *buffer = malloc(64);
    if (buffer) {
        free(buffer);
        /* retired vulnerable path would free again, but is never called */
    }
}

int main(void) {
    char *buffer = malloc(64);
    if (!buffer) return 1;
    free(buffer);
    buffer = NULL;
    return 0;
}
