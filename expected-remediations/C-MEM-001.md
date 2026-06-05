# Expected Remediation: C-MEM-001

- Free heap allocations on all successful and error paths.
- Prefer ownership conventions that make responsibility explicit.
- Add leak-check evidence using AddressSanitizer, Valgrind, or an equivalent tool where practical.
- Add regression coverage for normal and early-return paths.
