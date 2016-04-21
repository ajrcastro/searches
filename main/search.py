# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    "*** YOUR CODE HERE ***"           
    closedSet = set()
    actions = []
    dfsStack = util.Stack()
    
    currState = problem.getStartState() 
    closedSet.add(currState)
    
    for successor in problem.getSuccessors(currState):
        actions = [successor[1]]
        if successor[0] not in closedSet:
            dfsStack.push((successor, actions))
    currState = dfsStack.pop()
    closedSet.add(currState[0][0])

    ignoreFirst = 0
    
    while not (problem.isGoalState(currState[0][0])):
        if dfsStack.isEmpty() and ignoreFirst > 1:
            return []
        else:
            currSuccessors = problem.getSuccessors(currState[0][0])
            for successor in currSuccessors:
                if successor[0] not in closedSet:
                    dfsStack.push((successor, currState[1]+[successor[1]]))
                    ignoreFirst += 1            
            currState = dfsStack.pop()
            closedSet.add(currState[0][0])
    return currState[1]  
    
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    closedSet = set()
    actions = []
    bfsQueue= util.Queue()
    
    currState = problem.getStartState() 
    closedSet.add(currState)
    
    for successor in problem.getSuccessors(currState):
        actions = [successor[1]]
        if successor[0] not in closedSet:
            bfsQueue.push((successor, actions))
            closedSet.add(successor[0])
    currState = bfsQueue.pop()
   
    ignoreFirst = 0
    
    while not (problem.isGoalState(currState[0][0])):
        if bfsQueue.isEmpty() and ignoreFirst > 1:
            return []
        else:
            currSuccessors = problem.getSuccessors(currState[0][0])
            for successor in currSuccessors:
                if successor[0] not in closedSet:
                    bfsQueue.push((successor, currState[1]+[successor[1]]))
                    closedSet.add(successor[0])
                    ignoreFirst += 1            
            currState = bfsQueue.pop()
    return currState[1]

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    closedSet = {}
    ucsPQ = util.PriorityQueue()
    
    currState = problem.getStartState() 
    closedSet[currState] = 0
    
    for successor in problem.getSuccessors(currState):
        if successor[0] not in closedSet:
            ucsPQ.push((successor, [successor[1]]), successor[2])
            closedSet[successor[0]] = successor[2]
    currState = ucsPQ.pop()
   
    ignoreFirst = 0
    
    while not (problem.isGoalState(currState[0][0])):
        if ucsPQ.isEmpty() and ignoreFirst > 1:
            return []
        else:
            currSuccessors = problem.getSuccessors(currState[0][0])
            for successor in currSuccessors:
                sucDistance = successor[2] + closedSet[currState[0][0]]
                if successor[0] not in closedSet:
                    distToStore = successor[2] + closedSet[currState[0][0]]
                    ucsPQ.push((successor, currState[1]+[successor[1]]), distToStore)
                    closedSet[successor[0]] = distToStore
                    
                    ignoreFirst += 1     
                else:
                    if closedSet[successor[0]] > sucDistance:
                        ucsPQ.push((successor, currState[1]+[successor[1]]), sucDistance)
                        closedSet[successor[0]] = sucDistance
                        ignoreFirst += 1   
            currState = ucsPQ.pop()
    return currState[1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    closedSet = {}
    ucsPQ = util.PriorityQueue()
    
    currState = problem.getStartState() 
    closedSet[currState] = 0
    
    for successor in problem.getSuccessors(currState):
        if successor[0] not in closedSet:
            priority = heuristic(successor[0], problem) + successor[2]
            ucsPQ.push((successor, [successor[1]]), priority)
            closedSet[successor[0]] = priority
    currState = ucsPQ.pop()
   
    ignoreFirst = 0
    
    while not (problem.isGoalState(currState[0][0])):
        if ucsPQ.isEmpty() and ignoreFirst > 1:
            return []
        else:
            currSuccessors = problem.getSuccessors(currState[0][0])
            for successor in currSuccessors:
                sucDistance = successor[2] + problem.getCostOfActions(currState[1])
                priority = sucDistance + heuristic(successor[0], problem)
                if successor[0] not in closedSet:
                    ucsPQ.push((successor, currState[1]+[successor[1]]), priority)
                    closedSet[successor[0]] = priority
                    ignoreFirst += 1     
                else:
                    if closedSet[successor[0]] > priority:
                        ucsPQ.push((successor, currState[1]+[successor[1]]), priority)
                        closedSet[successor[0]] = priority
                        ignoreFirst += 1   
            currState = ucsPQ.pop()
    return currState[1]



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
