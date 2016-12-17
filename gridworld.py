import numpy as np

def randPair(s,e):
    return np.random.randint(s,e), np.random.randint(s,e)

def getLoc(state, level):
    for i in range(0,4):
        for j in range(0,4):
            if (state[i,j][level] == 1):
                return i,j

#finds an array in the "depth" dimension of the grid
def findLoc(state, obj):
    for i in range(0,4):
        for j in range(0,4):
            # for k in range(0,5):
            #     if(state[i,j,k]==obj[k] and obj[k] == 1):
            #         return i,j
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

def makeMove(state, action, player_index=4):
    #need to locate player in grid
    #need to determine what object (if any) is in the new grid spot the player is moving to
    player_loc   = getLoc(state, 4)
    otherp_loc   = getLoc(state, 3)

    otherp_index = 3
    if(player_index==3):
        player_loc, otherp_loc, otherp_index = otherp_loc, player_loc, 4

    wall = getLoc(state, 2)
    goal = getLoc(state, 0)
    pit = getLoc(state, 1)
    state = np.zeros((4,4,5))

    #up (row - 1)
    if action==0:
        new_loc = (player_loc[0] - 1, player_loc[1])
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][player_index] = 1
    #down (row + 1)
    elif action==1:
        new_loc = (player_loc[0] + 1, player_loc[1])
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][player_index] = 1
    #left (column - 1)
    elif action==2:
        new_loc = (player_loc[0], player_loc[1] - 1)
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][player_index] = 1
    #right (column + 1)
    elif action==3:
        new_loc = (player_loc[0], player_loc[1] + 1)
        if (new_loc != wall):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][player_index] = 1

    new_player_loc = getLoc(state, player_index)
    if (not new_player_loc):
        state[player_loc][player_index] = 1

    #re-place pit
    state[pit][1] = 1
    #re-place wall
    state[wall][2] = 1
    #re-place goal
    state[goal][0] = 1
    #re-place other player
    state[otherp_loc][otherp_index] = 1

    return state

def getReward(state, index=4):
    player_loc = getLoc(state, index)
    pit = getLoc(state, 1)
    goal = getLoc(state, 0)
    if (player_loc == pit):
        return -10
    elif (player_loc == goal):
        return 10
    else:
        return -1

def dispGrid(state):
    grid = np.zeros((4,4), dtype='a6')
    player1_loc = findLoc(state, np.array([0,0,0,0,1]))
    player2_loc = findLoc(state, np.array([0,0,0,1,0]))
    both = findLoc(state, np.array([0,0,0,1,1]))
    wall = findLoc(state, np.array([0,0,1,0,0]))
    goal = findLoc(state, np.array([1,0,0,0,0]))
    p1_goal = findLoc(state, np.array([1,0,0,0,1]))
    p2_goal = findLoc(state, np.array([1,0,0,1,0]))
    pit = findLoc(state, np.array([0,1,0,0,0]))
    p1_pit = findLoc(state, np.array([0,1,0,0,1]))
    p2_pit = findLoc(state, np.array([0,1,0,1,0]))
    for i in range(0,4):
        for j in range(0,4):
            grid[i,j] = '      '

    if player1_loc:
        grid[player1_loc] = '  P1  ' #player1
    if player2_loc:
        grid[player2_loc] = '  P2  ' #player2
    if both:
        grid[both] = 'P1  P2'
    if wall:
        grid[wall] = ' WALL ' #wall
    if goal:
        grid[goal] = ' GOAL ' #goal
    if p1_goal:
        grid[p1_goal] = 'P1GOAL'
    if p2_goal:
        grid[p2_goal] = 'P2GOAL'
    if pit:
        grid[pit] = ' PIT- ' #pit
    if p1_pit:
        grid[p1_pit] = 'P1PIT- ' #pit
    if p2_pit:
        grid[p2_pit] = 'P2PIT-' #pit

    for i in range(0,4):
        print(grid[i])
    return grid
