#include "fork.h"

void Fork::pickUp() {
    mutex.lock();
}

void Fork::putDown() {
    mutex.unlock();
}
