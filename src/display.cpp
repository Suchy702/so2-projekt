#include "display.h"
#include <ncurses.h>

Display::Display() {
    initscr();      // Start ncurses mode
    noecho();       // Disable user input
    curs_set(0);    // Hide the cursor
    start_color();  // Enable color functionality
    
    // Initialize color pairs (ID, foreground, background)
    init_pair(1, COLOR_GREEN, COLOR_BLACK);  // For "Thinking"
    init_pair(2, COLOR_RED, COLOR_BLACK);    // For "Eating"

    // Clear the screen and refresh
    clear();
    refresh();
}

Display::~Display() {
    endwin(); // End ncurses mode
}

void Display::updateStatus(int philosopherId, const std::string &status) {
    // Lock the mutex to prevent multiple threads from writing to the screen at the same time
    // and unlocking it when the function ends
    std::lock_guard<std::mutex> lock(mtx);

    // Determine which color pair to use based on the status
    int colorPair = 0;
    if (status == "Thinking") {
        colorPair = 1;
    } else if (status == "Eating") {
        colorPair = 2;
    }

    // Move cursor to the begginning philosopher's line
    move(philosopherId, 0);
    // clear line
    clrtoeol();
    // Apply color
    attron(COLOR_PAIR(colorPair));
    // Print the updated status
    printw("Philosopher %d: %s", philosopherId, status.c_str());
    // Turn off color
    attroff(COLOR_PAIR(colorPair));

    refresh();
}
