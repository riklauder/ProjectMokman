#! /usr/bin/python

import sys, types, os, random, time, math, heapq, itertools, util
import pygame as pg
from pygame import *
from mokman import Entity, getLegalActions, legalColl
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

    '''
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#ebef00"), pos)
        self.dir = 4
        self.vel = pg.Vector2(0, 0)
        self.dest = pg.Vector2(0,0)
        self.cdir = pg.Vector2(0,0)
        self.vdir = pg.Vector2(0,0)
        self.nextDir = pg.Vector2(0,0)
        self.stopped = True
        self.lastDir = 4
        self.platforms = platforms
        self.speed = PAC_SPEED
        self.turning = None
        self.streak = 0

    def getDir(self):
        if (self.vel.x>=1): return DIR_RIGHT
        if (self.vel.x<=-1): return DIR_LEFT
        if (self.vel.y<=-1): return DIR_UP
        if (self.vel.y>=1): return DIR_DOWN
        if (self.vel.y == 0 and self.vel.x == 0): return STOPPED

    def fixedUpdate(self):
        setcDir(self)
        self.readInputAndMove()
        self.animate()

    def animate(self):
        setcDir(self)
        self.cdir = self.dest - self.pdir
        left = self.speed
        top = self.speed

    def isvalid(self, vec2Dir):
        pos = pg.Vector2(self.cdir.x,self.cdir.y)
        vec2Dir += pg.Vector2(vec2Dir.x, vec2Dir.y)
        hit = None
        if self.vel.x != 0:
            hit = self.collide(self.vel.x, 0, self.platforms)
        if self.vel.y != 0:
            hit = self.collide(0, self.vel.y, self.platforms)
        return hit

    def resetDestination(self):
        dest = (self.getDir(), self.getDir)

    def readInputAndMove(self):
        setcDir(self)
        p = pg.Vector2(self.cdir.x,self.cdir.y)
        pressed = pg.key.get_pressed()
        up = pressed[K_UP]
        down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        currDir = self.getDir()
        illegalMoves = getLegalActions(self)
        if self.lastDir != STOPPED and DEBUG == True:
            print("currVselfVLastDir:", currDir, self.dir, self.lastDir)
            print("illegalMoves", illegalMoves)
        self.lastDir = currDir        
        if self.stopped:
            self.dir = 4
            self.vel.x = 0
            self.vel.y = 0
        if right or self.dir == 1:
            self.dir = 1
            if self.dir not in illegalMoves:
                self.vel.y = 0
                self.vel.x = self.speed
                self.change_x += self.vel.x
                self.stopped = False
        if left or self.dir == 3:
            self.dir = 3
            if self.dir not in illegalMoves:
                self.vel.y = 0
                self.vel.x = -self.speed
                self.change_x += self.vel.x
                self.stopped = False
        if up or self.dir == 0:
            self.dir = 0
            if self.dir not in illegalMoves:
                self.vel.x = 0
                self.vel.y = -self.speed
                self.change_y += self.vel.y
                self.stopped = False
        if down or self.dir == 2:
            self.dir = 2
            if self.dir not in illegalMoves:
                self.vel.x = 0
                self.vel.y = self.speed
                self.change_y += self.vel.y
                self.stopped = False
            if manhattanDistance(self.dest, self.cdir) < 1:
                if self.isvalid(self.nextDir):
                    self.dest = self.cdir + self.nextDir
                    self.vdir = self.nextDir
                elif self.isvalid(self.vdir):
                    self.dest = self.cdir + self.vdir

    def setcDir(self):
        self.cdir = self.vel
        return self.cdir

    def getvDir(self):
        return self.vdir

    def collide(self, xvel, yvel, platforms):
        hitc = False
        setcDir(self)
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                hitc = True
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
        return hitc
        #DIR_UP = 0   #DIR_RIGHT = 1
        #DIR_DOWN = 2 #DIR_LEFT = 3 #STOPPED=4