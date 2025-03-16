#!/bin/bash
# make build folder if it doesn't exist
mkdir -p build

# go to build folder
cd build

# run cmake and make
cmake ..
make

# pass the command line arguments to the program
./so2-projekt "$@"
