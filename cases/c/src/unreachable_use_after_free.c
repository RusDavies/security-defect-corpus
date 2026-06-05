/* C-UAF-001 safe paired fixture. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void legacy_uaf(void) {
    char *token = malloc(32);
    free(token);
    (void)token;
}

int main(void) {
    char *token = malloc(32);
    if (!token) return 1;
    strcpy(token, "session-token");
    printf("token=%s\n", token);
    free(token);
    return 0;
}
