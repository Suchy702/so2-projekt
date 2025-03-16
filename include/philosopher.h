#pragma once

#include "fork.h"
#include "display.h"

class Philosopher {
private:
    int id;
    int minActionTime;
    int maxActionTime;
    Fork &leftFork;
    Fork &rightFork;
    Display &display;

public:
    Philosopher(int id, Fork &leftFork, Fork &rightFork, Display &display, int minActionTime, int maxActionTime);
    void dine();

private:
    void think();
    void eat();
    int randomTime();
};