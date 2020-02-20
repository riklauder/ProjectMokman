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

void getData(std::vector<std::string>& data) {
	std::string s1;
	int rows=31;
	int cols=28;
	std::ifstream file("layouts/randomMap.lay");
	getline(file, s1);
	for (int i=0; i < rows;i++) {
		std::string s2 ="";
		if (i==0 || i == rows-1)
			s2.append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
		else{
			s2.append("%");
			s2.append(s1.substr((i*cols)+1, cols-2));
			s2.append("%");	
		}
		std::replace(s2.begin(), s2.end(), '|', '%');
		data.push_back(s2);
			}
	
	}



int main(){
	std::vector<std::string> map;

	getData(map);

	map[23][14]='P';
	for (auto x : map)
		std::cout << x << std::endl;

}
