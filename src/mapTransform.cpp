#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <iterator>
#include <iomanip>
#include <numeric>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <sstream>
#include <limits>
#include <iterator>

void getData(std::vector<std::string>& data, std::string fname) {
	std::string s1;
	int rows=31;
	int cols=28;
	std::ifstream file(fname);
	getline(file, s1);
	for (int i=1; i < rows-1;i++) {
		std::string s2 ="";
		
			if (s1.substr(i*cols,1) == " ")
				s2.append("T");
			else 
				s2.append("%");
			s2.append(s1.substr((i*cols)+1, cols-2));
			if (s1.substr(i*cols,1) == " ")
				s2.append("T");
			else
				s2.append("%");	

		std::replace(s2.begin(), s2.end(), '|', '%');
		std::replace(s2.begin(), s2.end(), '_', ' ');
		std::replace(s2.begin(), s2.end(), '-', ' ');
		data.push_back(s2);
			}
	
	}

std::string filename(int n){
	std::stringstream str;
	str << n;
	std::string fname = "layouts/randomMap";
	fname += str.str();
	fname += ".lay";
	return fname;
}


int main(){
	std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << std::endl;
	for (int i=0; i <= 12; i++){
		std::vector<std::string> map;
		std::string file = filename(i);
		getData(map, file);

		if (i == 11){
			map[16][18]='W';
			map[16][9]='W';
		}
		if (i == 12){
			map[22][14]='P';
			map[10][18]='B';//one ghost always spawn in house
			/*2 ghosts spawn on north side of map*/
			map[16][9]='C';
			map[0][3]='S';
			map[0][24]='S';
			/*random L R spawn south end*/
		}
		map.resize(27);
		for (auto x : map)
			std::cout << x << std::endl;
	}
	std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << std::endl;
}
