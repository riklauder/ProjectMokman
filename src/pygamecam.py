#! /usr/bin/python

import sys, types, os, random, time, math, heapq, itertools
import pygame as pg
import layout, util, pacmanrules, game
from pygame.locals import *
from pygame import *
from pacman import Directions
from math import sqrt
from pacmanrules import PacmanRules, GhostRules
from game import GameStateData
from game import Game
from game import Agent, Directions
from game import Actions
from util import nearestPoint
from util import manhattanDistance
import threading, multiprocessing
from multiprocessing import Process, current_process

DEBUG = False
WIN_WIDTH = 860
WIN_HEIGHT = 800
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30
SCREEN_SIZE = pg.Rect((0, 0, 860, 800))
TILE_SIZE = 32 
GRAVITY = pg.Vector2((0, 0))
WALL_RADIUS = 24
WALL_WIDTH=3
DIR_UP = 0;
DIR_RIGHT = 1;
DIR_DOWN = 2;
DIR_LEFT = 3;
STOPPED = 4;
SCRIPT_PATH=sys.path[0]
PAC_SPEED = 2
TURNBOOST = 6

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
YELLOW=         (255, 255,   0)
PINK=           (255, 105, 180)
LIGHTBLUE=      (135, 206, 250)
RED=            (255,   0,   0)
LIGHTPINK=      (255, 182, 193)

GHOST_SHAPE = [
    ( 0,    -0.3 ),
    ( 0.25, -0.75 ),
    ( 0.5,  -0.3 ),
    ( 0.75, -0.75 ),
    ( 0.75, 0.5 ),
    ( 0.5,  0.75 ),
    (-0.5,  0.75 ),
    (-0.75, 0.5 ),
    (-0.75, -0.75 ),
    (-0.5,  -0.3 ),
    (-0.25, -0.75 )
    ]
GHOST_SIZE=0.65
GHOST_OFFSET=0.1*WALL_RADIUS

# Must come before pygame.init()
pg.mixer.pre_init(22050,16,2,512)
pg.mixer.init()

pg.init()
#screen = pg.display.set_mode(SCREEN_SIZE.size)
screen = pg.display.set_mode(DISPLAY, FLAGS, DEPTH)
pg.display.set_caption("Mokman! Use arrows to move!")
screenp = pg.display.get_surface()
timer = pg.time.Clock()

snd_pellet = {}
snd_pellet[0] = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","pellet1.wav"))
snd_pellet[1] = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","pellet2.wav"))
snd_powerpellet = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","powerpellet.wav"))
snd_eatgh = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatgh2.wav"))
snd_fruitbounce = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","fruitbounce.wav"))
snd_eatfruit = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatfruit.wav"))
snd_extralife = pg.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","extralife.wav"))

def main():

    up = down = left = right = running = False
    maplay = 'randomfMap'
    level = layout.getLayout(maplay)
    levelt = level.layoutText
    platforms = pg.sprite.Group()
    playerX = getObjectPos(levelt, 'P', 'x')
    playerY = getObjectPos(levelt, 'P', 'y')
    player = Player(platforms, (playerX, playerY))
    level_width  = level.width*TILE_SIZE
    level_height = level.height*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pg.Rect(0, -level_height, level_width, level_height))

    # build the level    
    x = y = 0
    for row in levelt:
        for col in row:
            if col == '%':
                Platform((x, y), platforms, entities)
            if col == 'P':
                player = Player(platforms, (x, y))
            x+=TILE_SIZE
        y+=TILE_SIZE
        x=0

    while True:

        for e in pg.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pg.display.update()
        timer.tick(60)
        

def  add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def getLegalActions(self):
    """
    Returns the legal actions for the agent specified.
    """
    # GameState.explored.add(self)
    #if self.isWin() or self.isLose(): return []
    illegal = []
    plats = self.platforms
    velUL=-self.speed
    velDR=self.speed
    copys = self
    currDir = self.dir
    if currDir == 4:
        velUL = velDR = 0
    #check RIGHT
    if currDir != DIR_LEFT:
        copys.rect.left += velDR
        legalColl(plats, copys, velDR, 0, illegal)
    #check LEFT
    if currDir != DIR_RIGHT:
        copys.rect.left += velUL
        legalColl(plats, copys, velUL, 0, illegal)
    #check DOWN
    if currDir != DIR_UP:
        copys.rect.top += velDR 
        legalColl(plats, copys, 0, velDR, illegal)
    #check UP
    if currDir != DIR_DOWN:
        copys.rect.top += velUL
        legalColl(plats, copys, 0, velUL, illegal)
    
    return illegal

