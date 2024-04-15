import API
import Mouse_Tools

x=0
y=0
orient=0
cell = 0



cells = [[0 for _ in range(16)] for _ in range(16)]

tracker = [[0 for _ in range(16)] for _ in range(16)]

flood=[ [14,13,12,11,10,9,8,7,7,8,9,10,11,12,13,14],
        [13,12,11,10,9,8,7,6,6,7,8,9,10,11,12,13],
        [12,11,10,9,8,7,6,5,5,6,7,8,9,10,11,12],
        [11,10,9,8,7,6,5,4,4,5,6,7,8,9,10,11],
        [10,9,8,7,6,5,4,3,3,4,5,6,7,8,9,10],
        [9,8,7,6,5,4,3,2,2,3,4,5,6,7,8,9],
        [8,7,6,5,4,3,2,1,1,2,3,4,5,6,7,8],
        [7,6,5,4,3,2,1,0,0,1,2,3,4,5,6,7],
        [7,6,5,4,3,2,1,0,0,1,2,3,4,5,6,7],
        [8,7,6,5,4,3,2,1,1,2,3,4,5,6,7,8],
        [9,8,7,6,5,4,3,2,2,3,4,5,6,7,8,9],
        [10,9,8,7,6,5,4,3,3,4,5,6,7,8,9,10],
        [11,10,9,8,7,6,5,4,4,5,6,7,8,9,10,11],
        [12,11,10,9,8,7,6,5,5,6,7,8,9,10,11,12],
        [13,12,11,10,9,8,7,6,6,7,8,9,10,11,12,13],
        [14,13,12,11,10,9,8,7,7,8,9,10,11,12,13,14]  ]

flood2= [   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  ]

queue=[]


#Tracks Orientation while turning
def orientation(orient,turning):
    if (turning== 'L'):
        orient-=1
        if (orient==-1):
            orient=3
    elif(turning== 'R'):
        orient+=1
        if (orient==4):
            orient=0
    elif(turning== 'B'):
        if (orient==0):
            orient=2
        elif (orient==1):
            orient=3
        elif (orient==2):
            orient=0
        elif (orient==3):
            orient=1

    return(orient)

#changes coordininates based on current coordinates and orientation
def updateCoordinates(x,y,orient):

    if (orient==0):
        y+=1
    if (orient==1):
        x+=1
    if (orient==2):
        y-=1
    if (orient==3):
        x-=1

    return(x,y)

def updateWalls(x,y,orient,L,R,F): #decides which kind of box the mouse is currently in and updates walls accordingly
    Mouse_Tools.showSuroundingWalls(x,y,orient,L,R,F)
    if(L and R and F):
        if (orient==0): 
            cells[y][x]= 13
        elif (orient==1): 
            cells[y][x]= 12
        elif (orient==2): 
            cells[y][x]= 11
        elif (orient==3): 
            cells[y][x]= 14

    elif (L and R and not F):
        if (orient==0 or orient== 2): 
            cells[y][x]= 9
        elif (orient==1 or orient==3): 
            cells[y][x]= 10

    elif (L and F and not R):
        if (orient==0): 
            cells[y][x]= 8
        elif (orient==1): 
            cells[y][x]= 7
        elif (orient==2): 
            cells[y][x]= 6
        elif (orient==3): 
            cells[y][x]= 5

    elif (R and F and not L):
        if (orient==0): 
            cells[y][x]= 7
        elif (orient==1): 
            cells[y][x]= 6
        elif (orient==2): 
            cells[y][x]= 5
        elif (orient==3): 
            cells[y][x]= 8

    elif(F):
        if (orient==0): 
            cells[y][x]= 2
        elif (orient==1): 
            cells[y][x]= 3
        elif (orient==2): 
            cells[y][x]= 4
        elif (orient==3): 
            cells[y][x]= 1

    elif(L):
        if (orient==0): 
            cells[y][x]= 1
        elif (orient==1): 
            cells[y][x]= 2
        elif (orient==2): 
            cells[y][x]= 3
        elif (orient==3): 
            cells[y][x]= 4

    elif(R):
        if (orient==0): 
            cells[y][x]= 3
        elif (orient==1): 
            cells[y][x]= 4
        elif (orient==2): 
            cells[y][x]= 1
        elif (orient==3): 
            cells[y][x]= 2

    else:
        cells[y][x]= 15


