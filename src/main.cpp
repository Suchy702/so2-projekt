#include <iostream>
#include <vector>
#include <thread>
#include <cstdlib>   
#include <ctime>     
#include "fork.h"
#include "philosopher.h"
#include "display.h"

int main(int argc, char* argv[]) {
    // Parse command-line arguments
    int numOfPhilosophers = std::stoi(argv[1]);
    int minTime = std::stoi(argv[2]);
    int maxTime = std::stoi(argv[3]);

    // Seed the random number generator
    std::srand(std::time(nullptr));

    // Create Forks, Philosophers, Threads
    std::vector<Fork> forks(numOfPhilosophers);
    std::vector<Philosopher> philosophers;
    std::vector<std::thread> threads;

    // Create a Display instance
    Display display;

    // Initialize philosophers
    for (int i = 0; i < numOfPhilosophers; ++i) {
        philosophers.emplace_back(
            i,
            forks[i],
            forks[(i + 1) % numOfPhilosophers],
            display,
            minTime,
            maxTime
        );
    }

    // Create a thread for each philosopher
    for (int i = 0; i < numOfPhilosophers; ++i) {
        threads.emplace_back(&Philosopher::dine, &philosophers[i]);
    }

    // Join threads, ensuring that the main thread of the program waits for all
    // philosopher threads to complete before the program ends
    for (auto &t : threads) {
        t.join();
    }

    return 0;
}
