# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #list to hold closed nodes
    closedset = {}
    #create stack for nodes to be searched
    openset = util.Stack()
    #initiate the stack with the starting state
    openset.push((problem.getStartState(), 'start'))
    #list to hold the state with its parent node
    parent = {}
    #while we have nodes on the stack
    while not openset.isEmpty():
        state = openset.pop()
        #check if the node has not been visited
        if closedset.has_key(state[0]):
            continue
        #add the state to the list for visited nodes
        closedset[state[0]] = True
        #if we found the goalstate, reconstruct the path
        if problem.isGoalState(state[0]):
            path = createPath(state, parent)
            return path
        else:
            #get the successor of the current state and if it is not visited yet,
            #add it to the stack and set its parent
            for successor in problem.getSuccessors(state[0]):
                if not closedset.has_key(successor[0]):
                    openset.push(successor)
                    parent[successor] = state

def createPath(state, parent):
    path = []
    #when the state is not the starting state, add the action to get there to the path
    #and continue to construct the backwards path from the parent
    while state[1] != 'start':
        path.append(state[1])
        state = parent[state]
    #return the path (in reversed order since we reconstructed it backwards)
    return path[::-1]

def breadthFirstSearch(problem):
    #list to hold closed nodes
    closedset = {}
    #create stack for nodes to be searched
    openset = util.Queue()
    #initiate the queue with the starting state
    openset.push((problem.getStartState(), 'start'))
    #list to hold the state with its parent node
    parent = {}
    #while we have nodes on the Queue
    while not openset.isEmpty():
        state = openset.pop()
        #check if the node has not been visited
        if closedset.has_key(state[0]):
            continue
        #add the state to the list for visited nodes
        closedset[state[0]] = True
        #if we found the goalstate, reconstruct the path
        if problem.isGoalState(state[0]):
            path = createPath(state, parent)
            return path
        else: #get the successor of the current state and if it is not visited yet add it to the queue and set its parent
            for successor in problem.getSuccessors(state[0]):
                if not closedset.has_key(successor[0]):
                    openset.push(successor)
                    parent[successor] = state

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #list to hold closed nodes
    closedset = {}
    #create PriorityQueue for nodes to be searched, with the lambda function to take the cost as priority
    openset = util.PriorityQueueWithFunction(lambda x: x[2])
    #initiate the stack with the starting state
    openset.push((problem.getStartState(), 'start', 0))
    #list to hold the state with its parent node
    parent = {}
    #list to keep track of costs to all nodes,
    costs = {}
    #initiate cost for starting state
    costs[problem.getStartState()]= 0
    #while we have nodes on the Queue
    while not openset.isEmpty():
        state = openset.pop()
        #check if the node has not been visited
        if closedset.has_key(state[0]):
            continue
        #add the state to the list for visited nodes
        closedset[state[0]] = True
        #if we found the goalstate, reconstruct the path
        if problem.isGoalState(state[0]):
            #variation on create path for this search method
            path = []
            while state[1] != 'start':
                path.append(state[1])
                state = parent[state[0]]
            #return the path (in reversed order since we reconstructed it backwards)
            return path[::-1]

        else: #get the successor of the current state
            for successor in problem.getSuccessors(state[0]):
                #calculate its cost by taking the current cost + the cost to the successor
                cost = successor[2] + state[2]
                #if this node has already been found, but the cost is lower than the known cost, update it
                if costs.has_key(successor[0]) and costs[successor[0]] > cost:
                    openset.push((successor[0],successor[1], cost))
                    costs[successor[0]]= cost
                    parent[successor[0]] = state

                #if this node hasnt been found yet and hasnt been closed, add it to the queue and set the cost and parent
                if not costs.has_key(successor[0]):
                    if not closedset.has_key(successor[0]):
                        openset.push((successor[0],successor[1], cost))
                        costs[successor[0]]= cost
                        parent[successor[0]] = state

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Since A* can update node costs, we use a set to keep track of costs
    costs = {}
    costs[problem.getStartState()] = 0

    # These are the sets we use to keep track of open, closed and parent nodes
    closedset = {}
    # The lambda automatically calculates the heuristic plus the cost when adding to the queue
    openset = util.PriorityQueueWithFunction(lambda x: heuristic(x[0], problem) + costs[x[0]])
    openset.push((problem.getStartState(),'start',0)) # We identify the start state by giving it the action '', the node cost = 0
    parents = {}

    # While we have nodes to expand
    while not openset.isEmpty():
        # Take from the queue
        state = openset.pop()

        # Mark the node as visited
        closedset[state[0]] = True

        # If we have found the goal
        if problem.isGoalState(state[0]):
            actions = []

            # While we have not found the start state
            while state[1] != 'start':
                #Append the action to the list
                actions.append(state[1])
                # Get the parent state
                state = parents[state]

            # Since the list was constructed in reverse order
            # Reverse the list and return
            return actions[::-1]

        # For all successors
        for succ in problem.getSuccessors(state[0]):
            # Calculate the cost of getting there
            cost = costs[state[0]] + succ[2]
            # If we need to update the cost
            if costs.has_key(succ[0]) and costs[succ[0]] > cost:
                # Update the parent
                parents[succ] = state
                # Update the cost
                costs[succ[0]] = cost
                # Push the new state to the queue (after adding it to the costset)
                openset.push(succ)
            if not closedset.has_key(succ[0]):
                # Mark the successor as found
                closedset[succ[0]] = True
                # Set the parent
                parents[succ] = state
                # Set the cost
                costs[succ[0]] = cost
                # Push the new state to the queue (after adding it to the costset)
                openset.push(succ)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
