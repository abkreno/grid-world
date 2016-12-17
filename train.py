import os
import random
import numpy as np
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from gridworld import initGrid,makeMove,getReward,dispGrid,getLoc
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

epochs = 1000
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
        new_state = makeMove(new_state, np.random.randint(0,4), 3)
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
    if (i+1) % 100 == 0:
        print("Saving weights at epoch: "+str(i+1)+"...")
        model.save_weights("weights/weights_"+str(i+1)+".h5")
        print("Saved model to disk")

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
