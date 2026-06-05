// CPP-TOCTOU-001 reachable TOCTOU fixture. DO NOT DEPLOY.
#include <filesystem>
#include <fstream>
#include <string>

void writeIfMissing(const std::string& path) {
    if (!std::filesystem::exists(path)) {
        std::ofstream output(path);
        output << "created";
    }
}
