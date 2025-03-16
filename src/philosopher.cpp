#include "philosopher.h"
#include <chrono>
#include <thread>
#include <cstdlib>

Philosopher::Philosopher(int id, Fork &leftFork, Fork &rightFork, Display &display, int minActionTime, int maxActionTime)
    : id(id), leftFork(leftFork), rightFork(rightFork), display(display), 
      minActionTime(minActionTime), maxActionTime(maxActionTime) {}

void Philosopher::dine() {
    while (true) {
        think();
        eat();
    }
}

void Philosopher::think() {
    display.updateStatus(id, "Thinking");
    std::this_thread::sleep_for(std::chrono::milliseconds(randomTime()));
}

void Philosopher::eat() {
    // Even philosophers pick up left fork first, odd pick up right fork first
    if (id % 2 == 0) {
        leftFork.pickUp();
        rightFork.pickUp();
    } else {
        rightFork.pickUp();
        leftFork.pickUp();
    }

    display.updateStatus(id, "Eating");
    std::this_thread::sleep_for(std::chrono::milliseconds(randomTime()));

    // Put down forks
    leftFork.putDown();
    rightFork.putDown();
}

int Philosopher::randomTime() {
    int range = maxActionTime - minActionTime + 1;
    return (std::rand() % range) + minActionTime;
}
