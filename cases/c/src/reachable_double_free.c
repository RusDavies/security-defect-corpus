/* C-DFREE-001 reachable double-free fixture. DO NOT DEPLOY. */
#include <stdlib.h>

int main(void) {
    char *buffer = malloc(64);
    if (!buffer) return 1;
    free(buffer);
    free(buffer); /* double free */
    return 0;
}
