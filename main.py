import os
import random
import numpy as np
from keras.models import model_from_json
from gridworld import initGrid,makeMove,getReward,dispGrid,getLoc

print("Enter the number of epoches you want to play against e.g (100, 200, 300, ...., 1000):")
num_epochs = int(input())

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("weights/weights_"+str(num_epochs)+".h5")
print("Loaded model from disk")

model = loaded_model

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

testAlgo()