def legalColl(plts, cpys, xvel, yvel, legal):
    for p in plts:
        if pg.sprite.collide_rect(cpys, p):
            if xvel > 0:
                cpys.rect.right = p.rect.left
                legal.append(DIR_RIGHT)
            elif xvel < 0:
                cpys.rect.left = p.rect.right
                legal.append(DIR_LEFT)
            if yvel > 0:
                cpys.rect.bottom = p.rect.top
                legal.append(DIR_DOWN)
            elif yvel < 0:
                cpys.rect.top = p.rect.bottom
                legal.append(DIR_UP)
#DIR_UP = 0   #DIR_RIGHT = 1
#DIR_DOWN = 2 #DIR_LEFT = 3 #STOPPED=4

class CameraAwareLayeredUpdates(pg.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pg.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width/2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height/2
            self.cam += (pg.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width-SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height-SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty            

def getObjectPos(level, char ,coord):
    '''
    returns x or y pos based on 
    coord: of 'x' or 'y' 
    x or y * TILE_SIZE
    '''
    x = y = 0
    for row in level:
        for col in row:
            if col == char:
                if coord == 'x':
                    return x
                if coord == 'y':
                    return y
            x+=TILE_SIZE
        y+=TILE_SIZE
        x=0

def getObjectCoord(self, char):
    '''
    returns x or y pos based on rect pos
    char: of 'x' or 'y' for return
    '''
    if char == 'x':
        return math.ceil(self.rect.left / TILE_SIZE)
    if char == 'y':
        return math.ceil(self.rect.top / TILE_SIZE)

def exit():
    pg.quit()
    sys.exit()

class Entity(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        self.image = pg.Surface((TILE_SIZE-4, TILE_SIZE-4))
        super().__init__(Color("#ebef00"), pos)
        self.dir = None
        self.vel = pg.Vector2((0, 0))
        self.stopped = True
        self.lastDir = 4
        self.platforms = platforms
        self.speed = int(PAC_SPEED)
        self.turning = False
        self.change_x=0
        self.change_y=0

    def getDir(self):
        if (self.vel.x>=1): return DIR_RIGHT
        if (self.vel.x<=-1): return DIR_LEFT
        if (self.vel.y<=-1): return DIR_UP
        if (self.vel.y>=1): return DIR_DOWN
        if (self.vel.y == 0 and self.vel.x == 0): return STOPPED

    def update(self):
        pressed = pg.key.get_pressed()
        up = pressed[K_UP]
        down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]

        currDir = self.getDir()
        self.isTurning(currDir)
        self.setSpeed()
        illegalMoves = getLegalActions(self)
        if self.lastDir != STOPPED and DEBUG == True:
            print("currVselfVLastDir:", currDir, self.dir, self.lastDir)
            print("illegalMoves self.speed", illegalMoves, self.speed)
        self.lastDir = currDir
        if self.stopped == True:
            self.dir = 4
            self.vel.x = 0
            self.vel.y = 0
        if right or self.dir == 1:
            self.dir = 1
            if self.dir not in illegalMoves:
                self.vel.y = 0
                self.vel.x = self.speed
                self.change_x += self.vel.x
                self.stopped = False;
        if left or self.dir == 3:
            self.dir = 3
            if self.dir not in illegalMoves:
                self.vel.y = 0
                self.vel.x = -self.speed
                self.change_x += self.vel.x
                self.stopped = False;
        if up or self.dir == 0:
            self.dir = 0
            if self.dir not in illegalMoves:
                self.vel.x = 0
                self.vel.y = -self.speed
                self.change_y += self.vel.y
                self.stopped = False;
        if down or self.dir == 2:
            self.dir = 2
            if self.dir not in illegalMoves:
                self.vel.x = 0
                self.vel.y = self.speed
                self.change_y += self.vel.y
                self.stopped = False;
        # increment in x direction
        self.rect.left += int(self.vel.x)
        if self.vel.x != 0:
            self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += int(self.vel.y)
        if self.vel.y != 0:
            self.collide(0, self.vel.y, self.platforms)
        #DIR_UP = 0  #DIR_RIGHT = 1 #DIR_DOWN = 2  #DIR_LEFT = 3
        #STOPPED = 4

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):       
                curDir = self.getDir()
                if isinstance(p, ExitBlock):
                    pg.event.post(pg.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    #self.xvel = 0
                    if curDir == 1:
                        self.stopped = True
                elif xvel < 0:
                    self.rect.left = p.rect.right
                    #self.xvel = 0
                    if curDir == 3:
                        self.stopped = True
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    #
                    if curDir == 2:
                        self.stopped = True
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                    #self.yvel = 0
                    if curDir == 0:
                        self.stopped = True
        #DIR_UP = 0  #DIR_RIGHT = 1  #DIR_DOWN = 2  #DIR_LEFT = 3
        #STOPPED = 4
    def isTurning(self, cDir):
        if (cDir != self.dir):
            self.turning = True
        else: self.turning = False
    def setSpeed(self):
        if self.turning == True:
            self.speed = int(TURNBOOST)
        else: self.speed = int(PAC_SPEED)

    def a(self):
        #axis of motion
        if self.dir.x != 0:
            return 'x'
        else:
            return 'y'

    def b(self):
        #axis perpinidicual to motion
        if self.dir.x != 0:
            return 'y'
        else:
            return 'x'

    def drawGhost(self, surf, direction=None, index=0):
        (x,y)=add(self.game.ghostPos[0],(.5,.5))
        coords=[]
        w_r=WALL_RADIUS*GHOST_SIZE
        offset=WALL_RADIUS*(1-GHOST_SIZE)
        for (x1, y1) in GHOST_SHAPE:
            offsetX=x*offset
            offsetY=y*offset
            screen_x=int((x-x1)*w_r+offsetX)
            screen_y=int((y-y1)*w_r+offsetY)
            coords.append((screen_x,screen_y))

        offsetX=x*offset
        offsetY=y*offset
        dx_left=int((x-.3/1.5)*w_r+offsetX)
        dx_right=int((x+.5/1.5)*w_r+offsetX)
        dy=int((y-.3/1.5)*w_r+offsetY)
        dx_left_pupil = int((x-.35/1.5) * w_r+offsetX)
        dx_right_pupil = int((x+.55/1.5) * w_r+offsetX)
        dy_pupil = int((y-.25/1.5) * w_r+offsetY)
        leftEye = (dx_left,dy)
        rightEye = (dx_right,dy)
        leftPupil = (dx_left_pupil,dy_pupil)
        rightPupil = (dx_right_pupil,dy_pupil)
        pg.draw.polygon(surf, self.color, coords)
        pg.draw.circle(surf, WHITE, leftEye, int(WALL_RADIUS*GHOST_SIZE*.4), 0)
        pg.draw.circle(surf, WHITE, rightEye, int(WALL_RADIUS*GHOST_SIZE*.4), 0)
        pg.draw.circle(surf, BLACK, leftPupil, int(WALL_RADIUS*GHOST_SIZE*.22), 0)
        pg.draw.circle(surf, BLACK, rightPupil, int(WALL_RADIUS*GHOST_SIZE*.22), 0)

class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0000FF"), pos, *groups)

class ExitBlock(Platform):
    def __init__(self, pos, *groups):
        super().__init__(Color("#ebef00"), pos, *groups)

class pacman ():
	
	def __init__ (self):
		self.x = 0
		self.y = 0
		self.velX = 0
		self.velY = 0
		self.speed = 2
		
		self.nearestRow = 0
		self.nearestCol = 0
		
		self.homeX = 0
		self.homeY = 0
		
		self.anim_pacmanL = {}
		self.anim_pacmanR = {}
		self.anim_pacmanU = {}
		self.anim_pacmanD = {}
		self.anim_pacmanS = {}
		self.anim_pacmanCurrent = {}
		
		for i in range(1, 9, 1):
			self.anim_pacmanL[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-l " + str(i) + ".gif")).convert()
			self.anim_pacmanR[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-r " + str(i) + ".gif")).convert()
			self.anim_pacmanU[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-u " + str(i) + ".gif")).convert()
			self.anim_pacmanD[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-d " + str(i) + ".gif")).convert()
			self.anim_pacmanS[i] = pg.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman.gif")).convert()

		self.pelletSndNum = 0
		
	def Draw (self):
				
		# set the current frame array to match the direction pacman is facing
		if self.velX > 0:
			self.anim_pacmanCurrent = self.anim_pacmanR
		elif self.velX < 0:
			self.anim_pacmanCurrent = self.anim_pacmanL
		elif self.velY > 0:
			self.anim_pacmanCurrent = self.anim_pacmanD
		elif self.velY < 0:
			self.anim_pacmanCurrent = self.anim_pacmanU
			
		screenp.blit (self.anim_pacmanCurrent[ self.animFrame ], (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))
		
		if thisGame.mode == 1:
			if not self.velX == 0 or not self.velY == 0:
				# only Move mouth when pacman is moving
				self.animFrame += 1	
			
			if self.animFrame == 9:
				# wrap to beginning
				self.animFrame = 1
			

if __name__ == "__main__":
    main()