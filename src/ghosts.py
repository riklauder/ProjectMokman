#! /usr/bin/python

import sys, types, os, random, time, math
import mokman
from mokman import *


class BlinkyGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#ff0000"), pos, *groups)
        self.dir = 1
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 3
        self.lastDir = 4
        self.platforms = platforms
        self.speed = PAC_SPEED
        self.turning = None
        self.change_x=0
        self.change_y=0
        self.state=0

    def update(self):
        self.currDir = getDir(self)
        self.laycoods.x = getObjectCoord(self, 'x')
        self.laycoods.y = getObjectCoord(self, 'y')
        legals = getlayoutActions(self)
        randmove = random.randint(0, len(legals)-1)
        if self.stopped:
            self.dir = legals[randmove]
        if self.dir == 1:
            if self.dir in legals:
                self.vel.x = self.speed
                self.change_x += self.vel.x
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.change_x += self.vel.x
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.change_y += self.vel.y
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.change_y += self.vel.y
                self.vel.x = 0
                self.stopped = False
        #increment in x direction
        self.rect.left += int(self.vel.x)
        if self.vel.x != 0:
            self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += int(self.vel.y)
        if self.vel.y != 0:
            self.collide(0, self.vel.y, self.platforms)

    def collide(self, xvel, yvel, platforms):
        for g in platforms:
            if pg.sprite.collide_rect(self, g):
                curDir = getDir(self)
                if isinstance(g, ExitBlock):
                    pg.event.post(pg.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = g.rect.left
                    self.xvel = 0
                    if curDir == 1:
                        self.stopped = True
                elif xvel < 0:
                    if DEBUG == True:
                        print("s.lf p.rt", self.rect.left, g.rect.right)
                    self.rect.left = g.rect.right
                    self.xvel = 0
                    if curDir == 3:
                        self.stopped = True
                if yvel > 0:
                    self.rect.bottom = g.rect.top
                    self.yvel = 0
                    if curDir == 2:
                        self.stopped = True
                elif yvel < 0:
                    self.yvel = 0
                    self.rect.top = g.rect.bottom
                    if curDir == 0:
                        self.stopped = True