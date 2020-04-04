# SRC


# Source Files


To run:

*from src dir:

> python mokman.py

will run game with last generated random maze


mapTransform.cpp - transforms final map for pygame and adds Pacman/Ghost spawns and teleports

>compiled as mapt in dir so can be run seperately from PS

>bash -c ./mapt

>*this will transform the map in layouts folder and output to terminal

>to compile from PS > bash -c g++ mapTransform.cpp -o mapt -O3 

>to compile from WSL bash > g++ mapTransform.cpp -o mapt -O3 

>* relies on running node mapgen.js > randommap.lay to output a template map 




mapgen.js 
>script used to generate random maps. modified to accomodate project.  Output is then transformed using mapTransform.cpp compiled as mapt*


mokman.bat

>batch file to run full game. Creaates radnom map, pacman and ghost spawns then transforms it for pygame. This will autostart the game after levels created. Same file pacman.bat exists in AIVersion game to test with full working framework.

>./mokman

or double click in directory

*mokman.bat will generate random map using most current method and store it in* 

-    layouts/randomfMap.lay


mokmanw.bat

>created sript for windows only that doesn't require WSL

>./mokmanw

mokman.py

>core code including main loop for mokman game.  Can run independently using last random map generated using 

>python3 mokman.py




# Other project src files - from prototype - not used in final build

-food.py

>collision detection framework prototype  - will modify for food Mokman game

-game.py

>game state and observer based classes - work in progress

-various Agent py files
>may borrow some classes and functions from these

-util.py
>some useful funtions data structures for python like manhattan distance, priority queue, etc

data res and roundrects dir
>experimental support files - will be cleaned up as project progresses

-joystick.py
>pygame code to implement controller support. This tests and ouputs input from all buttons and axes that can be mapped to game functions.

-layout.py
>python objects used to help build and populate mazes in pygamecam.pu

-mapgen.cpp

>initial draft with Map.h to manage random map creation

-Map.h 
>draft of class to help build random mazes

-Map.py  
>attempt to recreate mapgen.js in python - likely to be discarded as seems to be more effort than it's worth

-pycollide.py

>initial prototype to test Pygame collisions and movement

-pygamecam.py

>initial prototype for game camera to be implemented in endless gameplay mode.  Camera follow pacman.

>to run

>python pygamecam.py

-walls.py
>python code that generates random maps from half map - maps are not consistent with desired authentic pacman style.  Was used in prototype phase only


# Required dependecies
1. Python 3.7 or higher
also install packages if not part of your current distribution:
>pip install numpy
>pip install Naked

2. Pygame 1.9.6
>pip install pygame

3. (optional)WSL - Windows Subsystem for Linux (g++ is installed with deafult Ubuntu LTS packages)
4. Powershell or BASH for running scripts