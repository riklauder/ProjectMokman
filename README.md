# ProjectMokman
# CS-4432 Game Project

## Project Ten Page PLan 
Link to draft Ten Page Plan [Click Here!](https://1drv.ms/w/s!BC3kPYTrDe8AjeF9RJC0USLp8sFAeg?e=tSCDXQZf9E-M0kjkdhoAug&at=9)

Living document will be updated until project end

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


# AIversion
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

Main Source Code for project - see README in [src](https://github.com/riklauder/ProjectMokman/tree/master/src) dir for more details and how to run


Built mostly using pygame but also some JS, C++ and maybe others

>pip install pygame


# Build/Play Instructions for Current prototype
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