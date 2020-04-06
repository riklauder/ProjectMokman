# SRC


# Source Files


To run:

*from src dir:
>cd src

> python mokman.py

this will run the game with last generated random maze


## File Details 
mapTransform.cpp - transforms final map for pygame and adds Pacman/Ghost spawns and teleports

>compiled as mapt in dir so can be run seperately from PS

>bash -c ./mapt

>*this will transform the map in layouts folder and output to terminal

>to compile from PS > bash -c g++ mapTransform.cpp -o mapt -O3 

>to compile from WSL bash > g++ mapTransform.cpp -o mapt -O3 

>* updated in scripts to output a new random map using python and launch game

mokman.py

>Bulk code including **main loop** for mokman game.  Can run independently using last random map generated using 
> This is where most of the code is.  Pygame doesn't seem to like it when things are moved into seperate modules.

>python3 mokman.py


astartwo.py
>This is the implementation of astar used by the ghosts to find pacman

gamestate.py
>Class that copies it's predecessor state when called so that game objects can call common
>game state related functions - like updating score, getting map deatils, etc.

settings.py
>Global variables and settings for configuration of the game
>Things like ghosts scared timers and intervals can be configured in this file

-util.py
>some useful funtions data structures for python like manhattan distance, priority queue, etc

layout.py
>File to help loading in map details and building a list object that can be used as refernce to game state by game objects

mapgen.js 
>script used to generate random maps. modified to accomodate project.  Output is then transformed using mapTransform.cpp compiled as mapt*

mokman.bat and mokman.sh

>batch files to run game. Creaates radnom map, pacman and ghost spawns then transforms it for pygame. This will autostart the game after levels created. 
>cs src
>./mokman
>./mokman.sh or
>bash mokman.sh

or double click in directory

*mokman.bat will generate random map using most current method and store it as* 

-    layouts/randomfMap.lay

particle.py
>attempted to build some effects to add some flair to the game - didn't work :(

various *.prof files
>used to profile code at various phases of project

eventman.py
>event manaager that was implemented but didn't improve anything.  Found it was easier using the Player class as the event manager since all event behaviours invovle the player somehow. Didn't seem worthwhile.



# Other project src files - from prototype - not used in final build

-food.py

>collision detection framework prototype  - will modify for food Mokman game

-fruit.py 
>did not have time to implement

-game.py

>some game state and observer based classes - only using to help create Grid data structure in layout

-various Agent py files
>may borrow some classes and functions from these


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

>initial early prototype for game camera to be implemented in endless gameplay mode.  Camera follow pacman.

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