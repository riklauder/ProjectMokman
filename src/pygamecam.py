#! /usr/bin/python

import sys, os, pygame
import random
from pygame import *
from math import sqrt

SCREEN_SIZE = pygame.Rect((0, 0, 740, 800))
TILE_SIZE = 32 
GRAVITY = pygame.Vector2((0, 0))
WALL_RADIUS = 24
WALL_WIDTH=3
DIR_UP = 0;
DIR_RIGHT = 1;
DIR_DOWN = 2;
DIR_LEFT = 3;

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

def  add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width/2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height/2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
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

def exit():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    level = [
		"%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
		"%      %%          %%      %",
		"% %%%% %% %%%%%%%% %% %%%% %",
		"% %%%% %% %%%%%%%% %% %%%% %",
		"%                          %",
		"%%% %% %%%%% %% %%%%% %% %%%",
		"%%% %% %%%%% %% %%%%% %% %%%",
		"%%% %% %%%%% %% %%%%% %% %%%",
		"    %%       %%       %%    ",
		"%%% %%%%% %%%%%%%% %%%%% %%%",
		"%%% %%%%% %%%%%%%% %%%%% %%%",
		"%%%                      %%%",
		"%%% %%%%% %%%  %%% %%%%% %%%",
		"%%% %%%%% %      % %%%%% %%%",
		"%%% %%    %      %    %% %%%",
		"%%% %% %% %%%%%%%% %% %% %%%",
		"       %%          %%       ",
		"%%% %%%%%%%% %% %%%%%%%% %%%",
		"%%% %%%%%%%% %% %%%%%%%% %%%",
		"%%%          %%          %%%",
		"%%% %%%%% %%%%%%%% %%%%% %%%",
		"%%% %%%%% %%%%%%%% %%%%% %%%",
		"%                          %",
		"% %%%% %%%%% %% %%%%% %%%% %",
		"% %%%% %%%%% %% %%%%% %%%% %",
		"% %%%% %%    %%    %% %%%% %",
		"% %%%% %% %%%%%%%% %% %%%% %",
		"% %%%% %% %%%%%%%% %% %%%% %",
		"%                          %",
		"%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
		]


    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE))
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, -level_height, level_width, level_height))

    # build the level
    x = y = 0
    for row in level:
        for col in row:
            if col == "%":
                Platform((x, y), platforms, entities)
            if col == "E":
                ExitBlock((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    while 1:

        for e in pygame.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()

        entities.update()

        screen.fill((0, 0, 0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#ebef00"), pos)
        self.dir = 3
        self.vel = pygame.Vector2((0, 0))
        self.stopped = True
        self.platforms = platforms
        self.speed = 5
        #self.jump_strength = 10

    def getDir(self):
        if (self.vel.x==-1): return DIR_LEFT
        if (self.vel.x==1): return DIR_RIGHT
        if (self.vel.y==-1): return DIR_UP
        if (self.vel.y==1): return DIR_DOWN

    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]


        if up:
            self.dir = 0
            # do x-y axis collisions
            self.collide(0, self.vel.y, self.platforms)
            #if self.stopped == False:
            #self.vel.x = 0
            self.vel.y = -self.speed
        if left:
            self.dir = 3
            # do x-y axis collisions
            self.collide(self.vel.x, 0, self.platforms)
            #if self.stopped == False:
            self.vel.x = -self.speed
            #self.vel.y = 0
        if down:
            self.dir = 2
            # do x-y axis collisions
            self.collide(0, self.vel.y, self.platforms)
            #if self.stopped == False:
            #self.vel.x = 0
            self.vel.y = self.speed
        if right:
            self.dir = 1
            # do x-y axis collisions
            self.collide(self.vel.x, 0, self.platforms)
            #if self.stopped == False:
            self.vel.x = self.speed
            #self.vel.y = 0
        # increment in x direction
        self.rect.left += int(self.vel.x)
        self.stopped = False;
        self.collide(self.vel.x, 0, self.platforms)
        self.stopped = False;
        # increment in y direction
        self.rect.top += int(self.vel.y)
        self.collide(0, self.vel.y, self.platforms)
        # assuming we're in the air

            #self.vel.y = 0

        #if self.collide(0, self.vel.y, self.platforms):
            #self.vel.x = 0

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):       
                curDir = self.dir
                #print("post:xvel:yvel",xvel, yvel)
                #print("player.vel", self.vel)
                #print("PLAUER:top:btm:lft:rigt",self.rect.top,self.rect.bottom,self.rect.left,self.rect.right)
                #print("P:top:bottom:left:right",p.rect.top,p.rect.bottom,p.rect.left,p.rect.right)
                #print("CurDir:", curDir)
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    if curDir == DIR_LEFT:
                        #self.vel.x = 0
                        self.stopped = True
                elif xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    if curDir == DIR_RIGHT:
                        #self.vel.x = 0
                        self.stopped = True
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                    if curDir == DIR_DOWN:
                        #self.vel.y = 0
                        self.stopped = True
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    if curDir == DIR_UP:
                        #self.vel.y = 0
                        self.stopped = True

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
        pygame.draw.polygon(surf, self.color, coords)
        pygame.draw.circle(surf, WHITE, leftEye, int(WALL_RADIUS*GHOST_SIZE*.4), 0)
        pygame.draw.circle(surf, WHITE, rightEye, int(WALL_RADIUS*GHOST_SIZE*.4), 0)
        pygame.draw.circle(surf, BLACK, leftPupil, int(WALL_RADIUS*GHOST_SIZE*.22), 0)
        pygame.draw.circle(surf, BLACK, rightPupil, int(WALL_RADIUS*GHOST_SIZE*.22), 0)

class Platform(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#4876FF"), pos, *groups)

class ExitBlock(Platform):
    def __init__(self, pos, *groups):
        super().__init__(Color("#ebef00"), pos, *groups)

if __name__ == "__main__":
    main()