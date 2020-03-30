#! /usr/bin/python

import mokman
from settings import *
from mokman import *
from mokman import Entity
from roundrects import aa_round_rect


def scaredTimer():
    return int(140)

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
        self.speed = PAC_SPEED*TURNBOOST
        self.turning = None
        self.ghostState=0

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
        self.speed = PAC_SPEED*TURNBOOST
        self.turning = None
        self.ghostState=0

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
        self.speed = TURNBOOST
        self.turning = None
        self.ghostState=0

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
        self.speed = PAC_SPEED*TURNBOOST
        self.turning = None
        self.ghostState=0

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




