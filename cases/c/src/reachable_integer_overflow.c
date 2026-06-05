/* C-INT-001 reachable integer overflow fixture. DO NOT DEPLOY. */
#include <stdint.h>
#include <stdlib.h>

void *allocate_records(uint32_t count) {
    uint32_t bytes = count * 64; /* overflow can under-allocate */
    return malloc(bytes);
}

int main(void) {
    void *records = allocate_records(0xFFFFFFFFu);
    free(records);
    return 0;
}
