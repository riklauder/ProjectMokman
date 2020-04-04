#! /usr/bin/python

import os, sys, random, settings, util, gamestate
from settings import *
#from mokman import Entity
from mokman import *
from astartwo import *


class Entity(pg.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self._layer = 1
#DIR_UP = 0  #DIR_RIGHT = 1 #DIR_DOWN = 2  #DIR_LEFT = 3 #STOPPED = 4

def scaredTimer():
    return int(GHOSTSSCARED)

#function called during loop to move ghosts to updated pos and dir
def ghostsMove(ghosts, teleports):
    for g in ghosts:
        #increment in x direction
        if g.vel.x != 0:
            g.rect.left += int(g.vel.x)
            ghostcollide(g, g.vel.x, 0, teleports)
        # increment in y direction
        if g.vel.y != 0:
            g.rect.top += int(g.vel.y)
            ghostcollide(g, 0, g.vel.y, teleports)

def chgGhostState(ghosts, state):
    for g in ghosts:
        g.ghostState = state

def sTimer(ghosts, gstime):
    gstime += 1
    if gstime >= scaredTimer():
        chgGhostState(ghosts, 0)
        return True

def respawnGhost(self, mx, my, gname):
    if gname == "Blinky":
        self.rect.left = mx
        self.rect.top = my-(27*TILE_SIZE)
    if gname == "Pinky":
        self.rect.left = mx
        self.rect.top = my-(27*TILE_SIZE)
    if gname == "Inky":
        self.rect.left = mx
        self.rect.top = my-(2*27*TILE_SIZE)
    if gname == "Clyde":
        self.rect.left = mx
        self.rect.top = my-(2*27*TILE_SIZE)
    if gname == "Slyder":
        self.rect.left = mx
        self.rect.top = my-(27*TILE_SIZE)
    if gname == "Welch":
        posint = random.randint(0,25)
        posx = 9
        if posint > 12:
            posx = 18
        self.rect.left = mx
        self.rect.top = my-(27*TILE_SIZE)


def ghostcollide(self, xvel, yvel, teleports):
    for g in self.platforms:
        if pg.sprite.collide_rect(self, g):
            curDir = self.dir
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
    teleport(self, teleports)

def getlayoutActions(self):
    x = self.laycoods.x
    y = self.laycoods.y
    gobjs = gamestate.GameState
    legals = []
    #check L
    if not gobjs.isWall(x-1, y, levelt):
        legals.append(DIR_LEFT)
    #check R
    if not gobjs.isWall(x+1, y, levelt):
        legals.append(DIR_RIGHT)
    #check D
    if not gobjs.isWall(x, y+1, levelt):
        legals.append(DIR_DOWN)
    #check U
    if not gobjs.isWall(x, y-1, levelt):
        legals.append(DIR_UP)
    
    return legals

def getMaze(level):
    mazet = [[0] * int(X_DIM+1)] * int(Y_DIM+1)
    maze = level.layoutText

    npmaze = np.array(maze)
    npmazet=np.array(mazet)
    xi=0
    for x in npmaze:
        yi=0
        for y in x:
            npmazet[xi][yi] = int(0)
            if npmaze[xi][yi] == '%':
                npmazet[xi][yi] = int(1)
            yi += 1
        xi+=1
        yi = 0

    mazet = npmazet.tolist()
    return mazet

def ghostAttack(self, mazet):
    '''
    args - mokman Player , mazet is map with walls only as 1 or 0
    Function used to make ghosts agressively pursue the Player
    Uses Astar search currently
    '''
    mokmanPos = self.laycoods

    #mazet = getMaze(level)
    #print(mazet)

    for g in self.ghosts:
        if g.behave == "chase":
            pos = g.laycoods
            if abs(mokmanPos[1] - pos[1]) < 30:
                if g.xadj != 0: #update xadj based on ghost personality
                    if (pos[0]==mokmanPos[0] or pos[1]==mokmanPos[1]):
                        break
                start = [int(pos.y), int(pos.x)]
                end = [int(mokmanPos.y), int(mokmanPos.x)]
                pcost = 1
                path = search(mazet, pcost, start, end)
                if path != None:
                    nppath = np.array(path)
                    nextpx = np.argmax(nppath, axis=0)
                    nextpy = np.argmax(nppath, axis=1)
                    nextpos = np.unravel_index(np.argmax(nppath, axis=None), nppath.shape)

                    b = np.argwhere(nppath==1)
                    if b.size != 0:
                        bpos = (b.max(), b.min())
                        pos = (pos[1], pos[0])
                        nextpd = sub(pos, bpos)
                        nextdir = getD(nextpd)
                        if nextdir != STOPPED:
                            g.dir = nextdir
        if g.behave == "sees":
            pos = g.laycoods
            seen = False
            if (abs(mokmanPos[0]-pos[0]) <= g.xadj ):
                seen = True
            if (pos[0]==mokmanPos[0] or pos[1]==mokmanPos[1]):
                seen = True
            if seen:
                continue
                start = [int(pos.y), int(pos.x)]
                end = [int(mokmanPos.y), int(mokmanPos.x)]
                pcost = 1
                path = search(mazet, pcost, start, end)
                if path != None:
                    nppath = np.array(path)
                    nextpx = np.argmax(nppath, axis=0)
                    nextpy = np.argmax(nppath, axis=1)
                    nextpos = np.unravel_index(np.argmax(nppath, axis=None), nppath.shape)

                    b = np.argwhere(nppath==1)
                    if b.size != 0:
                        bpos = (b.max(), b.min())
                        pos = (pos[1], pos[0])
                        nextpd = sub(pos, bpos)
                        nextdir = getD(nextpd)
                        if nextdir != STOPPED:
                            g.dir = nextdir



class BlinkyGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#ff0000"), pos, *groups)
        self.dir = 2
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 1
        self.lastDir = 4
        self.platforms = platforms
        self.speed = GHOST_SPEED*TURNBOOST
        self.turning = None
        self.ghostState=0
        self.gname = "Blinky"
        self.xadj=0 # ghosts personality adjust attack vector
        self.behave = "chase"

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
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.vel.x = 0
                self.stopped = False
        if self.ghostState == 3:
            self.image.fill(Color("#0000ff"))
        else: self.image.fill(Color("#ff0000")) 



class PinkyGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#FF1493"), pos, *groups)
        self.dir = 1
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 3
        self.lastDir = 4
        self.platforms = platforms
        self.speed = GHOST_SPEED*TURNBOOST
        self.turning = None
        self.ghostState=0
        self.gname = "Pinky"
        self.xadj=4 # ghosts personality adjust attack vector
        self.behave = "chase"

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
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.vel.x = 0
                self.stopped = False
        if self.ghostState == 3:
            self.image.fill(Color("#0000ff"))
        else: self.image.fill(Color("#FF1493"))       



class InkyGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#00BFFF"), pos, *groups)
        self.dir = 1
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 3
        self.lastDir = 4
        self.platforms = platforms
        self.speed = GHOST_SPEED # moves slower
        self.turning = None
        self.ghostState=0
        self.gname = "Inky"
        self.xadj = -2 # ghosts personality adjust attack vector
        self.behave = "chase"

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
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.vel.x = 0
                self.stopped = False
        if self.ghostState == 3:
            self.image.fill(Color("#0000ff"))
        else: self.image.fill(Color("#00BFFF"))      



class ClydeGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#FFA500"), pos, *groups)
        self.dir = 1
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 3
        self.lastDir = 4
        self.platforms = platforms
        self.speed = GHOST_SPEED*TURNBOOST
        self.turning = None
        self.ghostState=0
        self.xadj = 5 # Clyde only chases when he is on same level or within 5
        self.gname = "Clyde"
        self.behave = "sees"
        

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
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.vel.x = 0
                self.stopped = False
        if self.ghostState == 3:
            self.image.fill(Color("#0000ff"))
        else: self.image.fill(Color("#FFA500"))       



class SlyderGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#32CD32"), pos, *groups)
        self.dir = 1
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 1
        self.lastDir = 3
        self.nextDir = 3
        self.platforms = platforms
        self.speed = TURNBOOST
        self.turning = None
        self.ghostState=0
        self.gname = "Slyder"
        self.behave = "static"
        self.xadj=0 # ghosts personality adjust attack vector

    def update(self):
        self.currDir = getDir(self)
        self.laycoods.x = getObjectCoord(self, 'x')
        self.laycoods.y = getObjectCoord(self, 'y')
        legals = getlayoutActions(self)
        randmove = random.randint(0, len(legals)-1)
        if self.stopped:
            self.dir = self.nextDir
            if self.nextDir == 3:
                self.nextDir = 1
            else:
                self.nextDir = 3
        if self.dir == 1:
            if self.dir in legals:
                self.vel.x = self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.vel.x = 0
                self.stopped = False
        if self.ghostState == 3:
            self.image.fill(Color("#0000ff"))
        else: self.image.fill(Color("#32CD32"))       



class WelchGhosts(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#800080"), pos, *groups)
        self.dir = 0
        self.laycoods = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.stopped = False
        self.currDir = 0
        self.lastDir = 2
        self.nextDir = 2
        self.platforms = platforms
        self.speed = TURNBOOST
        self.turning = None
        self.ghostState=0
        self.gname = "Welch"
        self.behave = "static"
        self.xadj=0 # ghosts personality adjust attack vector

    def update(self):
        self.currDir = getDir(self)
        self.laycoods.x = getObjectCoord(self, 'x')
        self.laycoods.y = getObjectCoord(self, 'y')
        legals = getlayoutActions(self)
        randmove = random.randint(0, len(legals)-1)
        if self.stopped:
            self.dir = self.nextDir
            if self.nextDir == 2:
                self.nextDir = 0
            else:
                self.nextDir = 2
        if self.dir == 1:
            if self.dir in legals:
                self.vel.x = self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 3:
            if self.dir in legals:
                self.vel.x = -self.speed
                self.vel.y = 0
                self.stopped = False
        if self.dir == 0:
            if self.dir in legals:
                self.vel.y = -self.speed
                self.vel.x = 0  
                self.stopped = False
        if self.dir == 2:
            if self.dir in legals:
                self.vel.y = self.speed
                self.vel.x = 0
                self.stopped = False
        if self.ghostState == 3:
            self.image.fill(Color("#0000ff"))
        else: self.image.fill(Color("#800080"))      


from game import Actions, Directions

class GhostRules:
    """
    These functions dictate how ghosts interact with their environment.
    """
    #GHOST_SPEED = PAC_SPEED

    @staticmethod
    def getLegalActions(state, ghostIndex):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        conf = state.getGhostState(ghostIndex).configuration
        possibleActions = Actions.getPossibleActions(conf, state.data.layout.walls)
        reverse = Actions.reverseDirection(conf.direction)
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)
        if reverse in possibleActions and len(possibleActions) > 1:
            possibleActions.remove(reverse)
        return possibleActions

    @staticmethod
    def applyAction(state, action, ghostIndex):
        legal = GhostRules.getLegalActions(state, ghostIndex)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0: speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        ghostState.configuration = ghostState.configuration.generateSuccessor(vector)

    @staticmethod
    def decrementTimer(ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint(ghostState.configuration.pos)
        ghostState.scaredTimer = max(0, timer - 1)

    @staticmethod
    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0: # Pacman just moved; Anyone can kill him
            for index in range(1, len(state.data.agentStates)):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                if GhostRules.canKill(pacmanPosition, ghostPosition):
                    GhostRules.collide(state, ghostState, index)
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, agentIndex)

    @staticmethod
    def collide(state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            state.data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win:
                state.data.scoreChange -= 500
                state.data._lose = True

    @staticmethod
    def canKill(pacmanPosition, ghostPosition):
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

    @staticmethod
    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start




