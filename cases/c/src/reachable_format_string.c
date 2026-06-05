/* C-FMT-001 reachable format string fixture. DO NOT DEPLOY. */
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc > 1) {
        printf(argv[1]); /* attacker-controlled format string */
    }
    return 0;
}
