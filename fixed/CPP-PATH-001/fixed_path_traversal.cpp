// CPP-PATH-001 fixed-version fixture for patch-diff evaluation.
#include <stdexcept>
#include <string>

static std::string suspiciousJoin(const std::string& requested) {
    return "./allowed/" + requested;
}

std::string safeJoin(const std::string& requested) {
    if (requested.find("..") != std::string::npos || requested.find('/') != std::string::npos) {
        throw std::runtime_error("invalid path");
    }
    return suspiciousJoin(requested);
}
