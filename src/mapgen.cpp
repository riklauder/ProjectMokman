#include <iostream>
#include <algorithm>
#include <vector>
#include <limits>
#include <string>
#include <iterator>
#include <functional>
#include <iomanip>
#include <numeric>
#include <cerrno>
#include <ctime>
#include <cstdlib>
#include <deque>
#include <utility>
#include <execution>
#include <execution>
#include <cstdio>
#include <charconv>
#include <cmath>


using std::string;

#define DIR_UP = 0
#define DIR_RIGHT = 1;
#define DIR_DOWN = 2;
#define DIR_LEFT = 3;

/*Structure to handle coords, dir, points and vector math*/
struct Dir{
	double x, y;
	Dir& operator += (const Dir a) { x += a.x; y += a.y; return *this;}
};
bool operator==(const Dir a, const Dir b) { return a.x == b.x && a.y == b.y; }
bool operator<(const Dir a, const Dir b) { return (a.x != b.x) ? (a.x < b.x) : (a.y < b.y); }
Dir operator +(const Dir a, const Dir b) { return Dir{ a.x + b.x, a.y + b.y }; }

// get direction enum from a direction vector
int getEnumFromDir (Dir &dir) {
    if (dir.y==-1) return 0; //DIR_UP
	if (dir.x==1) return 1; //DIR_RIGHT;
	if (dir.y==1) return 2; //DIR_DOWN;
	if (dir.x==-1) return 3; //DIR_LEFT;  
};
// set direction vector from a direction enum
Dir setDirFromEnum(Dir &dir, int dirEnum){
  	if (dirEnum == 0)         { dir.x = 0; dir.y =-1; }
    else if (dirEnum == 1)  { dir.x =-1; dir.y = 0; }
    else if (dirEnum == 2)  { dir.x = 0; dir.y = 1; }
    else if (dirEnum == 3) { dir.x = 1; dir.y = 0; }
};

#include "Map.h"


int main(){
	const static int tileSize = 8;
	/*todo func for ghosts*/
	Dir midTile;
	midTile.x = 3, midTile.y = 4;
	Dir pacman;
	pacman.x = 14*tileSize-1;
	pacman.y = 26*tileSize + midTile.y;




}