// CPP-MEM-001 reachable memory leak fixture. DO NOT DEPLOY.
#include <iostream>
#include <string>

struct Session {
    std::string user;
    explicit Session(std::string userName) : user(std::move(userName)) {}
};

void handleLogin(const std::string& user) {
    Session* session = new Session(user);
    std::cout << "login " << session->user << std::endl;
    // Missing delete: repeated login handling leaks Session objects.
}

int main(int argc, char** argv) {
    if (argc > 1) handleLogin(argv[1]);
    return 0;
}
