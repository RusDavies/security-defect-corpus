/* C-FMT-001 fixed-version fixture for patch-diff evaluation. */
#include <stdio.h>

static void legacy_log(char *message) {
    printf(message);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        printf("%s", argv[1]);
    }
    return 0;
}
