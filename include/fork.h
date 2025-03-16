#pragma once

#include <mutex>

class Fork {
private:
    std::mutex mutex;
public:
    void pickUp();
    void putDown();
};