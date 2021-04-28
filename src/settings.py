#Configurations settings - global variables and macros

import os, sys
import pygame as pg
import util
from pygame.locals import *

DEBUG= False
TRUE = True
FALSE = False
#Currently game is set by these paramters so do not change for scaling purpose
#Use pygame api to resize
WIN_WIDTH = 648 
WIN_HEIGHT = 672
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
#DEPTH = 32 used to set depth in pygame - used to test 32 or 64 bit
#FLAGS = 1
SCREEN_SIZE = pg.Rect((0, 0, WIN_WIDTH, WIN_HEIGHT))
TILE_SIZE = 24
GRAVITY = pg.Vector2((0, 0))
WALL_RADIUS = 16
WALL_WIDTH = 3
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3
STOPPED = 4
SCRIPT_PATH = sys.path[0]
#May need to adjust these speed vars depending on system 
#PAC_SPEED=3, GHOST=3 also or 2 if too fast
PAC_SPEED = 3 
GHOST_SPEED = 2
TURNBOOST = 2
SCORE_XOFFSET=14 # pixels from left edge
SCORE_YOFFSET=14 # pixels from bottom edge (to top of score)
SCORE = 0
#interval at which ghosts cycle through states
GHOSTSFREE = 100 # ghosts in randon browse state
GHOSTINT=300 #interval at which ghosts cycle through states
#note 300 is equivalent to about 10 seconds in 30/60 frametime
GHOSTSSCARED=320 #interval for which ghosts stay scared
#Will activatae combo bonus feature tense sound in background while combo builds - sound stops
# if progress towards combo stops 
COMBOSOUND = False

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

JS_DEVNUM=0 # device 0 (pygame joysticks always start at 0). if JS_DEVNUM is not a valid device, will use 0
JS_XAXIS=0 # axis 0 for left/right (default for most joysticks)
JS_YAXIS=1 # axis 1 for up/down (default for most joysticks)
JS_STARTBUTTON=9 # button number to start the game. this is a matter of personal preference, and will vary from device to device

#        R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3,  54,  73)
GREEN = "#32CD32"
YELLOW = (255, 255,   0)
PINK = "#FF1493"
LIGHTBLUE = "#00BFFF"
RED = "#FF0000"
LIGHTPINK = (255, 182, 193)
ORANGE = "#FFA500"
PURPLE = "#EE82EE"
#FLAGS = pg.DOUBLEBUF | pg.HWACCEL | pg.ASYNCBLIT | pg.HWSURFACE | pg.HWPALETTE

COLLISION_TOLERANCE = 0.7 # How close ghosts must be to Pacman to kill