def isAccessible(x,y,x1,y1): #returns True if mouse can move to x1,y1 from x,y (two adjescent cells)

    if (x==x1):
        if(y>y1):
            if(cells[y][x]==4 or cells[y][x]==5 or cells[y][x]==6 or cells[y][x]==10 or cells[y][x]==11 or cells[y][x]==12 or cells[y][x]==14 or cells[y1][x1]==2 or cells[y1][x1]==7 or cells[y1][x1]==8 or cells[y1][x1]==10 or cells[y1][x1]==12 or cells[y1][x1]==13 or cells[y1][x1]==14 ):
                return (False)
            else:
                return(True)
        else:
            if(cells[y][x]==2 or cells[y][x]==7 or cells[y][x]==8 or cells[y][x]==10 or cells[y][x]==12 or cells[y][x]==13 or cells[y][x]==14 or cells[y1][x1]==4 or cells[y1][x1]==5 or cells[y1][x1]==6 or cells[y1][x1]==10 or cells[y1][x1]==11 or cells[y1][x1]==12 or cells[y1][x1]==14 ):
                return (False)
            else:
                return(True)
            

    elif (y==y1):
        if(x>x1):
            if(cells[y][x]==1 or cells[y][x]==5 or cells[y][x]==8 or cells[y][x]==9 or cells[y][x]==11 or cells[y][x]==13 or cells[y][x]==14 or cells[y1][x1]==3 or cells[y1][x1]==6 or cells[y1][x1]==7 or cells[y1][x1]==9 or cells[y1][x1]==11 or cells[y1][x1]==12 or cells[y1][x1]==13 ):
                return (False)
            else:
                return (True)
        else:
            if(cells[y][x]==3 or cells[y][x]==6 or cells[y][x]==7 or cells[y][x]==9 or cells[y][x]==11 or cells[y][x]==12 or cells[y][x]==13 or cells[y1][x1]==1 or cells[y1][x1]==5 or cells[y1][x1]==8 or cells[y1][x1]==9 or cells[y1][x1]==11 or cells[y1][x1]==13 or cells[y1][x1]==14 ):
                return (False)
            else:
                return (True)


def getSurrounds(x,y): #returns the 4 adjacent squares
    
    x3= x-1
    y3=y
    x0=x
    y0=y+1
    x1=x+1
    y1=y
    x2=x
    y2=y-1
    if(x1>=16):
        x1=-1
    if(y0>=16):
        y0=-1
    return (x0,y0,x1,y1,x2,y2,x3,y3)  #order of cells- north,east,south,west


def changeDestination(maze,destinationx, destinationy):
    for j in range(16):
        for i in range(16):
            flood[i][j]=255

    queue=[]
    maze[destinationy][destinationx]=0

    queue.append(destinationy)
    queue.append(destinationx)

    
    while (len(queue)!=0):
        yrun=queue.pop(0)
        xrun=queue.pop(0)

        x0,y0,x1,y1,x2,y2,x3,y3= getSurrounds(xrun,yrun)
        if(x0>=0 and y0>=0 ):
            if (maze[y0][x0]==255):
                maze[y0][x0]=maze[yrun][xrun]+1
                queue.append(y0)
                queue.append(x0)
        if(x1>=0 and y1>=0 ):
            if (maze[y1][x1]==255):
                maze[y1][x1]=maze[yrun][xrun]+1
                queue.append(y1)
                queue.append(x1)
        if(x2>=0 and y2>=0 ):
            if (maze[y2][x2]==255):
                maze[y2][x2]=maze[yrun][xrun]+1
                queue.append(y2)
                queue.append(x2)
        if(x3>=0 and y3>=0 ):
            if (maze[y3][x3]==255):
                maze[y3][x3]=maze[yrun][xrun]+1
                queue.append(y3)
                queue.append(x3)


