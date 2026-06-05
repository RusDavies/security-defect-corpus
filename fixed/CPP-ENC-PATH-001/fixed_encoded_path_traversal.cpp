// CPP-ENC-PATH-001 fixed-version fixture for patch-diff evaluation.
#include <algorithm>
#include <stdexcept>
#include <string>

std::string percentDecodeOnce(std::string value) {
    // Fixture stub: real code should use a reviewed decoder.
    std::replace(value.begin(), value.end(), '%', '_');
    return value;
}

std::string buildPath(const std::string& requested) {
    std::string decoded = percentDecodeOnce(requested);
    if (decoded.find("..") != std::string::npos || decoded.find('/') != std::string::npos || decoded.find('\\\\') != std::string::npos) {
        throw std::runtime_error("blocked");
    }
    return "./allowed/" + decoded;
}
