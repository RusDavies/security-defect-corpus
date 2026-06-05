/* C-BOF-001 unreachable paired fixture. */
#include <stdio.h>
#include <string.h>

static void retired_copy(const char *input) {
    char buffer[16];
    strcpy(buffer, input);
    printf("%s\n", buffer);
}

int main(void) {
    puts("safe path only");
    return 0;
}
