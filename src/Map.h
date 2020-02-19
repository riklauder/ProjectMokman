
#ifndef MAP
#define MAP
#include <iostream>
#include <vector>

using std::string;

class Map{
public:	
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




class mapgen{
public:
	mapgen() {}
	mapgen(){
		
		
		
		
		
	}

	int randomInt;
	Dir UP = setDirFromEnum(UP, 0);
	Dir RIGHT = setDirFromEnum(RIGHT, 1);
	Dir DOWN = setDirFromEnum(DOWN, 2);
	Dir LEFT = setDirFromEnum(LEFT, 3);

	int rows = 9;
	int cols = 5;

};

#endif