cmake_minimum_required(VERSION 3.10)

# Set the project name
project(so2-projekt)

# Find the ncurses package
find_package(Curses REQUIRED)

# Add the executable and include all source files
add_executable(so2-projekt
    src/main.cpp
    src/fork.cpp
    src/philosopher.cpp
    src/display.cpp
)

# Include directories
target_include_directories(so2-projekt PUBLIC ${PROJECT_SOURCE_DIR}/include)

# Link required libraries (threads and ncurses)
target_link_libraries(so2-projekt ${CMAKE_THREAD_LIBS_INIT} ${CURSES_LIBRARIES})
