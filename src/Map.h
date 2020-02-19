
#ifndef Map
#define Map
#include <iostream>
#include <vector>

using std::string;

class Map{
	Map() {}
	Map(const int &numCols, const int &numRows){
		this -> numCols = numCols;
		this -> numRows = numRows;
		numTiles = numCols*numRows;
	}


	int numCols;
	int numRows;
	int numTiles;
	std::vector<string> tiles;

};

#endif