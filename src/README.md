# SRC

# Required
1. Python 3.8.1
2. Pygame
>pip install pygame
3. WSL - Windows Subsystem for Linux with g++(should be installed by default)
4. Powershell for running batch files in early project stage

# Source Files

-Map.h 
>draft of class to help build random mazes

-Map.py  
>attempt to recreate mapgen.js in python - likely to be discarded as seems to be more effort than it's worth

-pygamecam.py 
>prototype for movemement controls and camera in pygame.
To run:

*from src dir:

> python pygamecam.py


mapTransform.cpp - transforms final map for pygame and adds Pacman/Ghost spawns.

>compiled as mapt in dir so can be run seperately from PS

>bash -c ./mapt

>*this will transform the map in layouts folder and output to terminal

>to compile from PS > bash -c g++ mapTransform.cpp -o mapt -O3 

>to compile from WSL bash > g++ mapTransform.cpp -o mapt -O3 

>* relies on running node mapgen.js > randommap.lay to output a template map 

mapgen.cpp
>initial draft with Map.h to manage random map creation


mapgen.js 
>script used to generate random maps in JS modified slightly to accomodate project.  Most transformation happens in mapTransform.cpp*


pacman.bat

>batch file to help creaate radnom map, add pacman and ghost spawns then transform it.  Same file exists in AIVersion game to test with full working framework.


*pacman.bat will generate random map using most current method and store it in* 

-    layouts/randomfMap.lay


pycollide.py

>initial prototype to test Pygame collisions and movement

pygamecam.py

>initial prototype for game camera to be implemented in endless gameplay mode.  Camera follow pacman.

>to run

>python pygamecam.py

walls.py
>likely to be thrown away python script that generates random map from half map - maps not consistent with style desired



