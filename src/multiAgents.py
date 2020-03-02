# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from __future__ import print_function
from game import Agent, Directions
import random, util, logging, math, heapq
import threading, multiprocessing, time

logging.basicConfig(format='%(levelname)s:%(message)s', filename="plog/pacman.log", filemode='w', level=logging.DEBUG)
   

##########################################################################
# Evaluation Helper Functions
##########################################################################
def betterEvaluationFunction(currGameState):
    """
    extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function

    DESCRIPTON: various gamestate variables and constraints used to substitute 
    heuriistitc in evalFn
    
    ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
    """
    
    legalMoves = currGameState.getLegalActions()
    logging.debug("legalMoves:%s", legalMoves)
    logging.debug("food:\n%s", currGameState.getFood())
    
  
    position = currGameState.getPacmanPosition()
    ghostStates = currGameState.getGhostStates()
    foodStates = currGameState.getFood()
    successrP = currGameState.generatePacmanSuccessor(position)
    capsuleStates = currGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    distanceToFood = map(lambda x: 1.0 / util.manhattanDistance(x, position), foodStates.asList())
    ghostScoreu = ghostScore(ghostStates, position)

       
    def _betterScore(successrP):
        newPos = successrP.getPacmanPosition()
        foodScores = foodScore(foodStates, newPos)
        nextScore = successrP.getScore()
        try:
            logging.debug("RefreshEvalOpts Successor:\n%s newPos:%s ::%s\n NextScore:%s foodScore:%s",
                successrP, newPos, ghostStates[0], nextScore, foodScores)
        except:
            pass
        bestScore = foodScores + ghostScore(ghostStates, newPos) + nextScore
        logging.debug("betterScore:%s:%s", position, bestScore)
        
        return bestScore

    singlescore = _betterScore(successrP)
    scores = [_betterScore( action) for action in legalMoves]

    
    return singlescore


##########################################################################
# Prolog Evaluation Helper Function
##########################################################################
def prologEvaluationFunction(currGameState):
    """
    extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function

    DESCRIPTON: various gamestate variables and constraints used to substitute 
    heuriistitc in evalFn
    
    ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
    """
    
    prolog.consult("eval.pl")
    legalMoves = currGameState.getLegalActions()
    logging.debug("legalMoves:%s", legalMoves)
    logging.debug("food:\n%s", currGameState.getFood())
    
    position = currGameState.getPacmanPosition()
    ghostStates = currGameState.getGhostStates()
    foodStates = currGameState.getFood()
    successrP = currGameState.generatePacmanSuccessor(position)
    capsuleStates = currGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    distanceToFood = map(lambda x: 1.0 / util.manhattanDistance(x, position), foodStates.asList())
    ghostScoreu = ghostScore(ghostStates, position)

    problem = successrP
       
    p = str(problem)
    logging.debug("p:%s", p)
    logging.debug("prolog:\nL=%s,eval(L)", p)
    logging.debug(prolog.query("L=%s,eval(L)" % p, maxresult=1))
    result = list(prolog.query("L=%s,eval(L)" % p, maxresult=1))
    logging.debug("result:\n%s\nresult0:\n%s", result, result[0])
    if result:
        result = result[0]
        logging.debug("result[L]\n%s", result["L"])
        return result["L"]
    else:
        return False



def foodScore(foodPositions, pacmanPosition):
    """
    Calculate Food score using hyperbolic metric.
    Higher numbers are better.

    ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
    """
    # Prevent zero division, but keep reward strong.
    distanceToFood = [1.0 / max(util.manhattanDistance(x, pacmanPosition), 1) for x in foodPositions.asList()]
    # Take the best of all distanceToFood. 
    return foodPositions.count(0) + (foodPositions.count(0) * (max(distanceToFood + [0])))

def ghostScore(ghostPositions, pacmanPosition):
    """
    Calculate Manhattan Distance based on ghost positions and their scared timers.
    Higher numbers are better.

    ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
    """
    score = 0
    for ghost in ghostPositions:
        score += util.manhattanDistance(pacmanPosition, ghost.getPosition()) 
    logging.debug("ghostScore:%s", score)
    return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.

    Depth is a command line argument, like from:
    python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


