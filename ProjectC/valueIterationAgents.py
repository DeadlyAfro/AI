# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        # Create iterator
        i = 0
        while i < iterations:
            #initialize a list to hold values
            values = {}
            # Loop through all states if it is a terminal state, set its value to 0
            for state in mdp.getStates():
                if mdp.isTerminal(state):
                    values[state] = 0
                else:
                #Create a list to hold the temporaray QValues
                    tempList = []
                    #Loop through all possible actions
                    for action in mdp.getPossibleActions(state):
                        tempList.append(self.getQValue(state, action))
                    # Get the max from the list and store locally
                    values[state] = max(tempList)
            #update the values
            for state in values:
                self.values[state] = values[state]

            i += 1  # Update iterator


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        #Get all the states and their probabilities
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        #Initialize the Q score
        Qvalue = 0.0
        #for all successor states, calculate the (discounted score of the state + the reward of the action) * the probability
        for (successor, prob) in statesAndProbs:
            Qvalue += prob * (self.mdp.getReward(state,action,successor) + self.discount * self.getValue(successor))
        return Qvalue


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        #Get the possilble actions as a list
        Actions = self.mdp.getPossibleActions(state)
        #if there is no more actions return None, as told in the assiignment
        if len(Actions) == 0:
            return None
        else:
            #initialize a list for actions with their values
            actionValues = []
            #for all actions give the action the value of their Qscore
            for action in Actions:
                actionValues.append((self.getQValue(state, action), action))
            #take the maximum score and return the accompanied action
            action = max(actionValues)
            return action[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
