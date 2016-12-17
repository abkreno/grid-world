import numpy as np
import random
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from gridworld import initGrid,makeMove,getReward,dispGrid
from IPython.display import clear_output

model = Sequential()
model.add(Dense(164, init='lecun_uniform', input_shape=(80,)))
model.add(Activation('relu'))
#model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

model.add(Dense(150, init='lecun_uniform'))
model.add(Activation('relu'))
#model.add(Dropout(0.2))

model.add(Dense(4, init='lecun_uniform'))
model.add(Activation('linear')) #linear output so we can have range of real-valued outputs

rms = RMSprop()
model.compile(loss='mse', optimizer=rms)

epochs = 10
gamma = 0.9 #since it may take several moves to goal, making gamma high
epsilon = 1
for i in range(epochs):

    state = initGrid()
    status = 1
    #while game still in progress
    while(status == 1):
        #We are in state S
        #Let's run our Q function on S to get Q values for all possible actions
        qval = model.predict(state.reshape(1,80), batch_size=1)
        if (random.random() < epsilon): #choose random action
            action = np.random.randint(0,4)
        else: #choose best action from Q(s,a) values
            action = (np.argmax(qval))
        #Take action, observe new state S'
        new_state = makeMove(state, action)
        #Observe reward
        reward = getReward(new_state)
        #Get max_Q(S',a)
        newQ = model.predict(new_state.reshape(1,80), batch_size=1)
        maxQ = np.max(newQ)
        y = np.zeros((1,4))
        y[:] = qval[:]
        if reward == -1: #non-terminal state
            update = (reward + (gamma * maxQ))
        else: #terminal state
            update = reward
        y[0][action] = update #target output
        print("Game #: %s" % (i,))
        model.fit(state.reshape(1,80), y, batch_size=1, nb_epoch=1, verbose=1)
        state = new_state
        if reward != -1:
            status = 0
        clear_output(wait=True)
    if epsilon > 0.1:
        epsilon -= (1/epochs)

def testAlgo(init=0):
    state = initGrid()
    print("Initial State:")
    dispGrid(state)
    status = 1
    i = 0
    #while game still in progress
    while(status == 1):
        qval = model.predict(state.reshape(1,80), batch_size=1)
        action = (np.argmax(qval)) #take action with highest Q-value
        print('Move #: %s; Taking action: %s' % (i, action))
        state = makeMove(state, action, 4)
        dispGrid(state)
        reward = getReward(state)
        if reward == -10:
            print("The agent steped on the pit.. You won!")
            state = 0
            break
        elif reward == 10:
            print("The agent won!")
            state = 0
            break

        print("Enter your move (0,1,2,3) for (up,down,left,right)")
        action = int(input())
        state = makeMove(state, action, 3)
        reward = getReward(state,3)
        dispGrid(state)
        if reward == -10:
            print("You Lost!")
            state = 0
            break
        elif reward == 10:
            print("You won!")
            state = 0
            break
        i+=1
