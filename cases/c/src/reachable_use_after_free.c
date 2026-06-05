/* C-UAF-001 reachable use-after-free fixture. DO NOT DEPLOY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *token = malloc(32);
    if (!token) return 1;
    strcpy(token, "session-token");
    free(token);
    printf("token=%s\n", token); /* use after free */
    return 0;
}
