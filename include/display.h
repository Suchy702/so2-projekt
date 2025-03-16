#pragma once

#include <string>
#include <mutex>

class Display {
public:
    Display();
    ~Display();
    void updateStatus(int philosopherId, const std::string &status);
private:
    std::mutex mtx;
};