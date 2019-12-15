#!/bin/sh

if [[ "$1" == "help" ]]; then
	echo ""
	echo "Welcome to the online help"
	echo "Use the following syntax to call the program:"
	echo "./BusRouting.sh <problem-file> <heuristic>"
	echo ""
	echo "<problem-file>: path of the file containing the problem to solve"
	echo "<heuristic>: since our program didn't implement heuristics, this argument may take any value"
	echo ""
	# TODO: list 
	exit 0
fi

if [[ "$#" -ne 2 ]]; then
	echo "Wrong parameters"
	exit -1
fi

echo "Compiling program"
g++ -std=c++14 main.cpp -O3 -o a_star > /dev/null 2>&1

echo "Done"
echo
echo "Obtaining the solution..."
./a_star $1

exit 0
