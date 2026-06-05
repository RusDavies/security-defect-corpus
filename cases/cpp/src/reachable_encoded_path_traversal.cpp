// CPP-ENC-PATH-001 reachable encoded path traversal fixture. DO NOT DEPLOY.
#include <string>

std::string buildPath(const std::string& requested) {
    if (requested.find("..") != std::string::npos) throw "blocked";
    return "./allowed/" + requested;
}