def floodFill2(maze): #flood fills to destination
    for i in range(16):
        for j in range(16):
            maze[i][j]=0

    queue=[]
    flood2[7][7]=1
    flood2[8][7]=1
    flood2[7][8]=1
    flood2[8][8]=1

    queue.append(7)
    queue.append(7)
    queue.append(8)
    queue.append(7)
    queue.append(7)
    queue.append(8)
    queue.append(8)
    queue.append(8)

    
    while (len(queue)!=0): 
        yrun=queue.pop(0)
        xrun=queue.pop(0)

        x0,y0,x1,y1,x2,y2,x3,y3= getSurrounds(xrun,yrun)
        if(x0>=0 and y0>=0 and cells[y0][x0]!=0):
            if (maze[y0][x0]==0):
                if (isAccessible(xrun,yrun,x0,y0)):
                    maze[y0][x0]=maze[yrun][xrun]+1
                    queue.append(y0)
                    queue.append(x0)
        if(x1>=0 and y1>=0 and cells[y1][x1]!=0):
            if (maze[y1][x1]==0):
                if (isAccessible(xrun,yrun,x1,y1)):
                    maze[y1][x1]=maze[yrun][xrun]+1
                    queue.append(y1)
                    queue.append(x1)
        if(x2>=0 and y2>=0 and cells[y2][x2]!=0):
            if (maze[y2][x2]==0):
                if (isAccessible(xrun,yrun,x2,y2)):
                    maze[y2][x2]=maze[yrun][xrun]+1
                    queue.append(y2)
                    queue.append(x2)
        if(x3>=0 and y3>=0 and cells[y3][x3]!=0):
            if (maze[y3][x3]==0):
                if (isAccessible(xrun,yrun,x3,y3)):
                    maze[y3][x3]=maze[yrun][xrun]+1
                    queue.append(y3)
                    queue.append(x3)


def floodFill3(maze,queue): #flood fills home

    while (len(queue)!=0):
        yrun=queue.pop(0)
        xrun=queue.pop(0)

        x0,y0,x1,y1,x2,y2,x3,y3= getSurrounds(xrun,yrun)
        if(x0>=0 and y0>=0 ):
            if (maze[y0][x0]==255):
                if (isAccessible(xrun,yrun,x0,y0)):
                    maze[y0][x0]=maze[yrun][xrun]+1
                    queue.append(y0)
                    queue.append(x0)
        if(x1>=0 and y1>=0):
            if (maze[y1][x1]==255):
                if (isAccessible(xrun,yrun,x1,y1)):
                    maze[y1][x1]=maze[yrun][xrun]+1
                    queue.append(y1)
                    queue.append(x1)
        if(x2>=0 and y2>=0 ):
            if (maze[y2][x2]==255):
                if (isAccessible(xrun,yrun,x2,y2)):
                    maze[y2][x2]=maze[yrun][xrun]+1
                    queue.append(y2)
                    queue.append(x2)
        if(x3>=0 and y3>=0 ):
            if (maze[y3][x3]==255):
                if (isAccessible(xrun,yrun,x3,y3)):
                    maze[y3][x3]=maze[yrun][xrun]+1
                    queue.append(y3)
                    queue.append(x3)


def toMove(maze,x,y,xprev,yprev,orient):#returns new direction
 
    x0,y0,x1,y1,x2,y2,x3,y3 = getSurrounds(x,y)
    val= maze[y][x]
    minCell=0
    if (isAccessible(x,y,x0,y0)):
        if (maze[y0][x0]==val-1):
            minCell=0

    if (isAccessible(x,y,x1,y1)):
        if (maze[y1][x1]==val-1):
            minCell=1

    if (isAccessible(x,y,x2,y2)):
        if (maze[y2][x2]==val-1):
            minCell=2

    if (isAccessible(x,y,x3,y3)):
        if (maze[y3][x3]==val-1):
            minCell=3


    if (minCell==orient):
        return ('F')
    elif((minCell==orient-1) or (minCell== orient+3)):
        return('L')
    elif ((minCell==orient+1) or (minCell== orient-3)):
        return('R')
    else:
        return('B')

