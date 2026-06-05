// CPP-PATH-001 reachable vulnerable fixture. DO NOT DEPLOY.
#include <fstream>
#include <iostream>
#include <string>

std::string readUserFile(const std::string& requested) {
    std::string path = "./allowed/" + requested;
    std::ifstream file(path);
    return std::string((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
}

int main(int argc, char** argv) {
    if (argc > 1) std::cout << readUserFile(argv[1]);
    return 0;
}
