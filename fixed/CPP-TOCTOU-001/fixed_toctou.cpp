// CPP-TOCTOU-001 fixed-version fixture for patch-diff evaluation.
#include <fstream>
#include <ios>
#include <string>

void writeIfMissing(const std::string& path) {
    std::ofstream output(path, std::ios::out | std::ios::app);
    output << "created";
}
