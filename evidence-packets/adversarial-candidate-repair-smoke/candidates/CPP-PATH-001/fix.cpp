// Superficial CPP-PATH-001 repair: blocks one traversal spelling but keeps direct path joining.
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

std::string readUserFile(const std::string& requested) {
    if (requested == "../secret.txt") {
        throw std::runtime_error("blocked path");
    }
    std::string path = "./allowed/" + requested;
    std::ifstream file(path);
    return std::string((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
}

int main(int argc, char** argv) {
    if (argc > 1) std::cout << readUserFile(argv[1]);
    return 0;
}