##########################################################################
# ReflexAgent is our default, simple agent.
##########################################################################
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    A capable reflex agent will have to consider both food locations and ghost 
    locations to perform well. Your agent should easily and reliably clear the 
    testClassic layout.

    The code below can be changed, so long as you don't touch the method
    headers.
    """

    def getAction(self, gameState):
        """
        Return the best move based on the evaluation function.

        ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        logging.debug("legalMoves:%s", legalMoves)
        logging.debug("food:\n%s", gameState.getFood())

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        logging.debug("***ChosenIndex:%s=%s***\n", chosenIndex, legalMoves[chosenIndex])

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currGameState, pacManAction):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where HIGHER NUMBERS ARE BETTER.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
        """
        nextGameState = currGameState.generatePacmanSuccessor(pacManAction)
        newPos = nextGameState.getPacmanPosition()
        foodPositions = currGameState.getFood()
        foodScores = foodScore(foodPositions, newPos)
        ghostStates = nextGameState.getGhostStates()
        nextScore = nextGameState.getScore()
        newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
        try:
            logging.debug("RefreshEvalOpts Successor:\n%s newPos:%s ::%s\n NextScore:%s foodScore:%s",
                nextGameState, newPos, ghostStates[0], nextScore, foodScores)
        except:
            pass
        # Use food, ghosts and successor state to evaluate overall score
        overallSocre = foodScores + ghostScore(ghostStates, newPos) + nextScore
        logging.debug("OverallScore:%s:%s", pacManAction, overallSocre)
        return overallSocre


##########################################################################
# Minimax
##########################################################################
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
 
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        
        vector = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = minimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            
            if temp > vector:
              vector = temp
              bestAction = successor[0]
        return bestAction
        
def minimax(agent, agentList, state, depth, evalFunc):
  
  if depth <= 0 or state.isWin() == True or state.isLose() == True:
    return evalFunc(state)
    
  if agent == 0:
    vector = float("-inf")
  else:
    vector = float("inf")
          
  actions = state.getLegalActions(agent)
  successors = [state.generateSuccessor(agent, action) for action in actions]
  for j in range(len(successors)):
    successor = successors[j]
    
    if agent == 0:
      
      vector = max(vector,minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
    elif agent == agentList[-1]:
      
      vector = min(vector,minimax(agentList[0], agentList, successor, depth - 1, evalFunc))
    else:
     
      vector = min(vector,minimax(agentList[agent+1], agentList, successor, depth, evalFunc))
  
  return vector


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    minimax agent with alpha-beta pruning 
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgent = gameState.getNumAgents()
        ActionScore = []

        def _rmStop(List):
          return [x for x in List if x != 'Stop']

        def _alphaBeta(s, iterCount, alpha, beta):
          if iterCount >= self.depth*numAgent or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
          if iterCount%numAgent != 0: #Ghost min
            result = 1e10
            for a in _rmStop(s.getLegalActions(iterCount%numAgent)):
              sdot = s.generateSuccessor(iterCount%numAgent,a)
              result = min(result, _alphaBeta(sdot, iterCount+1, alpha, beta))
              beta = min(beta, result)
              if beta < alpha:
                break
            return result
          else: # Pacman Max
            result = -1e10
            for a in _rmStop(s.getLegalActions(iterCount%numAgent)):
              sdot = s.generateSuccessor(iterCount%numAgent,a)
              result = max(result, _alphaBeta(sdot, iterCount+1, alpha, beta))
              alpha = max(alpha, result)
              if iterCount == 0:
                ActionScore.append(result)
              if beta < alpha:
                break
            return result

        result = _alphaBeta(gameState, 0, -1e20, 1e20)
        return _rmStop(gameState.getLegalActions(0))[ActionScore.index(max(ActionScore))]

        util.raiseNotDefined()



##########################################################################
# A* Prolog Search
##########################################################################
def aStarHeuristic(gameState):
    """
    Generic heuristic function for A* search.

    ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
    """
    asfood = foodScore(gameState.getFood(), gameState.getPacmanPosition())
    asfood = math.log(asfood)
    logging.debug("astarFood %s - pmanPos-%s", asfood, gameState.getPacmanPosition())
    return asfood

class AStarAgent(MultiAgentSearchAgent):
    """
    Agent that performs A* Search to find the best action.
    """

    def getAction(self, currGameState, heuristic=aStarHeuristic):
        """
        Return the A* action.

        frontier contains triples of form ('GameState', ' Sequence of actions',
        'Total Cost', 'Depth').

        ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
        """
        explored = set()
        frontier = util.PriorityQueue()
        frontier.push((currGameState, list(), 0, 0), 0)
        bestActions, lowestCost = list(), 999999
        flag = False

        while not frontier.isEmpty():
            flag = True
            nextState, nextActions, cost, level = frontier.pop()
            if nextState.isWin() or level >= self.depth:
                if cost < lowestCost:
                    lowestCost = cost
                    bestActions = nextActions
                if level >= self.depth:
                    continue
            actions = nextState.getLegalActions(0)
            for action in actions:
                successor = nextState.generateSuccessor(0, action)
                if successor not in explored and action != Directions.STOP:
                    frontier.push(
                        (successor, nextActions + [action], cost + 1, level + 1),
                        cost + heuristic(successor)
                        )
        if len(bestActions) == 0:
            return Directions.STOP
        return bestActions[0]


##########################################################################
# A* Prolog Search
##########################################################################
class APStarAgent(MultiAgentSearchAgent):
    """
    SWI Prolog Agent that performs A* Search to find the best action.
    Borrowed Open Source idastar from UofT 
    """

    def getAction(self, currGameState, heuristic=aStarHeuristic):
        """
        Return the A* action by calling prolog

        triples of form ('GameState', ' Sequence of actions',
        'Total Cost', 'Depth').

        ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
        """
        explored = set()
        frontier = util.PriorityQueue()
        frontier.push((currGameState, list(), 0, 0), 0)
        bestActions, lowestCost = list(), 999999
        flag = False
        prolog.consult("idastar.pl")

        while not frontier.isEmpty():
            flag = True
            nextState, nextActions, cost, level = frontier.pop()
            if nextState.isWin() or level >= self.depth:
                if cost < lowestCost:
                    lowestCost = cost
                    bestActions = nextActions
                if level >= self.depth:
                    continue
            actions = nextState.getLegalActions(0)
            for action in actions:
                successor = nextState.generateSuccessor(0, action)
                p = str(actions)
                heur = cost + heuristic(successor)
                logging.debug("heur then heur[0]: %s", heur)
                if successor not in explored and action != Directions.STOP:
                    result = list(prolog.query("idastar(1, %s, %s, %s, %s, 1)" % p, 
                      bestActions, heur, (cost+1)))
                    logging.debug("result:\n%s\nresult0:\n%s", result, result[0])
                    if result:
                        result = result[0]
                        logging.debug("result:\n%s", result)
                        return result[1]
                    else:
                        return False


##########################################################################
# D* Lite
##########################################################################
def dStarHeuristic(gameState):
    """
    Calculate heuristic value for DStarLiteAgent.
    """
    pacmanPosition = gameState.getPacmanPosition()

    # Ghost information
    ghostStates = gameState.getGhostStates()
    ghostValue = max([1.0 / max(util.manhattanDistance(pacmanPosition, ghost.getPosition()), 1.0) for ghost in ghostStates])
    
    # Food information
    foodPositions = gameState.getFood()
    foodValue = max([1.0 / max(util.manhattanDistance(pacmanPosition, x), 1.0) for x in foodPositions.asList()] + [0])
    retval = max(ghostValue + (1 - foodValue) + foodPositions.count(1) - 2, 0)
    logging.debug("dStarHeur: %s", retval)

    return retval

class DStarLiteAgent(MultiAgentSearchAgent):
    """
    Agent that performs D* Lite search

    Reference to paper:
    http://www.aaai.org/Papers/AAAI/2002/AAAI02-072.pdf
    """

    def getAction(self, currGameState, heuristic=dStarHeuristic):
        """
        Return the optimal action by the D* Lite algorithm.

        maze of current game state aka frontier contains triples of 
        form ('GameState', ' Sequence of actions','Total Cost', 'Depth').

        ⭐⭐⭐️ Free to Adjust ⭐⭐⭐️
        """
        explored = set()
        frontier = util.PriorityQueue()
        frontier.push((currGameState, list(), 0, 0), 0)
        bestActions, lowestCost = list(), 999999
        logging.debug("lowestCost: %s", lowestCost)
        logging.debug("bestActions: %s", bestActions)

        while not frontier.isEmpty():
            logging.debug("bestActions!Empty: %s", bestActions)
            nextState, nextActions, cost, level = frontier.pop()
            if nextState.isWin() or level >= self.depth:
                if cost < lowestCost:
                    lowestCost = cost
                    bestActions = nextActions
                    if len(bestActions) == 0:
                        bestActions.append(None)
                if level >= self.depth:
                    continue
            actions = nextState.getLegalActions(0)
            for action in actions:
                successor = nextState.generateSuccessor(0, action)
                direction = successor.getPacmanState()
                logging.debug("direction: %s", direction)
                logging.debug("nextAction: %s", nextActions + [action])
                if successor not in explored and action != Directions.STOP:
                    frontier.push(
                        (successor, nextActions + [action], cost + 1, level + 1),
                        cost + heuristic(successor))
        if len(bestActions) == 0:
            return Directions.STOP
        logging.debug("bestActions: \n%s", bestActions)
        logging.debug("frontier.pop: \n%s", nextState)
        logging.debug("bestActionsRet: \n%s", bestActions[0])
        return bestActions[0]


##########################################################################
# Expectimax 
##########################################################################
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      expectimax agent - minimax that takes max - does not expect smart opponent
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        vector = float("-inf")
        bestAction = []
        agent = 0
        actions = gameState.getLegalActions(agent)
        successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
        for successor in successors:
            temp = expectimax(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction)
            
            if temp > vector:
              vector = temp
              bestAction = successor[0]
        return bestAction
        

def expectimax(agent, agentList, state, depth, evalFunc):
  
  if depth <= 0 or state.isWin() == True or state.isLose() == True:
    return evalFunc(state)
    
  if agent == 0:
    vector = float("-inf")
  else:
    vector = 0
          
  actions = state.getLegalActions(agent)
  successors = [state.generateSuccessor(agent, action) for action in actions]
  p = 1.0/len(successors)
  for j in range(len(successors)):
    successor = successors[j]
    
    if agent == 0:
      
      vector = max(vector, expectimax(agentList[agent+1], agentList, successor, depth, evalFunc))
    elif agent == agentList[-1]:
      
      vector += p * expectimax(agentList[0], agentList, successor, depth - 1, evalFunc)
    else:
     
      vector += p * expectimax(agentList[agent+1], agentList, successor, depth, evalFunc)
  
  return vector

# Abbreviation
better = betterEvaluationFunction
