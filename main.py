import numpy as np
from gridworld import initGrid,makeMove,getReward,dispGrid

state = initGrid()
print(dispGrid(state))
state = makeMove(state, 3, 3)
print('Reward: %s' % (getReward(state),))
print(dispGrid(state))
