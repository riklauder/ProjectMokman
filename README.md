# ProjectMokman
# CS-4432 Game Project

## Project Ten Page Plan 
Link to draft Ten Page Plan [Click Here!](https://1drv.ms/w/s!BC3kPYTrDe8AjeF9RJC0USLp8sFAeg?e=tSCDXQZf9E-M0kjkdhoAug&at=9)

Living document will be updated until project end - Contains details of project design and lessons learned

Map Analysis [Click Here](https://1drv.ms/x/s!Ai3kPYTrDe8Aj4QXeZNKA7SK2G1UnA?e=kCqbm4)

Project Scedule and Story Planning [click here](https://1drv.ms/x/s!Ai3kPYTrDe8Aj4VHUD1C-X5nfQ5vfA?e=CYuuac)

## Project Description
Pacman Clone for undergrad game project

| Feature       | detail        | 
| ------------- |:-------------:| 
| Stealth focus | Ghosts will have different behaviours and spawning than OG game| 
| Maze Generation | Automatically generate random pacman style mazes   |
| Endless Mode | Game will go on infinitely with randomly created mazes with authentic Pacman style | 
| Power Ups | Power-ups and 256-combo(like in pacman 356 )  |


## AIversion
[AIversion](https://github.com/riklauder/ProjectMokman/tree/master/AIversion)
Conatins Berkely Pacman AI project (modified to work with Python 3 and this project).  This framework was used for AI project last year.
This is the project that helped spark curiosity and project idea.


# design
[design](https://github.com/riklauder/ProjectMokman/tree/master/design)
contains design documents - pdf UML - created using combination of Pylint and Pyreverse
>Pylint can be installed with pip

>pip install pylint

# ref
Contains reference code and documents from other sources
[ref](https://github.com/riklauder/ProjectMokman/tree/master/ref)


# src
[src](https://github.com/riklauder/ProjectMokman/tree/master/src)

Main Source Code for project - see additional README in [src](https://github.com/riklauder/ProjectMokman/tree/master/src) dir for more details and how to run


Built mostly using pygame but also used JS and C++

>pip install pygame



# Build/Play Instructions for Latest Build
*Generates random endless map consistent to OG Pacman and Ms Pacman level style*

*Will spawn Ghosts and Pacman Map, Food, Power Ups and Teleports*


1.  cd into src directory from PowerShell(Admin)

>cd src

2.  run ./mokman from that dir

>./mokman

### creates random map for Pygame based game. Transformation of maps is done using C++ .

*pacman batch file will execute required scripts, run code then automatically start pygame. MUST BE run from correct dir

*used WSL bash shell in Windows with g++ although mapTransform.cpp could be compiled as mapt.exe using VS cl or other Windows c++ compiler 
*included mapTransform.exe - run mokmanw.bat if WSL is not installed



## Build/Play Instructions for prototype
*Generates random map consistent to OG Pacman and Ms Pacman level style*

*Will spawn Ghosts and Pacman using tkinter framework found in AIversion*


1.  cd into AIVersion directory from PowerShell(Admin)

>cd AIversion

2.  run ./pacman from that dir

>./pacman

### creates random map for Python based game. Transformation of map strings using C++ .

*batch file will execute code then automatically start python game if run from correct dir

*requires WSL bash shell with g++ installed although could likely be compiled to mapt.exe using VS or Windoes based  


*working project and more details in README in [src](https://github.com/riklauder/ProjectMokman/tree/master/src) dir


Camera and Movement Controls Implementation
cd into src folder src
>cd src


>pytyhon pygamecam.py