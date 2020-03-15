#! /usr/bin/python

import sys, types, os, random, time, math, heapq, itertools, util, mokman
import pygame as pg
from pygame import *
from mokman import Entity, getlayoutActions, getObjectCoord, getObjectPos, getDir
from util import manhattanDistance

PAC_SPEED = 2
TURNBOOST = 2
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3
STOPPED = 4

class PlayerController(Entity):
    '''
    Player class - initialize with = Player(mapsprite,*(startX, startY))

    *mapsprite - master sprite object representing game world

    *startX - x coordinate for staring position

    *startY - y coordinate for staring position
    '''
    def __init__(self, platforms, pos, foods, teleports, powerups, *groups):
        super().__init__(Color("#ebef00"), pos)
        self.dir = 4
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = True
        self.currDir = 3
        self.lastDir = 4
        self.platforms = platforms
        self.foods = foods
        self.speed = PAC_SPEED
        self.turning = None
        self.change_x=0
        self.change_y=0
        self.score=1


    def update(self):
        pressed = pg.key.get_pressed()
        up = pressed[K_UP]
        down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        
        self.currDir = getDir(self)
        self.isTurning()
        self.laycoods.x = getObjectCoord(self, 'x')
        self.laycoods.y = getObjectCoord(self, 'y')
        legals = getlayoutActions(self)
        if self.stopped == True:
            legals.append(STOPPED)
        if self.lastDir != STOPPED and DEBUG == True:
            print("currVselfVLastDir:", self.currDir, self.dir, self.lastDir)
            print("legals, l.x l.y", legals, self.laycoods.x, self.laycoods.y)
        self.lastDir = self.currDir
        if self.stopped:
            self.dir = 4
            if self.dir in legals:
                self.vel.x = 0
                self.vel.y = 0
        if right or self.dir == 1:
            self.dir = 1
            if self.dir in legals:
                self.vel.x = self.speed
                self.change_x += self.vel.x
                self.vel.y = 0
                self.stopped = False
        if left or self.dir == 3:
            self.dir = 3
            if self.dir in legals:
                self.vel.x = -self.speed
                self.change_x += self.vel.x
                self.vel.y = 0
                self.stopped = False
        if up or self.dir == 0:
            self.dir = 0
            if self.dir in legals:
                self.vel.y = -self.speed
                self.change_y += self.vel.y
                self.vel.x = 0  
                self.stopped = False
        if down or self.dir == 2:
            self.dir = 2
            if self.dir in legals:
                self.vel.y = self.speed
                self.change_y += self.vel.y
                self.vel.x = 0
                self.stopped = False
        # increment in x direction
        self.rect.left += int(self.vel.x)
        if self.vel.x != 0:
            if self.turning and abs(self.vel.x) < PAC_SPEED+TURNBOOST:
                self.vel.x = PAC_SPEED+TURNBOOST
            self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += int(self.vel.y)
        if self.vel.y != 0:
            if self.turning and abs(self.vel.y) < PAC_SPEED+TURNBOOST:
                self.vel.y = PAC_SPEED+TURNBOOST
            self.collide(0, self.vel.y, self.platforms)
        self.foodCollide(self.foods)
        score = self.score
        if DEBUG == True:
            print("v.x new.x v.y", self.vel.x, self.rect.left, self.vel.y)        
        #DIR_UP = 0  #DIR_RIGHT = 1 #DIR_DOWN = 2  #DIR_LEFT = 3
        #STOPPED = 4


    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                curDir = getDir(self)
                if isinstance(p, ExitBlock):
                    pg.event.post(pg.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    if curDir == 1:
                        self.stopped = True
                elif xvel < 0:
                    if DEBUG == True:
                        print("s.lf p.rt", self.rect.left, p.rect.right)
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    if curDir == 3:
                        self.stopped = True
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                    if curDir == 2:
                        self.stopped = True
                elif yvel < 0:
                    self.yvel = 0
                    self.rect.top = p.rect.bottom
                    if curDir == 0:
                        self.stopped = True
        #DIR_UP = 0  #DIR_RIGHT = 1  #DIR_DOWN = 2  #DIR_LEFT = 3
        #STOPPED = 4

    def isTurning(self):
        if getDir(self) != self.dir:
            self.turning = True
            self.speed = PAC_SPEED+TURNBOOST
        else: 
            self.speed = PAC_SPEED+TURNBOOST
            self.turning = False

    def foodCollide(self, foods):
        for f in foods:
            if pg.sprite.collide_rect(self, f):
                f.kill()
                self.score += 1

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