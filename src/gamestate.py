#State Machine for Mokmak
# A State has an operation, and can be moved
# into the next State given an Input:
from settings import *
import multiprocessing
from multiprocessing import Process, current_process
from util import nearestPoint
from util import manhattanDistance
import pacmanrules
from ghosts import GhostRules

class GameState:

    # static variable keeps track of which states have had getLegalActions called
    explored = set()

    @staticmethod
    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp

	def getLegalActions(self, agentid=0):
		if self.isWin() or self.isLose(): return []

		if agentid == 0:  # Pacman
			return getlayoutActions(self)
		else:
			return getlayoutActions(self, agentid)

	def getlayoutActions(self, *agentid):
		x = self.laycoods.x
		y = self.laycoods.y

		legals = []
		#check L
		if not isWall(x-1, y):
			legals.append(DIR_LEFT)
		#check R
		if not isWall(x+1, y):
			legals.append(DIR_RIGHT)
		#check D
		if not isWall(x, y+1):
			legals.append(DIR_DOWN)
		#check U
		if not isWall(x, y-1):
			legals.append(DIR_UP)
		return legals

	def isWall(x, y):
		if levelt[int(y)][int(x)] == '%':
			return True
		else: return False

	def getLegalPacmanActions(self):
		return self.getLegalActions(0)

	def getPacmanState(self):
		return self.data.agentStates[0].copy()

    def getPacmanPosition(self):
        return self.data.agentStates[0].getPosition()

    def getGhostStates(self):
        return self.data.agentStates[1:]

    def getGhostState(self, agentIndex):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise Exception("Invalid index passed to getGhostState")
        return self.data.agentStates[agentIndex]

    def getGhostPosition(self, agentIndex):
        if agentIndex == 0:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.data.agentStates[agentIndex].getPosition()

    def getGhostPositions(self):
        return [s.getPosition() for s in self.getGhostStates()]

    def getNumAgents(self):
        return len(self.data.agentStates)

    def getScore(self):
        return float(self.data.score)

    def getCapsules(self):
        """
        Returns a list of positions (x,y) of the remaining capsules.
        """
        return self.data.capsules

    def getNumFood(self):
        return self.data.food.count()

    def getFood(self):
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.data.food

    def getPlatforms(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

	def hasFood(self, x, y):
		return self.data.food[x][y]

	def hasWall(self, x, y):
		return self.data.layout.walls[x][y]

	def isLose(self):
		return self.data._lose

	def isWin(self):
		return self.data._win

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################

    def __init__(self, prevState = None):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None: # Initial state
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def deepCopy(self):
        state = GameState(self)
        state.data = self.data.deepCopy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.data)

    def __str__(self):

        return str(self.data)

    def initialize(self, layout, numGhostAgents=1000):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.data.initialize(layout, numGhostAgents)

class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """
    def __init__(self, timeout=30):
        self.timeout = timeout

    def newGame(self, layout, pacmanAgent, ghostAgents, display, quiet = False, catchExceptions=False):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize(layout, len(ghostAgents))
        game = Game(agents, display, self, catchExceptions=catchExceptions)
        game.state = initState
        self.initialState = initState.deepCopy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        """
        Checks to see whether it is time to end the game.
        """
        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)

    def win(self, state, game):
        if not self.quiet: print("Pacman emerges victorious! Score: %d" % state.data.score)
        game.gameOver = True

    def lose(self, state, game):
        if not self.quiet: print("Pacman died! Score: %d" % state.data.score)
        game.gameOver = True

    def getProgress(self, game):
        return float(game.state.getNumFood()) / self.initialState.getNumFood()

    def agentCrash(self, game, agentIndex):
        if agentIndex == 0:
            print("Pacman crashed")
        else:
            print("A ghost crashed")

    def getMaxTotalTime(self, agentIndex):
        return self.timeout

    def getMaxStartupTime(self, agentIndex):
        return self.timeout

    def getMoveWarningTime(self, agentIndex):
        return self.timeout

    def getMoveTimeout(self, agentIndex):
        return self.timeout

    def getMaxTimeWarnings(self, agentIndex):
        return 0


##############################################
#FRAMEWORK
##############################################

def default(str):
    return str + ' [Default: %default]'

def parseAgentArgs(str):
    if str == None: return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key,val = p, 1
        opts[key] = val
    return opts


def formatOutput(games):
    ret = ''
    ret_dict = {}
    ret_dict['scores'] = scores = [game.state.getScore() for game in games]
    ret_dict['wins'] = wins = [game.state.isWin() for game in games]
    ret_dict['win_rate'] = win_rate = wins.count(True) / float(len(wins))
    ret_dict['avg_score'] = avg_score = sum(scores) / float(len(scores))
    ret += '{} {}\n'.format('Average Score:', avg_score)
    ret += '{} {}\n'.format('Scores:       ', ', '.join([str(score) for score in scores]))
    ret += '{}{}/{} ({:.2f})\n'.format('Win Rate:      ', wins.count(True), len(wins), win_rate)
    ret += '{} {}'.format('Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins]))
    ret_dict['output_string'] = ret
    return ret_dict