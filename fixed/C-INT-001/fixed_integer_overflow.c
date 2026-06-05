/* C-INT-001 fixed-version fixture for patch-diff evaluation. */
#include <stdint.h>
#include <stdlib.h>
#include <limits.h>

void *allocate_records(uint32_t count) {
    if (count > SIZE_MAX / 64) return NULL;
    return malloc((size_t)count * 64);
}

int main(void) {
    void *records = allocate_records(10);
    free(records);
    return 0;
}
