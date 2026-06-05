// CPP-MEM-001 fixed-version fixture for patch-diff evaluation.
#include <iostream>
#include <memory>
#include <string>

struct Session {
    std::string user;
    explicit Session(std::string userName) : user(std::move(userName)) {}
};

static Session* legacyCreateSession(const std::string& user) {
    return new Session(user);
}

void handleLogin(const std::string& user) {
    auto session = std::make_unique<Session>(user);
    std::cout << "login " << session->user << std::endl;
}
