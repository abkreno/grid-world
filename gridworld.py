import numpy as np

def randPair(s,e):
    return np.random.randint(s,e), np.random.randint(s,e)

#finds an array in the "depth" dimension of the grid
def findLoc(state, obj):
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j] == obj).all():
                return i,j

#Initialize stationary grid, all items are placed deterministically
def initGrid():
    state = np.zeros((4,4,5))
    #place player1
    state[0,1] = np.array([0,0,0,0,1])
    #place player2
    state[0,3] = np.array([0,0,0,1,0])
    #place wall
    state[2,2] = np.array([0,0,1,0,0])
    #place pit
    state[1,1] = np.array([0,1,0,0,0])
    #place goal
    state[3,3] = np.array([1,0,0,0,0])

    return state

def makeMove(state, action, index=4):
    #need to locate player in grid
    #need to determine what object (if any) is in the new grid spot the player is moving to
    player_loc = findLoc(state, np.array([0,0,0,0,1]))
    print(player_loc)
    otherp_loc = findLoc(state, np.array([0,0,0,1,0]))
    other_index = 3
    if(index==3):
        player_loc, otherp_loc, other_index = otherp_loc, player_loc, 4
    wall = findLoc(state, np.array([0,0,1,0,0]))
    goal = findLoc(state, np.array([1,0,0,0,0]))
    pit = findLoc(state, np.array([0,1,0,0,0]))
    state = np.zeros((4,4,5))

    #up (row - 1)
    if action==0:
        new_loc = (player_loc[0] - 1, player_loc[1])
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][index] = 1
    #down (row + 1)
    elif action==1:
        new_loc = (player_loc[0] + 1, player_loc[1])
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][index] = 1
    #left (column - 1)
    elif action==2:
        new_loc = (player_loc[0], player_loc[1] - 1)
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][index] = 1
    #right (column + 1)
    elif action==3:
        new_loc = (player_loc[0], player_loc[1] + 1)
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][index] = 1
    arr = np.array([0,0,0,0,0])
    arr[index] = 1
    new_player_loc = findLoc(state, arr)
    if (not new_player_loc):
        state[player_loc] = arr
    #re-place pit
    state[pit][1] = 1
    #re-place wall
    state[wall][2] = 1
    #re-place goal
    state[goal][0] = 1
    #re-place other player
    state[otherp_loc][other_index] = 1
    return state

def getLoc(state, level):
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j][level] == 1):
                return i,j

def getReward(state):
    player1_loc = getLoc(state, 4)
    player2_loc = getLoc(state, 3)
    pit = getLoc(state, 1)
    goal = getLoc(state, 0)
    if (player1_loc == pit or player2_loc == goal):
        return -10
    elif (player1_loc == goal):
        return 10
    else:
        return -1

def dispGrid(state):
    grid = np.zeros((4,4), dtype='<U2')
    player1_loc = findLoc(state, np.array([0,0,0,0,1]))
    player2_loc = findLoc(state, np.array([0,0,0,1,0]))
    wall = findLoc(state, np.array([0,0,1,0,0]))
    goal = findLoc(state, np.array([1,0,0,0,0]))
    pit = findLoc(state, np.array([0,1,0,0,0]))
    for i in range(0,4):
        for j in range(0,4):
            grid[i,j] = ' '

    if player1_loc:
        grid[player1_loc] = 'C' #player1
    if player2_loc:
        grid[player2_loc] = 'P' #player2
    if wall:
        grid[wall] = 'W' #wall
    if goal:
        grid[goal] = '+' #goal
    if pit:
        grid[pit] = '-' #pit

    return grid
