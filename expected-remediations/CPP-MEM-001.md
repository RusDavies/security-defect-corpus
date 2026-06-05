# Expected Remediation: CPP-MEM-001

- Replace raw owning pointers with RAII types such as `std::unique_ptr` or stack allocation.
- Ensure all ownership paths release memory deterministically.
- Add leak-check evidence using AddressSanitizer, Valgrind, or equivalent tooling where practical.
- Prefer constructor/destructor or smart-pointer ownership over manual `new`/`delete` pairs.
