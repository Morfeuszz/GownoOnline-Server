from itertools import product

grid_size = 50 
map_size = 1000
grid = [ [ [] for y in range(int(map_size/grid_size)) ] for x in range(int(map_size/grid_size))]
disconnectedID = set()


def addToGrid(x,y,ID):
    temp = grid[x][y]
    temp.append(ID)
    print(temp)

def changeToGrid(x,y,oldX,oldY,ID):
    temp = grid[oldX][oldY]
    temp.remove(ID)
    temp = grid[x][y]
    temp.append(ID)

def removeToGrid(x,y,ID):
    temp = grid[x][y] 
    temp.remove(ID)

def usersInGrid(x,y):
    usersList = []
    temp = grid[x][y]
    for id in temp:
        if id in disconnectedID:
            temp.remove(id)
    
    usersList.extend(temp)
    for user in list(neighbours((x,y))):
        temp = grid[user[0]][user[1]]
        for id in temp:
            if id in disconnectedID:
                temp.remove(id)
        usersList.extend(temp)
    return usersList

def neighbours(cell):
    for c in product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= n < len(grid) for n in c):
            yield c

    
