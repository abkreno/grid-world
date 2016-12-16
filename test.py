import numpy as np
from pprint import pprint
from gridworld import initGrid,makeMove,getReward,dispGrid

state = initGrid()
arr = dispGrid(state)
pprint(arr)
state = makeMove(state, 1)
arr = dispGrid(state)
pprint(arr)
print(getReward(state))
state = makeMove(state, 1)
print('Reward: %s' % (getReward(state),))
dispGrid(state)