def show(flood,variable): #updates distance values for all squares
    for x in range(16):
        for y in range(16):
            x0,y0,x1,y1,x2,y2,x3,y3= getSurrounds(x,y)
            a=''
            if isAccessible(x,y,x0,y0):
                a+=str(x0)
                a+=str(y0)
            if isAccessible(x,y,x1,y1):
                a+=str(x1)
                a+=str(y1)
            if isAccessible(x,y,x2,y2):
                a+=str(x2)
                a+=str(y2)
            if isAccessible(x,y,x3,y3):
                a+=str(x3)
                a+=str(y3)
                    
            #API.setText(x,y,a)
            #API.setText(x,y,str(x0)+str(y0)+str(x1)+str(y1)+str(x2)+str(y2)+str(x3)+str(y3))
            API.setText(x,y,str(flood[y][x]))
            #API.setText(x,y,str(variable))



def appendZero():

    for i in range(16):
        for j in range(16):
            flood[i][j]=255

    flood[7][7]=0
    flood[8][7]=0
    flood[7][8]=0
    flood[8][8]=0

    queue.append(7)
    queue.append(7)
    queue.append(8)
    queue.append(7)
    queue.append(7)
    queue.append(8)
    queue.append(8)
    queue.append(8)

def appendDestination(x,y):

    
    # Initialize all cells of the flood matrix to 255
    for i in range(16):
        for j in range(16):
            flood[i][j]=255

    flood[y][x] = 0
    
    # Append the coordinates to the queue
    queue.append(x)
    queue.append(y)

def close_unused_cells(cells):
    for x in range(16):
        for y in range(16):
            if(cells[x][y] == 0):
                API.setWall(x,y,'n')
                API.setWall(x,y,'e')
                API.setWall(x,y,'s')
                API.setWall(x,y,'w')
    return cells

def main():
    x, y = 0, 0
    xprev, yprev = 0, 0
    orient = 0
    step = 0
    short = False
    visits_start = 0
    keep_going = True

    while keep_going:

        # Update walls and cell value
        L = API.wallLeft()
        R = API.wallRight()
        F = API.wallFront()
        updateWalls(x, y, orient, L, R, F)
        API.setColor(x, y, 'G')
        

        if x == 0 and y == 0:
            visits_start += 1

        tracker[x][y] += 1

        if flood[y][x] != 0:

            if step == 0: 
               
                appendZero()
            elif step == 1: 
                
                appendDestination(0, 0)
            floodFill3(flood, queue)

        else:

            if step == 1:
                changeDestination(flood, 0, 0)
                step += 1
            elif step == 0:
                #x, y, xprev, yprev, orient = center(x, y, orient)
                changeDestination(flood, 15, 0)
                step += 1

            floodFill2(flood2)

        # Determine direction to move
        direction = toMove(flood, x, y, xprev, yprev, orient)

        # Move in the determined direction
        if direction == 'L':
            API.turnLeft()
            orient = orientation(orient, 'L')
        elif direction == 'R':
            API.turnRight()
            orient = orientation(orient, 'R')
        elif direction == 'B':
            API.turnLeft()
            orient = orientation(orient, 'L')
            API.turnLeft()
            orient = orientation(orient, 'L')

        show(flood, step)

        if visits_start > 1:
            Mouse_Tools.log("Speed run!!")
            keep_going = False
            break

        API.moveForward()
        xprev, yprev = x, y
        x, y = updateCoordinates(x, y, orient)

    # Follow the shortest path
    while True:
        show(flood2, step)
        L = API.wallLeft()
        R = API.wallRight()
        F = API.wallFront()
        API.setColor(x, y, 'g')

        if flood2[y][x] != 1:
            direction = toMove(flood2, x, y, xprev, yprev, orient)

            if direction == 'L':
                API.turnLeft()
                orient = orientation(orient, 'L')
            elif direction == 'R':
                API.turnRight()
                orient = orientation(orient, 'R')
            elif direction == 'B':
                API.turnLeft()
                orient = orientation(orient, 'L')
                API.turnLeft()
                orient = orientation(orient, 'L')

            show(flood2, step)
            API.moveForward()
            xprev, yprev = x, y
            x, y = updateCoordinates(x, y, orient)
        else:
            break
    return


if __name__ == "__main__":
    main()